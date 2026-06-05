from faker import Faker
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product

fake = Faker()

SEED_COUNT = 20


async def seed_products(session: AsyncSession) -> None:
    count = await session.scalar(select(func.count()).select_from(Product))
    if count and count > 0:
        return

    products = [
        Product(
            name=fake.unique.catch_phrase(),
            description=fake.sentence(nb_words=12),
            price=round(fake.pyfloat(min_value=5, max_value=500, right_digits=2), 2),
            stock=fake.random_int(min=0, max=200),
            is_active=fake.boolean(chance_of_getting_true=85),
        )
        for _ in range(SEED_COUNT)
    ]

    session.add_all(products)
    await session.commit()
    print(f"[seed] inserted {len(products)} products.")


async def run_seeds(session: AsyncSession) -> None:
    await seed_products(session)
