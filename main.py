from typing import List
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, inspect
from sqlalchemy.orm import selectinload

import schemas
from models import (
    Base,
    Recipe,
    Ingredient,
    RecipeDetails,
)
from database import engine, get_db_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(init_db)
    yield
    await engine.dispose()


def init_db(connection) -> None:
    """
    Функция для проверки существования базы данных
    :param connection: Объект соединения с базой данных
    :return: None
    """
    inspector = inspect(connection)
    tables = ["recipes", "ingredients", "recipe_details"]
    if not all(inspector.has_table(table) for table in tables):
        Base.metadata.create_all(connection)
        print("База данных создана.")
    else:
        print("База данных уже существует.")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def index() -> dict:
    """
    Функция-endpoint для первой страницы
    :return: Приветствие
    """
    return {"hello": "world"}


@app.get("/recipes/", response_model=List[schemas.RecipeSimpleOut])
async def get_all_recipes(
    session: AsyncSession = Depends(get_db_session),
) -> list[Recipe]:
    """
    Функция-endpoint для получения списка всех рецептов
    :param session: Сессия соединения с базой данных
    :return: Список рецептов
    """
    res = await session.scalars(select(Recipe))
    return list(res)


@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeFullOut)
async def get_recipe(
    recipe_id: int, session: AsyncSession = Depends(get_db_session)
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
    )


@app.post("/recipes/", response_model=schemas.RecipeFullOut)
async def create_recipe(
    data: schemas.RecipeIn,
    session: AsyncSession = Depends(get_db_session),
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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
