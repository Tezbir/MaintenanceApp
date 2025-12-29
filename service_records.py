from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from .sesh import get_db, get_current_user
from .model import ServiceRecord, Vee, User
from .schemas import ServiceRecordCreate, ServiceRecordOut

router = APIRouter(prefix="/service-records", tags=["service-records"])

def assert_vee_owner(db: Session, vee_id: int, user_id: int):
    vee = db.get(Vee, vee_id)
    if not vee or vee.user_id != user_id:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vee

@router.get("/vee/{vee_id}", response_model=list[ServiceRecordOut])
def list_records_for_vee(vee_id: int, db: Session = Depends(get_db), me: User = Depends(get_current_user)):
    assert_vee_owner(db, vee_id, me.user_id)
    q = select(ServiceRecord).where(ServiceRecord.vee_id == vee_id).order_by(ServiceRecord.service_record_date.desc())
    return db.execute(q).scalars().all()

@router.post("", response_model=ServiceRecordOut)
def create_record(body: ServiceRecordCreate, db: Session = Depends(get_db), me: User = Depends(get_current_user)):
    assert_vee_owner(db, body.vee_id, me.user_id)
    rec = ServiceRecord(**body.model_dump())
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

@router.delete("/{service_record_id}")
def delete_record(service_record_id: int, db: Session = Depends(get_db), me: User = Depends(get_current_user)):
    rec = db.get(ServiceRecord, service_record_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")
    vee = assert_vee_owner(db, rec.vee_id, me.user_id)
    db.delete(rec)
    db.commit()
    return {"ok": True}
