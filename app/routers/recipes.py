from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import schemas
from app.database import get_db_session
from app.models.ingredient_model import Ingredient
from app.models.recipe_details_model import RecipeDetails
from app.models.recipe_model import Recipe

router = APIRouter(
    prefix="/recipes", tags=["recipes"], dependencies=[Depends(get_db_session)]
)
dependency = Depends(get_db_session)


@router.get("/", response_model=List[schemas.RecipeSimpleOut])
async def get_all_recipes(
    session: AsyncSession = dependency,
) -> list[Recipe] | dict:
    """
    Функция-endpoint для получения списка всех рецептов
    :param session: Сессия соединения с базой данных
    :return: Список рецептов
    """
    res = await session.scalars(select(Recipe))
    if res:
        return list(res)
    return {"message": "Ничего не найдено"}


@router.get("/{recipe_id}", response_model=schemas.RecipeFullOut)
async def get_recipe(
    recipe_id: int,
    session: AsyncSession = dependency,
) -> schemas.RecipeFullOut:
    """
    Функция-endpoint для получения детальной
    информации о конкретном рецепте
    :param recipe_id: Идентификатор рецепта
    :param session: Сессия соединения с базой данных
    :return: Информация о рецепте
    """
    stmt = (
        select(Recipe)
        .options(selectinload(Recipe.ingredients))
        .where(Recipe.id == recipe_id)
    )

    process_recipe_data = await session.execute(stmt)
    resulting_recipe = process_recipe_data.scalar_one_or_none()

    if resulting_recipe is None:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    if resulting_recipe:
        resulting_recipe.views += 1
        await session.commit()

    ingredients_data = []
    for ing in resulting_recipe.ingredients:
        ingredients_data.append(
            {
                "id": ing.id,
                "name": ing.name,
            }
        )

    return schemas.RecipeFullOut(
        id=resulting_recipe.id,
        name=resulting_recipe.name,
        description=resulting_recipe.description,
        ingredients=ingredients_data,
        cooking_time=resulting_recipe.cooking_time,
        views=resulting_recipe.views,
    )


@router.post("/", response_model=schemas.RecipeFullOut)
async def create_recipe(
    data: schemas.RecipeIn,
    session: AsyncSession = dependency,
) -> schemas.RecipeFullOut:
    """
    Функция-endpoint для создания
    нового рецепта
    :param data: Данные нового рецепта
    :param session: Сессия соединения с базой данных
    :return: Информация о новом рецепте
    """
    new_recipe = Recipe(
        name=data.name,
        description=data.description,
        cooking_time=data.cooking_time,
    )
    session.add(new_recipe)
    await session.flush()

    ingredients_data = []
    for ingredient_data in data.ingredients:
        ingredient = await session.get(Ingredient, ingredient_data.ingredient_id)

        if not ingredient:
            raise HTTPException(
                status_code=400,
                detail=f"Ингредиент с ID {ingredient_data.ingredient_id} не найден.",
            )

        ingredients_data.append(
            {
                "id": ingredient.id,
                "name": ingredient.name,
            }
        )

        recipe_detail = RecipeDetails(
            recipe_id=new_recipe.id,
            ingredient_id=ingredient_data.ingredient_id,
            quantity=ingredient_data.quantity,
        )
        session.add(recipe_detail)

    await session.commit()
    await session.refresh(new_recipe)

    return schemas.RecipeFullOut(
        id=new_recipe.id,
        name=new_recipe.name,
        description=new_recipe.description,
        ingredients=ingredients_data,
        cooking_time=new_recipe.cooking_time,
    )
