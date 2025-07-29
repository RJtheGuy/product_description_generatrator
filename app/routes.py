from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
import logging
from app.models.request_models import (
    ProductDescriptionRequest, 
    ProductDescriptionResponse,
    BulkProductDescriptionRequest,
    BulkProductDescriptionResponse
)
from app.services.generate import ProductDescriptionGenerator

logger = logging.getLogger(__name__)
router = APIRouter()

def get_generator(request: Request) -> ProductDescriptionGenerator:
    """Dependency to get the product description generator"""
    return ProductDescriptionGenerator(request.app.state.ollama_client)

@router.post("/generate-description", response_model=ProductDescriptionResponse)
async def generate_single_description(
    request: ProductDescriptionRequest,
    generator: ProductDescriptionGenerator = Depends(get_generator)
):
    """Generate a single product description"""
    try:
        logger.info(f"Generating description for product: {request.product_name}")
        
        description = await generator.generate_description(
            product_name=request.product_name,
            raw_text=request.raw_text,
            category=request.category,
            target_length=request.target_length
        )
        
        return ProductDescriptionResponse(
            product_name=request.product_name,
            generated_description=description,
            status="success"
        )
    
    except Exception as e:
        logger.error(f"Error generating description: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@router.post("/generate-bulk", response_model=BulkProductDescriptionResponse)
async def generate_bulk_descriptions(
    request: BulkProductDescriptionRequest,
    generator: ProductDescriptionGenerator = Depends(get_generator)
):
    """Generate multiple product descriptions"""
    try:
        logger.info(f"Generating bulk descriptions for {len(request.products)} products")
        
        results = []
        for product in request.products:
            try:
                description = await generator.generate_description(
                    product_name=product.product_name,
                    raw_text=product.raw_text,
                    category=product.category,
                    target_length=product.target_length
                )
                results.append(ProductDescriptionResponse(
                    product_name=product.product_name,
                    generated_description=description,
                    status="success"
                ))
            except Exception as e:
                logger.error(f"Error generating description for {product.product_name}: {str(e)}")
                results.append(ProductDescriptionResponse(
                    product_name=product.product_name,
                    generated_description="",
                    status="error",
                    error_message=str(e)
                ))
        
        return BulkProductDescriptionResponse(results=results)
    
    except Exception as e:
        logger.error(f"Error in bulk generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Bulk generation failed: {str(e)}")
