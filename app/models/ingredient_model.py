from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from .base_model import Base


class Ingredient(Base):
    """
    Класс модели ингредиента

    Атрибуты:
        id: Идентификатор ингредиента
        name: Название ингредиента
        recipes: Рецепты, где используется
    """

    __tablename__ = "ingredients"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    recipes: Mapped[List["Recipe"]] = relationship(
        "Recipe",
        back_populates="ingredients",
        secondary="recipe_details",
    )

    def __repr__(self):
        return f"Ingredient(name={self.name}, recipes={self.recipes})"
