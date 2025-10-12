from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    price: float
    tags: list[str] = Field(default_factory=list)

@app.post("/product")
def add_product(product: Product):
    return {'product': product.dict()}
