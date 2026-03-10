import pytest


@pytest.mark.asyncio
async def test_index(async_test_client) -> None:
    """
    Тест главной страницы
    :return: None
    """
    response = await async_test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Wellcome to our recipes storage!!!"}


@pytest.mark.asyncio
async def test_get_all_recipes(async_test_client) -> None:
    """
    Тест получения списка всех рецептов
    :return: None
    """
    response = await async_test_client.get("/recipes/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_recipe_not_found(async_test_client) -> None:
    """
    Тест получения несуществующего рецепта
    :return: None
    """
    response = await async_test_client.get("/recipes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Рецепт не найден"}


@pytest.mark.asyncio
async def test_get_recipe_success(async_test_client) -> None:
    """
    Тест успешного получения рецепта
    :return: None
    """
    response = await async_test_client.get("/recipes/1")
    data = response.json()
    views = data["views"]
    assert response.status_code == 200
    assert data["id"] == 1
    assert data["name"] == "Test recipe 1"
    assert data["description"] == "Test recipe description 1"
    assert len(data["ingredients"]) == 3
    assert data["cooking_time"] == 5
    assert data["views"] == views


@pytest.mark.asyncio
async def test_create_recipe(async_test_client) -> None:
    """
    Тест создания рецепта с существующими ингредиентами
    :return: None
    """
    recipe_data = {
        "name": "Test new recipe",
        "description": "Test new recipe description",
        "ingredients": [{"ingredient_id": 1, "quantity": "1"}],
        "cooking_time": 15,
    }
    response = await async_test_client.post("/recipes/", json=recipe_data)
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Test new recipe"
    assert data["description"] == "Test new recipe description"
    assert data["ingredients"] == [{"id": 1, "name": "Test ingredient 1"}]
    assert data["cooking_time"] == 15


@pytest.mark.asyncio
async def test_create_recipe_ingredient_not_found(async_test_client) -> None:
    """
    Тест создания рецепта с несуществующим ингредиентом
    :return: None
    """
    recipe_data = {
        "name": "test",
        "description": "test",
        "ingredients": [{"ingredient_id": 999, "quantity": "1"}],
        "cooking_time": 10,
    }
    response = await async_test_client.post("/recipes/", json=recipe_data)
    data = response.json()
    assert response.status_code == 400
    assert "Ингредиент с ID 999 не найден." in data["detail"]


@pytest.mark.asyncio
async def test_create_recipe_without_ingredients(async_test_client) -> None:
    """
    Тест создания рецепта без ингредиентов
    :return: None
    """
    recipe_data = {
        "name": "test",
        "description": "test",
        "ingredients": [],
        "cooking_time": 20,
    }
    response = await async_test_client.post("/recipes/", json=recipe_data)
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "test"
    assert data["description"] == "test"
    assert data["ingredients"] == []
    assert data["cooking_time"] == 20


@pytest.mark.asyncio
async def test_create_recipe_invalid_data(async_test_client) -> None:
    """
    Тест создания рецепта с невалидными данными
    :return:
    """
    invalid_data = {
        "name": "",
        "description": "test" * 1000,
        "ingredients": [{"ingredient_id": 1}],
        "cooking_time": -10,
    }
    response = await async_test_client.post("/recipes/", json=invalid_data)
    assert response.status_code == 422
