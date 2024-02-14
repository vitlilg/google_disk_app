from typing import Optional

from fastapi import APIRouter, Cookie, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.auth.auth_config import oauth2_client, sessions, templates
from src.config import REDIRECT_URL

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.get('/login', response_class=HTMLResponse)
async def login_redirect(request: Request):
    authorization_url = await oauth2_client.get_authorization_url(redirect_uri=REDIRECT_URL)
    return templates.TemplateResponse('login.html', {'request': request, 'authorization_url': authorization_url})


@router.get('/callback')
async def callback(request: Request, code: str, state: Optional[str] = None):
    token = await oauth2_client.get_access_token(code=code, redirect_uri=REDIRECT_URL)
    if token:
        session_id = str(hash(token['access_token']))
        sessions[session_id] = token
        response = RedirectResponse(url='/drive/folders_and_files')
        response.set_cookie(key='session_id', value=session_id)
        return response
    else:
        raise HTTPException(status_code=400, detail='Failed to retrieve access token')


@router.get('/logout')
async def logout(request: Request, session_id: Optional[str] = Cookie(None)):
    if session_id in sessions:
        sessions.pop(session_id)
    return RedirectResponse(url='/auth/login')
