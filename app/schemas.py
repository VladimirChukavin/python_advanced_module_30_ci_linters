from typing import List

from pydantic import BaseModel, ConfigDict


class RecipeSimpleOut(BaseModel):
    """
    Класс модели для вывода упрощенной информации о рецепте

    Атрибуты:
        id: Идентификатор рецепта
        name: Название рецепта
        views: Количество просмотров
        cooking_time: Время приготовления
    """

    id: int
    name: str
    views: int
    cooking_time: int

    model_config = ConfigDict(from_attributes=True)


class RecipeFullOut(BaseModel):
    """
    Класс модели для вывода полной информации о рецепте

    Атрибуты:
        id: Идентификатор рецепта
        name: Название рецепта
        description: Описание рецепта
        ingredients: Список ингредиентов
        cooking_time: Время приготовления
    """

    id: int
    name: str
    description: str
    ingredients: List[Ingredient] = []
    cooking_time: int
    views: int = 0

    model_config = ConfigDict(from_attributes=True)


class RecipeIn(BaseModel):
    """
    Класс модели для входных данных создания рецепта

    Атрибуты:
        name: Название рецепта
        description: Описание рецепта
        ingredients: Список ингредиентов
        cooking_time: Время приготовления
    """

    name: str
    description: str
    ingredients: List[Ingredients]
    cooking_time: int


class Ingredient(BaseModel):
    """
    Класс модели для базовой информации об ингредиенте

    Атрибуты:
        id: Идентификатор ингредиента
        name: Название ингредиента
    """

    id: int
    name: str


class Ingredients(BaseModel):
    """
    Класс модели для связи ингредиента с рецептом

    Атрибуты:
        ingredient_id: Идентификатор ингредиента
        quantity: Количество ингредиента
    """

    ingredient_id: int
    quantity: str
