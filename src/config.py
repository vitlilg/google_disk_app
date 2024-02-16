import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

SECRET = os.environ.get('SECRET', 'secret')

GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '')
GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET', '')

if GOOGLE_OAUTH_CLIENT_ID is None or GOOGLE_OAUTH_CLIENT_SECRET is None:
    raise Exception('Missing env variables')

if not SECRET:
    raise 'Missing SECRET_KEY'

REDIRECT_URL = os.environ.get('REDIRECT_URL', '')

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
