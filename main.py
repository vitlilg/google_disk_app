import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.config import REDIS_HOST, REDIS_PORT
from src.drive.router import router as drive_router

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@asynccontextmanager
async def lifespan(_):
    redis = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}', encoding='utf-8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    yield
    FastAPICache.reset()


app = FastAPI(
    title='Simple Google Drive App',
    lifespan=lifespan,
)


@app.middleware('http')
async def log_requests(request: Request, call_next):
    path = request.url.path
    method = request.method
    client_host = request.client.host
    logging.info(f'User {client_host} accessed {method} {path}')
    response = await call_next(request)
    return response

origins = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=[
        'Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers', 'Access-Control-Allow-Origin',
        'Authorization',
    ],
)


def get_logger(request: Request):
    return logging.getLogger('user_activity')


app.include_router(auth_router)
app.include_router(drive_router)
