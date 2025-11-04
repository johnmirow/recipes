from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/allergens", tags=["Allergens"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.AllergenResponse)
def add_allergen(data: schemas.AllergenCreate, db: Session = Depends(get_db)):
    allergen = crud.create_allergen(db, data.name, data.description)
    return allergen

@router.get("/", response_model=list[schemas.AllergenResponse])
def get_allergens(db: Session = Depends(get_db)):
    return crud.list_allergens(db)
