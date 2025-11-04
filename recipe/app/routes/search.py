from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/search", tags=["Search"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/safe", response_model=list[schemas.RecipeWithAllergens])
def search_safe(exclude: list[str] = Query(default=[]), db: Session = Depends(get_db)):
    recipes = crud.search_safe_recipes(db, exclude)
    result = []
    for r in recipes:
        result.append({"recipe_id": r.recipe_id, "title": r.title, "allergens": []})
    return result
