from typing import List

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base


class Recipe(Base):
    """
    Класс модели рецепта

    Атрибуты:
        id: Идентификатор рецепта
        name: Название рецепта
        description: Описание рецепта
        ingredients: Ингредиенты
        cooking_time: Время приготовления
        views: Просмотры
    """

    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(
        Text, default="Описание рецепта будет добавлено позже."
    )
    ingredients: Mapped[List["Ingredient"]] = relationship(
        "Ingredient",
        back_populates="recipes",
        secondary="recipe_details",
    )
    cooking_time: Mapped[int] = mapped_column(default=0)
    views: Mapped[int] = mapped_column(default=0)

    def __repr__(self):
        return (
            f"Recipe(name={self.name}, "
            f"description={self.description}, "
            f"ingredients={self.ingredients}, "
            f"cooking_time={self.cooking_time}, "
            f"views={self.views})"
        )
