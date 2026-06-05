from pydantic import BaseModel, ConfigDict, field_validator


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int = 0
    is_active: bool = True

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name cannot be empty")
        return v

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError("price must be positive")
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    is_active: bool | None = None


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
