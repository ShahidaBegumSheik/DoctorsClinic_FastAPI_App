from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from app.core.config import settings
from app.core.rate_limit import limiter
from app.api.routers import auth, doctors, patients, assignments
from app.db.base import Base
from app.db.session import engine
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # For alembic-based migrations we mustnot use create_all()
    # Base.metadata.create_all(bind=engine) 

    yield

app = FastAPI(
    lifespan=lifespan,
    title=settings.APP_NAME,
    description="FastAPI backend for Doctors & Patients with JWT auth and RBAC",
)


# Rate limiting (global)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Routers
app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(assignments.router)

@app.get("/health", tags=["System"])
@limiter.limit("30/minute")
def health(request: Request):
    return {"status": "ok", "env": settings.ENV}