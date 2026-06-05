from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database import engine, Base
from backend.app.routers import (
    health,
    auth,
    modules,
    perception,
    travel,
    ai,
    kpop,
    football,
)

app = FastAPI(
    title="KoreaIntel Pro API",
    description="Full-stack backend for Korea market and culture intelligence workspace",
    version="1.0.0",
)

# CORS - allow Streamlit frontend on any port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(modules.router)
app.include_router(perception.router)
app.include_router(travel.router)
app.include_router(ai.router)
app.include_router(kpop.router)
app.include_router(football.router)
