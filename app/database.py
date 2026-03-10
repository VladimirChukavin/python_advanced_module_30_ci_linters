from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///recipe_db.db")
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator:
    """
    Функция для создания сессии
    соединения с базой данных
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
