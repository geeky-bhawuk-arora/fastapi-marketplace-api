from fastapi import FastAPI
from models import Product

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello Bhawuk !"}

products = [
    Product(id=1, name="Laptop", description="High performance laptop", price=75000.0, quantity=10),
    Product(id=2, name="Phone", description="Smartphone with good camera", price=25000.0, quantity=25),
    Product(id=3, name="Headphones", description="Noise cancelling headphones", price=5000.0, quantity=50),
    Product(id=4, name="Keyboard", description="Mechanical keyboard", price=3000.0, quantity=15),
    Product(id=5, name="Monitor", description="24-inch LED monitor", price=12000.0, quantity=20),
]


@app.get("/products")
def get_all_products():
    return products   


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
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return {"message": "Product deleted succesfully !"}
    return {"message": "No product found !"}

