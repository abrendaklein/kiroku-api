from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Kiroku
from app.schemas import KirokuCreate, KirokuUpdate, KirokuResponse

router = APIRouter(prefix="/kiroku", tags=["kiroku"])


# used by get, update and delete, so the 404 logic lives in one place
def get_record_or_404(kiroku_id: int, db: Session) -> Kiroku:
    record = db.query(Kiroku).filter(Kiroku.id == kiroku_id).first()

    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    return record


@router.post("/", response_model=KirokuResponse, status_code=201)
def create_kiroku(data: KirokuCreate, db: Session = Depends(get_db)):
    record = Kiroku(**data.model_dump())
    db.add(record)
    db.commit()
    # reload from the db to get id and created_at, which it generated
    db.refresh(record)
    return record


# skip/limit = simple pagination, so we never return the whole table
@router.get("/", response_model=list[KirokuResponse])
def get_kiroku(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return db.query(Kiroku).offset(skip).limit(limit).all()


@router.get("/{kiroku_id}", response_model=KirokuResponse)
def get_kiroku_by_id(kiroku_id: int, db: Session = Depends(get_db)):
    return get_record_or_404(kiroku_id, db)


@router.put("/{kiroku_id}", response_model=KirokuResponse)
def update_kiroku(
    kiroku_id: int,
    data: KirokuUpdate,
    db: Session = Depends(get_db)
):
    record = get_record_or_404(kiroku_id, db)

    # exclude_unset: only update what the client actually sent
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


# 204 = success with no body, so there's nothing to return
@router.delete("/{kiroku_id}", status_code=204)
def delete_kiroku(kiroku_id: int, db: Session = Depends(get_db)):
    record = get_record_or_404(kiroku_id, db)

    db.delete(record)
    db.commit()