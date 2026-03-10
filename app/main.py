from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy import inspect

from app.database import engine, get_db_session
from app.models.base_model import Base
from app.routers import recipes


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


app = FastAPI(lifespan=lifespan, dependencies=[Depends(get_db_session)])
app.include_router(recipes.router)


@app.get("/", tags=["index"])
def index() -> dict:
    """
    Функция-endpoint для первой страницы
    :return: Приветствие
    """
    return {"message": "Wellcome to our recipes storage!!!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
