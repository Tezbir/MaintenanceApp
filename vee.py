from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from .sesh import get_db, get_current_user
from .model import Vee, User
from .schemas import VeeCreate, VeeOut

router = APIRouter(prefix="/vee", tags=["vee"])

@router.get("", response_model=list[VeeOut])
def list_vees(db: Session = Depends(get_db), me: User = Depends(get_current_user)):
    return db.execute(select(Vee).where(Vee.user_id == me.user_id).order_by(Vee.vee_stamped.desc())).scalars().all()

@router.post("", response_model=VeeOut)
def create_vee(body: VeeCreate, db: Session = Depends(get_db), me: User = Depends(get_current_user)):
    vee = Vee(user_id=me.user_id, **body.model_dump())
    db.add(vee)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create vehicle (maybe duplicate VIN for this user?)")
    db.refresh(vee)
    return vee

@router.delete("/{vee_id}")
def delete_vee(vee_id: int, db: Session = Depends(get_db), me: User = Depends(get_current_user)):
    vee = db.get(Vee, vee_id)
    if not vee or vee.user_id != me.user_id:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    db.delete(vee)
    db.commit()
    return {"ok": True}
