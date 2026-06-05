from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import get_cached, invalidate, set_cached
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

CACHE_KEY_ALL = "products:all"
CACHE_KEY_ONE = "products:{id}"


async def get_all_products(db: AsyncSession) -> list[dict]:
    cached = await get_cached(CACHE_KEY_ALL)
    if cached:
        return cached

    result = await db.execute(select(Product).where(Product.is_active == True))
    products = result.scalars().all()
    data = [_serialize(p) for p in products]

    await set_cached(CACHE_KEY_ALL, data)
    return data


async def get_product(db: AsyncSession, product_id: int) -> dict | None:
    key = CACHE_KEY_ONE.format(id=product_id)
    cached = await get_cached(key)
    if cached:
        return cached

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        return None

    data = _serialize(product)
    await set_cached(key, data)
    return data


async def create_product(db: AsyncSession, payload: ProductCreate) -> dict:
    product = Product(**payload.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    await invalidate(CACHE_KEY_ALL)
    return _serialize(product)


async def update_product(db: AsyncSession, product_id: int, payload: ProductUpdate) -> dict | None:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        return None

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)
    await invalidate(CACHE_KEY_ALL)
    await invalidate(CACHE_KEY_ONE.format(id=product_id))
    return _serialize(product)


async def delete_product(db: AsyncSession, product_id: int) -> bool:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        return False

    await db.delete(product)
    await db.commit()
    await invalidate(CACHE_KEY_ALL)
    await invalidate(CACHE_KEY_ONE.format(id=product_id))
    return True


def _serialize(product: Product) -> dict:
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": float(product.price),
        "stock": product.stock,
        "is_active": product.is_active,
    }
