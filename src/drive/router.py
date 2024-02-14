import io
import json
from typing import List, Optional

from fastapi import APIRouter, Cookie, UploadFile
from fastapi.responses import Response, StreamingResponse
from google.oauth2.credentials import Credentials
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from src.auth.auth_config import sessions, templates
from src.drive import drive

router = APIRouter(
    prefix='/drive',
    tags=['drive'],
)


def get_credentials(session_id) -> Credentials | None:
    credentials = None
    if session_id in sessions:
        token = sessions[session_id]
        if token:
            token_json = json.loads(Credentials(token).to_json()).get('token')
            credentials = Credentials(token_json.get('access_token'))
        return credentials


@router.get('/folders_and_files', response_class=HTMLResponse)
async def get_folders_and_files(
        request: Request,
        file_id: str | None = None,
        session_id: Optional[str] = Cookie(None),
):
    credentials = get_credentials(session_id)
    if not credentials:
        return RedirectResponse(url='/auth/login')
    folders_and_files = drive.folders_and_files(credentials=credentials, file_id=file_id)
    if isinstance(folders_and_files, bytes):
        file_like_object = io.BytesIO(folders_and_files)
        return StreamingResponse(file_like_object, media_type='application/octet-stream')
    return templates.TemplateResponse(
        'folders_and_files.html', {
            'request': request, 'folders_and_files': folders_and_files,
        },
    )


@router.get('/search')
async def search(
        request: Request,
        file_name: str | None = None,
        folder_name: str | None = None,
        page_size: int = 15,
        session_id: Optional[str] = Cookie(None),
):
    credentials = get_credentials(session_id)
    if not credentials:
        return RedirectResponse(url='/auth/login')
    search_list = drive.search_file(
        credentials=credentials, file_name=file_name, folder_name=folder_name, page_size=page_size,
    )
    return templates.TemplateResponse(
        'search.html', {'request': request, 'search_list': search_list},
    )


@router.get('/download')
async def download_file(
        file_id: str | None = None,
        file_name: str | None = None,
        session_id: Optional[str] = Cookie(None),
):
    credentials = get_credentials(session_id)
    if not credentials:
        return RedirectResponse(url='/auth/login')
    result = drive.download_file(credentials=credentials, file_id=file_id, file_name=file_name)
    file_like_object = io.BytesIO(result)
    return StreamingResponse(file_like_object, media_type='application/octet-stream')


@router.post('/create_files')
async def upload_files(
        request: Request,
        files: List[UploadFile],
        folder_id: str | None = None,
        session_id: Optional[str] = Cookie(None),
):
    credentials = get_credentials(session_id)
    if not credentials:
        return RedirectResponse(url='/auth/login')
    result = drive.upload_files(credentials=credentials, files=files, folder_id=folder_id)
    response = Response(status_code=303)
    response.headers['Location'] = f'/drive/folders_and_files/?&file_id={result}'
    return response


@router.get('/create_folder')
async def create_folder(
        folder_name: str,
        parent_folder_id: str | None = None,
        session_id: Optional[str] = Cookie(None),
):
    credentials = get_credentials(session_id)
    if not credentials:
        return RedirectResponse(url='/auth/login')
    result = drive.create_folder(credentials=credentials, folder_name=folder_name, parent_folder_id=parent_folder_id)
    return RedirectResponse(url=f'/drive/folders_and_files/?&file_id={result}')


@router.get('/move_file')
async def move_file(
        file_id: str,
        new_folder_id: str,
        session_id: Optional[str] = Cookie(None),
):
    credentials = get_credentials(session_id)
    if not credentials:
        return RedirectResponse(url='/auth/login')
    drive.move_file(credentials=credentials, file_id=file_id, new_folder_id=new_folder_id)
    return RedirectResponse(url=f'/drive/folders_and_files/?&file_id={new_folder_id}')


@router.get('/move_to_trash')
async def move_to_trash(
        file_id: str | None = None,
        session_id: Optional[str] = Cookie(None),
):
    credentials = get_credentials(session_id)
    if not credentials:
        return RedirectResponse(url='/auth/login')
    drive.move_to_trash(credentials=credentials, file_id=file_id)
    return RedirectResponse(url='/drive/list_files_in_trash')


@router.get('/recover_from_trash')
async def recover_from_trash(
        file_id: str | None = None,
        session_id: Optional[str] = Cookie(None),
):
    credentials = get_credentials(session_id)
    if not credentials:
        return RedirectResponse(url='/auth/login')
    drive.recover_from_trash(credentials=credentials, file_id=file_id)
    return RedirectResponse(url='/drive/folders_and_files')


@router.get('/empty_trash')
async def empty_trash(
        session_id: Optional[str] = Cookie(None),
):
    credentials = get_credentials(session_id)
    if not credentials:
        return RedirectResponse(url='/auth/login')
    drive.empty_trash(credentials=credentials)
    return RedirectResponse(url='/drive/list_files_in_trash')


@router.get('/list_files_in_trash')
async def list_files_in_trash(
        request: Request,
        session_id: Optional[str] = Cookie(None),
):
    credentials = get_credentials(session_id)
    if not credentials:
        return RedirectResponse(url='/auth/login')
    trash_list = drive.list_files_in_trash(credentials=credentials)
    return templates.TemplateResponse(
        'trash.html', {'request': request, 'trash_list': trash_list},
    )


@router.get('/delete_file')
async def delete_file(
        file_id: str | None = None,
        session_id: Optional[str] = Cookie(None),
):
    credentials = get_credentials(session_id)
    if not credentials:
        return RedirectResponse(url='/auth/login')
    drive.delete_file(credentials=credentials, file_id=file_id)
    return RedirectResponse(url='/drive/folders_and_files')


@router.get('/export_file_to_pdf')
async def export_file(
        file_id: str,
        session_id: Optional[str] = Cookie(None),
):
    credentials = get_credentials(session_id)
    if not credentials:
        return RedirectResponse(url='/auth/login')
    return drive.export_file(credentials=credentials, file_id=file_id)
