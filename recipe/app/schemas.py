from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List

# Users
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    user_id: int
    role: str
    class Config:
        orm_mode = True

# Recipes
class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    servings: Optional[int] = None
    source_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(RecipeBase):
    pass

class RecipeResponse(RecipeBase):
    recipe_id: int
    author: str
    class Config:
        orm_mode = True

# Allergens
class AllergenBase(BaseModel):
    name: str
    description: Optional[str] = None

class AllergenCreate(AllergenBase):
    pass

class AllergenResponse(AllergenBase):
    allergen_id: int
    class Config:
        orm_mode = True

class RecipeWithAllergens(BaseModel):
    recipe_id: int
    title: str
    allergens: List[str] = []
