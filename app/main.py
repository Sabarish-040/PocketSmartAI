from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import Base, engine
from app.routes import auth, pages, planners

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="PocketSmart AI - Smart Budget and Recommendation Assistant",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(planners.router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "ai_configured": bool(settings.gemini_api_key),
    }


@app.get("/startup")
def startup_status():
    return {
        "status": "initialized",
        "model": settings.gemini_model,
    }