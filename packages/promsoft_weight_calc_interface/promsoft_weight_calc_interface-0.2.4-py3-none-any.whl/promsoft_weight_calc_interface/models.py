from pydantic import BaseModel, validator, root_validator, Field, PositiveInt


V2_RESULT_DICT = {
    "detail": "",
    "dimensions": {},
    "items_sizes": {}
}


class Entry(BaseModel):
    """
    Класс для входных данных о товарах
    """

    id: int = Field(
        default=0,
        title="The idgood of item.",
        description="Needs to be an integer positive number.",
        example=10004,
    )
    cnt: int = Field(
        default=0,
        title="The quantity of items.",
        description="Needs to be an integer positive number.",
        example=2,
    )

    @validator("id")
    def check_id(cls, v):
        if v < 1:
            raise ValueError("id must be > 0")
        return v

    @validator("cnt")
    def check_cnt(cls, v):
        if v < 0:
            raise ValueError("cnt must be >= 0")
        return v


class ComplEntry(BaseModel):
    """
        Класс для входных данных о товарах с возможностью возврата изначальных размеров
    """

    items: list[Entry] = []
    return_sizes_goods: bool = Field(
        default=False,
        title="True if you need to see the initial sizes of all items which ids you wrote in 'id' fields.",
        description="Can only be True or False.",
    )

    class Config:
        schema_extra = {
            "example": {"items": [{"id": 10004, "cnt": 2}], "return_sizes_goods": True}
        }

    @validator("items")
    def check_items(cls, v):
        if v is None:
            raise ValueError("Entry is empty")
        if len(v) == 0:
            raise ValueError("No items entered")
        return v


class ZakazEntry(BaseModel):
    """
        Класс для входных данных о заказе
    """
    idzakaz: PositiveInt|None = Field(
        default=None,
        title="The idzakaz on the site",
        description="Needs to be an integer positive number.",
        example=2380955,
    )
    idmonopolia: PositiveInt|None = Field(
        default=None,
        title="The idzakaz in the monopolia",
        description="Needs to be an integer positive number.",
        example=816121,
    )
    from_monopolia: bool = Field(
        default = False,
        title = "Заказ из monopolia",
        description = "Состав заказа брать не из ep_zakaz_parts, а из ep_zakaz_monopolia_stat",
     )

    @root_validator()
    def check_id_zakaz(cls, values):
        if not values.get('idzakaz') and not values.get('idmonopolia'):
            raise ValueError('idzakaz and idmonopolia is empty')
        if values.get('from_monopolia') and not values.get('idmonopolia'):
            raise ValueError('from_monopolia есть, а idmonopolia нет')
        return values
