import io
from typing import List

from fastapi import UploadFile
from google.auth import exceptions
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from starlette.responses import RedirectResponse


def get_service(credentials):
    return build('drive', 'v3', credentials=credentials)


def download_file_by_id(file_id: str, service):
    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f'Download {int(status.progress() * 100)}%')
    return file.getvalue()


def folders_and_files(credentials: Credentials | None, file_id: str | None = None):
    service = get_service(credentials)
    if not file_id:
        try:
            root_folder = service.files().get(fileId='root').execute()
            root_folder_files = service.files().list(
                q=f'"{root_folder["id"]}" in parents and trashed=false',
                fields='nextPageToken, files(id, name, mimeType, parents, size)',
            ).execute()
            return root_folder_files.get('files', [])
        except exceptions.RefreshError:
            return RedirectResponse(url='/auth/login')

    file = service.files().get(fileId=file_id).execute()
    if not file:
        return None
    if file['mimeType'] == 'application/vnd.google-apps.folder':
        folder_files = service.files().list(
            q=f'"{file["id"]}" in parents and trashed=false',
            fields='nextPageToken, files(id, name, mimeType, parents, size)',
        ).execute()
        return folder_files.get('files', [])
    else:
        return download_file_by_id(file_id, service)


def search_file(credentials: Credentials | None, file_name=None, folder_name=None, page_size: int = 10):
    service = get_service(credentials)
    files = []
    if file_name:
        query = f'name = "{file_name}" and trashed=false'
    elif folder_name:
        query = f'"{folder_name}" in parents and trashed=false'
    elif file_name and folder_name:
        query = f'"{folder_name}" in parents and name = "{file_name}" and trashed=false'
    else:
        query = "mimeType='application/vnd.google-apps.folder'"
    response = (
        service.files()
        .list(
            pageSize=page_size,
            q=query,
            spaces='drive',
            fields='nextPageToken, files(id, name, mimeType, parents, size)',
        )
        .execute()
    )
    files.extend(response.get('files', []))

    return files


def create_folder(credentials: Credentials | None, folder_name: str, parent_folder_id: str = None):
    try:
        service = get_service(credentials)
        if not parent_folder_id or parent_folder_id == 'null':
            root_folder = service.files().get(fileId='root').execute()
            parent_folder_id = root_folder.get('id')
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id],
        }
        file = service.files().create(body=file_metadata, fields='id, parents').execute()
        return file.get('parents', [])[0]
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def move_file(credentials: Credentials | None, file_id: str, new_folder_id: str):
    try:
        service = get_service(credentials)
        file = service.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ','.join(file.get('parents'))
        file = service.files().update(
            fileId=file_id,
            addParents=new_folder_id,
            removeParents=previous_parents,
            fields='id, parents',
        ).execute()
        print(f'File ID {file_id} moved to folder ID {new_folder_id}')
        return file.get('id')
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def move_to_trash(credentials: Credentials | None, file_id: str):
    try:
        service = get_service(credentials)
        body_value = {'trashed': True}
        file = service.files().update(fileId=file_id, body=body_value).execute()
        return file.get('id')
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def recover_from_trash(credentials: Credentials | None, file_id: str):
    try:
        service = get_service(credentials)
        body_value = {'trashed': False}
        file = service.files().update(fileId=file_id, body=body_value).execute()
        return file.get('id')
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def empty_trash(credentials: Credentials | None):
    try:
        service = get_service(credentials)
        service.files().emptyTrash().execute()
        return True
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def list_files_in_trash(credentials: Credentials | None):
    try:
        service = get_service(credentials)
        files = service.files().list(q='trashed=true', fields='files(id, name, mimeType, parents, size)').execute()
        return files.get('files', [])
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def delete_file(credentials: Credentials, file_id: str):
    try:
        service = get_service(credentials)
        service.files().delete(fileId=file_id).execute()
        return True
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def upload_files(credentials: Credentials | None, files: List[UploadFile], folder_id: str | None = None):
    try:
        service = get_service(credentials)
        for file in files:
            file_metadata = {'name': file.filename}
            if folder_id or not folder_id == 'null':
                file_metadata['parents'] = [folder_id]
            fh = io.BytesIO(file.file.read())
            media = MediaIoBaseUpload(fh, mimetype=file.content_type)
            file = (
                service.files()
                .create(body=file_metadata, media_body=media, fields='id, parents')
                .execute()
            )
            return file.get('parents', [])[0]
    except HttpError as error:
        print(f'An error occurred: {error}')


def update_file(credentials: Credentials | None, file_to_replace: UploadFile, file_id: str):
    try:
        service = get_service(credentials)
        fh = io.BytesIO(file_to_replace.file.read())
        media = MediaIoBaseUpload(fh, mimetype=file_to_replace.content_type, resumable=True)
        (
            service.files()
            .update(fileId=file_id, body={}, media_body=media, fields='id')
            .execute()
        )
    except HttpError as err:
        print(f'An error occurred: {err}')


def download_file(credentials: Credentials | None, file_id=None, file_name=None):
    if file_id:
        service = get_service(credentials)
        return download_file_by_id(file_id, service)
    elif file_name:
        files = search_file(credentials=credentials, file_name=file_name)
        if len(files) == 0:
            print(f"Couldn't find file: {file_name}")
        elif len(files) > 1:
            print(f'Multiple files found: {len(files)}')
            return
        file_id = files[0]['id']
        return download_file(file_id)
    else:
        print('no file_id or file_name provided')


def export_file(credentials: Credentials | None, file_id):
    try:
        service = get_service(credentials)
        request = service.files().export_media(
            fileId=file_id, mimeType='application/pdf',
        )
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(f'An error occurred: {error}')
        file = None

    return file.getvalue()
