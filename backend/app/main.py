"""
Route Optimization SaaS - FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.routes import health, auth, users, routes, optimize, jobs, geocoding

# ---------------------------------------------------------------------------
# Lifespan: create DB tables on startup
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown (clean-up if needed)

# ---------------------------------------------------------------------------
# App instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Route Optimization SaaS API powered by OSRM",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(health.router,   prefix="/api/v1",          tags=["Health"])
app.include_router(auth.router,     prefix="/api/v1/auth",      tags=["Auth"])
app.include_router(users.router,    prefix="/api/v1/users",     tags=["Users"])
app.include_router(routes.router,   prefix="/api/v1/routes",    tags=["Routes"])
app.include_router(optimize.router, prefix="/api/v1/optimize",  tags=["Optimization"])
app.include_router(jobs.router,     prefix="/api/v1/jobs",      tags=["Jobs"])
app.include_router(geocoding.router, prefix="/geocode",         tags=["Geocoding"])
