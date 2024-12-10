# uvicorn main:app --reload
import time

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dao import database

from app.auth.router import router as auth_router
from app.projects.router import router as projects_router

app = FastAPI(title='educonnect', version='127.0.0.1')
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


@app.get("/")
@app.get("/status/")
async def status():
    return {'app': app.title,
            'version': app.version,
            'status': 'running',
            'uptime': round(time.time() - run_time)}
