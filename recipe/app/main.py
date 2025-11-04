from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import users, recipes, allergens, search

app = FastAPI(title="Food Allergy Recipes API")

app.include_router(users.router)
app.include_router(recipes.router)
app.include_router(allergens.router)
app.include_router(search.router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/health")
def health():
    return {"status": "ok"}
