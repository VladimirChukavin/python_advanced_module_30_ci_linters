from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from .base_model import Base


class RecipeDetails(Base):
    """
    Класс модели для организации связей между
    рецептами и ингредиентами (тип связи many-to-many)

    Атрибуты:
        recipe_id: Идентификатор рецепта
        ingredient_id: Идентификатор ингредиента
        quantity: Количество ингредиента
    """

    __tablename__ = "recipe_details"
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"), primary_key=True
    )
    quantity: Mapped[str] = mapped_column(String(100))

    def __repr__(self):
        return (
            f"Recipe details(recipe_id={self.recipe_id}, "
            f"ingredient_id={self.ingredient_id}, "
            f"quantity={self.quantity})"
        )
