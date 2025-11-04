from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String(20), default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    recipes = relationship("Recipe", back_populates="author", cascade="all, delete-orphan")

class Recipe(Base):
    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    title = Column(String(150), nullable=False)
    description = Column(Text)
    instructions = Column(Text)
    prep_time = Column(Integer)
    cook_time = Column(Integer)
    servings = Column(Integer)
    source_url = Column(String(500))
    image_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    author = relationship("User", back_populates="recipes")
    recipe_allergens = relationship("RecipeAllergen", back_populates="recipe", cascade="all, delete-orphan")

class Allergen(Base):
    __tablename__ = "allergens"

    allergen_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))

    recipe_links = relationship("RecipeAllergen", back_populates="allergen", cascade="all, delete-orphan")

class RecipeAllergen(Base):
    __tablename__ = "recipe_allergens"

    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id", ondelete="CASCADE"), primary_key=True)
    allergen_id = Column(Integer, ForeignKey("allergens.allergen_id", ondelete="CASCADE"), primary_key=True)

    recipe = relationship("Recipe", back_populates="recipe_allergens")
    allergen = relationship("Allergen", back_populates="recipe_links")

    __table_args__ = (UniqueConstraint('recipe_id', 'allergen_id', name='uq_recipe_allergen'), )
