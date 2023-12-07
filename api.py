from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from licenseplates.api import router
from licenseplates.model import lpmodel

lpmodel.init_modules()

app = FastAPI()

app.include_router(router.router, prefix="/api")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)
