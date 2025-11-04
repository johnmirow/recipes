from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal
from app.dependencies import get_current_user

router = APIRouter(prefix="/recipes", tags=["Recipes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.RecipeResponse)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_recipe = crud.create_recipe(db, recipe, current_user.user_id)
    return {**new_recipe.__dict__, "author": current_user.username}

@router.get("/", response_model=list[schemas.RecipeResponse])
def list_recipes(db: Session = Depends(get_db)):
    recipes = crud.get_recipes(db)
    result = []
    for r in recipes:
        result.append({
            "recipe_id": r.recipe_id,
            "title": r.title,
            "description": r.description,
            "instructions": r.instructions,
            "prep_time": r.prep_time,
            "cook_time": r.cook_time,
            "servings": r.servings,
            "source_url": r.source_url,
            "image_url": r.image_url,
            "author": getattr(r.author, "username", "unknown")
        })
    return result

@router.get("/me", response_model=list[schemas.RecipeResponse])
def my_recipes(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    recipes = crud.get_my_recipes(db, current_user.user_id)
    return [{
        "recipe_id": r.recipe_id,
        "title": r.title,
        "description": r.description,
        "instructions": r.instructions,
        "prep_time": r.prep_time,
        "cook_time": r.cook_time,
        "servings": r.servings,
        "source_url": r.source_url,
        "image_url": r.image_url,
        "author": current_user.username
    } for r in recipes]

@router.put("/{recipe_id}", response_model=schemas.RecipeResponse)
def update_recipe(recipe_id: int, data: schemas.RecipeUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    updated = crud.update_recipe(db, recipe_id, data, current_user.user_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Recipe not found or not owned by user")
    return {**updated.__dict__, "author": current_user.username}

@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    deleted = crud.delete_recipe(db, recipe_id, current_user.user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Recipe not found or not owned by user")
    return {"detail": "Recipe deleted"}
