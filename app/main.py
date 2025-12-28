from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.models
from app.api import auth
from app.api import organizations
from app.config.settings import settings
from app.api import apis
from app.api import user
#from app.api import audits
from app.api import reports
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.config.limiter import limiter

<<<<<<< HEAD
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
=======

>>>>>>> temp-fix

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
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    #  Routers 
    app.include_router(auth.router)
    app.include_router(organizations.router)
    app.include_router(apis.router)
    app.include_router(user.router)
   # app.include_router(audits.router)
    app.include_router(reports.router)

    # Health Check 
    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "ok"}

    return app
app = create_app()
