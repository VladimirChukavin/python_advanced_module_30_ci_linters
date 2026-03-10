from typing import Any, List

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
    ingredients: List[dict[str, Any]] = []
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


class Ingredients(BaseModel):
    """
    Класс модели для связи ингредиента с рецептом

    Атрибуты:
        ingredient_id: Идентификатор ингредиента
        quantity: Количество ингредиента
    """

    ingredient_id: int
    quantity: str
