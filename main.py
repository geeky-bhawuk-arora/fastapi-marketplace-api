from fastapi import Depends, FastAPI
from models import Product
from sqlalchemy.orm import Session
import database_models
from database import SessionLocal, engine
from database_models import Base 

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello Bhawuk !"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

products = [
    Product(id=1, name="Laptop", description="High performance laptop", price=75000.0, quantity=10),
    Product(id=2, name="Phone", description="Smartphone with good camera", price=25000.0, quantity=25),
    Product(id=3, name="Headphones", description="Noise cancelling headphones", price=5000.0, quantity=50),
    Product(id=4, name="Keyboard", description="Mechanical keyboard", price=3000.0, quantity=15),
    Product(id=5, name="Monitor", description="24-inch LED monitor", price=12000.0, quantity=20),
]



def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    existing_count = db.query(database_models.Product).count()

    if existing_count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
        print("Database initialized with sample products.")
        
    db.close()

init_db()    


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products   


@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    return {"message": "Product not found!"}


@app.post("/product")
def add_product(product: Product):
    products.append(product)
    return products


@app.put("/product")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return {"message": "Product updated succesfully !"}
    return {"message": "No product found !"}


@app.delete("/product")
def delete_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return {"message": "Product deleted succesfully !"}
    return {"message": "No product found !"}

