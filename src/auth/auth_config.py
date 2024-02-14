from pathlib import Path

from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.templating import Jinja2Templates
from httpx_oauth.clients.google import GoogleOAuth2

from src.config import BASE_DIR, GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl='https://accounts.google.com/o/oauth2/auth',
    tokenUrl='https://oauth2.googleapis.com/token',
)

SCOPES = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/docs',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
]


oauth2_credentials = {
    'client_id': GOOGLE_OAUTH_CLIENT_ID,
    'client_secret': GOOGLE_OAUTH_CLIENT_SECRET,
    'scopes': SCOPES,
}

oauth2_client = GoogleOAuth2(**oauth2_credentials)

sessions = {}

global logged_in

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))
