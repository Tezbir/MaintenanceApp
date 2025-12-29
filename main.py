from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .user import router as user_router
from .vee import router as vee_router
from .service_types import router as service_types_router
from .service_records import router as service_record_router  # change name if your file differs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(vee_router)
app.include_router(service_types_router)
app.include_router(service_record_router)
