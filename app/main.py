# uvicorn main:app --reload
import time
from contextlib import asynccontextmanager
import asyncio

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dao import database

from app.tgbot import bot_start_polling, bot_stop_polling
from app.auth.router import router as auth_router
from app.projects.router import router as projects_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(bot_start_polling())
    yield
    await bot_stop_polling()
    # await bot.delete_webhook()


app = FastAPI(title='educonnect', version='127.0.0.1', lifespan=lifespan)
run_time = time.time()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(projects_router)

# app.include_router(api_router, prefix='/api/latest')
app.include_router(api_router, prefix='/api/v1')

@app.on_event("startup")
async def startup():
    await database.init_db_if_required()
    # asyncio.run(bot_start_polling())


@app.get("/")
@app.get("/status/")
async def status():
    return {'app': app.title,
            'version': app.version,
            'status': 'running',
            'uptime': round(time.time() - run_time)}
