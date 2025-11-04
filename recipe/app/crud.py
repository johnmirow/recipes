from sqlalchemy.orm import Session
from app import models, schemas

# Recipes
def create_recipe(db: Session, recipe: schemas.RecipeCreate, user_id: int):
    new_recipe = models.Recipe(**recipe.dict(exclude_unset=True), user_id=user_id)
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

def get_recipes(db: Session):
    return db.query(models.Recipe).all()

def get_my_recipes(db: Session, user_id: int):
    return db.query(models.Recipe).filter(models.Recipe.user_id == user_id).all()

def update_recipe(db: Session, recipe_id: int, data: schemas.RecipeUpdate, user_id: int):
    recipe = db.query(models.Recipe).filter(
        models.Recipe.recipe_id == recipe_id,
        models.Recipe.user_id == user_id
    ).first()
    if recipe:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(recipe, key, value)
        db.commit()
        db.refresh(recipe)
    return recipe

def delete_recipe(db: Session, recipe_id: int, user_id: int):
    recipe = db.query(models.Recipe).filter(
        models.Recipe.recipe_id == recipe_id,
        models.Recipe.user_id == user_id
    ).first()
    if recipe:
        db.delete(recipe)
        db.commit()
    return recipe

# Allergens
def create_allergen(db: Session, name: str, description: str | None = None):
    allergen = models.Allergen(name=name, description=description)
    db.add(allergen)
    db.commit()
    db.refresh(allergen)
    return allergen

def list_allergens(db: Session):
    return db.query(models.Allergen).order_by(models.Allergen.name).all()

def link_recipe_allergens(db: Session, recipe_id: int, allergen_ids: list[int]):
    for allergen_id in allergen_ids:
        link = models.RecipeAllergen(recipe_id=recipe_id, allergen_id=allergen_id)
        db.add(link)
    db.commit()

def search_safe_recipes(db: Session, excluded_allergens: list[str]):
    subq = (
        db.query(models.RecipeAllergen.recipe_id)
        .join(models.Allergen, models.RecipeAllergen.allergen_id == models.Allergen.allergen_id)
        .filter(models.Allergen.name.in_(excluded_allergens))
        .subquery()
    )
    return db.query(models.Recipe).filter(~models.Recipe.recipe_id.in_(subq)).all()
