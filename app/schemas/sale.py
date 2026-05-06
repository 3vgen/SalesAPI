from pydantic import BaseModel, field_validator, model_validator


class SaleItem(BaseModel):
    dish: str
    cost_price: float
    selling_price: float
    quantity: int

    @field_validator("cost_price", "selling_price")
    @classmethod
    def must_be_positive(cls, v: float, info) -> float:
        if v <= 0:
            raise ValueError(f"{info.field_name} должна быть больше нуля")
        return v

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Количество должно быть больше нуля")
        return v

    @model_validator(mode="after")
    def cost_below_selling(self) -> "SaleItem":
        if self.cost_price >= self.selling_price:
            raise ValueError(
                f"Себестоимость ({self.cost_price}) должна быть меньше цены продажи ({self.selling_price})"
            )
        return self

    # Вычисляемые поля 
    @property
    def margin_percent(self) -> float:
        return round((self.selling_price - self.cost_price) / self.selling_price * 100, 2)

    @property
    def revenue(self) -> float:
        return round(self.selling_price * self.quantity, 2)

    @property
    def profit(self) -> float:
        return round((self.selling_price - self.cost_price) * self.quantity, 2)


class SalesRequest(BaseModel):
    sales: list[SaleItem]

    @field_validator("sales")
    @classmethod
    def not_empty(cls, v: list) -> list:
        if not v:
            raise ValueError("Список продаж не может быть пустым")
        return v


class DishResult(BaseModel):
    dish: str
    margin_percent: float
    revenue: float
    profit: float


class SalesResponse(BaseModel):
    top_margin_dishes: list[DishResult]
    loss_making: list[DishResult]
    total_revenue: float
    total_margin: float
    suggestions: list[str]
