from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from app.database import get_db_session

from app.models.base_model import Base
from app.models.recipe_model import Recipe
from app.models.ingredient_model import Ingredient
from app.models.recipe_details_model import RecipeDetails

engine_test = create_async_engine("sqlite+aiosqlite:///test.db")
async_session = async_sessionmaker(engine_test, expire_on_commit=False)


async def get_test_db_session() -> AsyncGenerator:
    """
    Функция для создания сессии соединения
    с тестовой базой данных
    :return: Объект сессии
    :raise: Сообщение об ошибке
    """
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


app.dependency_overrides[get_db_session] = get_test_db_session
client = TestClient(app)

ingredients = [
    {"name": "Test ingredient 1"},
    {"name": "Test ingredient 2"},
    {"name": "Test ingredient 3"},
]
recipes = [
    {
        "name": "Test recipe 1",
        "description": "Test recipe description 1",
        "cooking_time": 5,
        "views": 10,
    },
    {
        "name": "Test recipe 2",
        "description": "Test recipe description 2",
        "cooking_time": 8,
        "views": 16,
    },
]
recipe_details = [
    {"recipe_id": 1, "ingredient_id": 1, "quantity": 1},
    {"recipe_id": 1, "ingredient_id": 2, "quantity": 2},
    {"recipe_id": 1, "ingredient_id": 3, "quantity": 3},
    {"recipe_id": 2, "ingredient_id": 3, "quantity": 4},
    {"recipe_id": 2, "ingredient_id": 2, "quantity": 5},
]


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_test_db():
    """
    Функция для конфигурации тестовой базы данных
    """
    async with engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await connection.execute(insert(Ingredient), ingredients)
        await connection.execute(insert(Recipe), recipes)
        await connection.execute(insert(RecipeDetails), recipe_details)
    yield
    async with engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def async_test_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Функция для создания тестового клиента
    :return: Тестовый клиент
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
