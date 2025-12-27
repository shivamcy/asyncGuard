from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.models
from app.api import auth
from app.api import organizations
from app.config.settings import settings
from app.api import apis
from app.api import user
from app.api import audits

def create_app() -> FastAPI:
    app = FastAPI(
        title="asyncGuard",
        description="Async API Security & Compliance Platform",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #  Routers 
    app.include_router(auth.router)
    app.include_router(organizations.router)
    app.include_router(apis.router)
    app.include_router(user.router)
    app.include_router(audits.router)

    # Health Check 
    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "ok"}

    return app
app = create_app()
