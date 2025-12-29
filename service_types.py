from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from .sesh import get_db
from .model import ServiceType
from .schemas import ServiceTypeOut

router = APIRouter(prefix="/service-types", tags=["service-types"])

@router.get("", response_model=list[ServiceTypeOut])
def list_service_types(db: Session = Depends(get_db)):
    return db.execute(select(ServiceType).order_by(ServiceType.service_type_name.asc())).scalars().all()
