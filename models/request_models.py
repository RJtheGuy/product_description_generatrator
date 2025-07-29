from pydantic import BaseModel, Field
from typing import List, Optional

class ProductDescriptionRequest(BaseModel):
    product_name: str = Field(..., description="Name of the product")
    raw_text: str = Field(..., description="Raw product information text")
    category: Optional[str] = Field(None, description="Product category")
    target_length: Optional[int] = Field(150, description="Target description length in words")

class ProductDescriptionResponse(BaseModel):
    product_name: str
    generated_description: str
    status: str = "success"
    error_message: Optional[str] = None

class BulkProductDescriptionRequest(BaseModel):
    products: List[ProductDescriptionRequest] = Field(..., description="List of products to process")

class BulkProductDescriptionResponse(BaseModel):
    results: List[ProductDescriptionResponse]
