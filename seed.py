"""
Seed the database with dummy product data.
Usage: python seed.py
"""
import asyncio

from faker import Faker
from sqlalchemy import text

from app.database import AsyncSessionLocal, Base, engine
from app.models.product import Product

fake = Faker()


async def seed():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Clear existing data
        await session.execute(text("TRUNCATE TABLE products RESTART IDENTITY CASCADE"))
        await session.commit()

        products = [
            Product(
                name=fake.unique.catch_phrase(),
                description=fake.sentence(nb_words=12),
                price=round(fake.pyfloat(min_value=5, max_value=500, right_digits=2), 2),
                stock=fake.random_int(min=0, max=200),
                is_active=fake.boolean(chance_of_getting_true=85),
            )
            for _ in range(20)
        ]

        session.add_all(products)
        await session.commit()
        print(f"Seeded {len(products)} products.")


if __name__ == "__main__":
    asyncio.run(seed())
