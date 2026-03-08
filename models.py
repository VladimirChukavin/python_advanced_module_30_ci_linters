from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey


class Base(DeclarativeBase):
    pass


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
