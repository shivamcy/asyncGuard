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
from app.api import stats
from app.api import health
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.config.limiter import limiter

def create_app() -> FastAPI:
    app = FastAPI(
        title="asyncGuard",
        description="Async API Security & Compliance Platform",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
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
    app.include_router(stats.router)
    app.include_router(health.router)


    return app
app = create_app()
