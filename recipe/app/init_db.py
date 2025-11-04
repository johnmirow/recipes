from app.database import Base, engine, SessionLocal
from app import models

def init_db():
    print("🔧 Initializing database...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    default_allergens = [
        ("gluten", "Found in wheat, barley, and rye"),
        ("milk", "Dairy products"),
        ("eggs", "Chicken eggs and derivatives"),
        ("nuts", "Tree nuts such as almonds, hazelnuts, walnuts"),
        ("peanuts", "Groundnuts and peanut butter"),
        ("soy", "Soybeans and soy-based products"),
        ("fish", "All kinds of fish and fish oil"),
        ("shellfish", "Shrimp, crab, lobster, etc."),
    ]

    for name, desc in default_allergens:
        exists = db.query(models.Allergen).filter(models.Allergen.name == name).first()
        if not exists:
            db.add(models.Allergen(name=name, description=desc))

    db.commit()
    db.close()
    print("✅ Database initialized successfully.")

if __name__ == "__main__":
    init_db()
