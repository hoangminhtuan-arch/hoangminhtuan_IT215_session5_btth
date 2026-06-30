from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
app = FastAPI()

products = [

    {"id": 1, "name": "Keyboard", "price": 500000},

    {"id": 2, "name": "Mouse", "price": 300000}
]
class productCreate(BaseModel):
    id: int
    name: str 
    price: float = Field(..., ge=0.0, description="Phải lớn hơn 0")
    
@app.post("/products/post")
def post_product(product:productCreate):
    found = False
    for i in products:
        if i["id"] == product.id:
            found = True
            break

    if found:
        raise HTTPException(
            status_code=409,
            detail="ID đã tồn tại"
        )

    new_product = {
        "id": product.id,
        "name": product.name,
        "price": product.price
    }
    products.append(new_product)
    return {
        "message": "Thêm mới sản phẩm thành công",
        "data": products
    }

@app.get("/product")
def get_product():
    return {
        "message": "Danh sách sản phẩm",
        "data": products
    }

@app.delete("/product/{product_id}")
def delete_product(product_id: int):
    found_index = None
    for index, product in enumerate(products):
        if product["id"] == product_id:
            found_index = index
            break

    if found_index is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    products.pop(found_index)
    return "Xóa thành công"