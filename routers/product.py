from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services import product as product_service

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await product_service.get_all_products(db)


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await product_service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductOut, status_code=201)
async def create_product(payload: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await product_service.create_product(db, payload)


@router.patch("/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, payload: ProductUpdate, db: AsyncSession = Depends(get_db)):
    product = await product_service.update_product(db, product_id, payload)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await product_service.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
