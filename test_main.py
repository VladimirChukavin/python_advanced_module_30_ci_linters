from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_index() -> None:
    """
    Тест главной страницы
    :return: None
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}


def test_get_all_recipes() -> None:
    """
    Тест получения списка всех рецептов
    :return: None
    """
    response = client.get("/recipes/")
    assert response.status_code == 200


def test_get_recipe_not_found() -> None:
    """
    Тест получения несуществующего рецепта
    :return: None
    """
    response = client.get("/recipes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Рецепт не найден"}


def test_get_recipe_success() -> None:
    """
    Тест успешного получения рецепта
    :return: None
    """
    response = client.get("/recipes/1")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == 1
    assert data["name"] == "Блины классические"
    assert len(data["ingredients"]) == 7
    assert data["cooking_time"] == 30


def test_create_recipe() -> None:
    """
    Тест создания рецепта с существующими ингредиентами
    :return: None
    """
    recipe_data = {
        "name": "test",
        "description": "test",
        "ingredients": [{"ingredient_id": 1, "quantity": "1"}],
        "cooking_time": 10,
    }
    response = client.post("/recipes/", json=recipe_data)
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "test"
    assert data["description"] == "test"
    assert data["ingredients"] == [{"id": 1, "name": "мука пшеничная"}]
    assert data["cooking_time"] == 10


def test_create_recipe_ingredient_not_found() -> None:
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
    response = client.post("/recipes/", json=recipe_data)
    data = response.json()
    assert response.status_code == 400
    assert "Ингредиент с ID 999 не найден." in data["detail"]


def test_create_recipe_without_ingredients() -> None:
    """
    Тест создания рецепта без ингредиентов
    :return: None
    """
    recipe_data = {
        "name": "test",
        "description": "test",
        "ingredients": [],
        "cooking_time": 10,
    }
    response = client.post("/recipes/", json=recipe_data)
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "test"
    assert data["description"] == "test"
    assert data["ingredients"] == []
    assert data["cooking_time"] == 10


def test_create_recipe_invalid_data() -> None:
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
    response = client.post("/recipes/", json=invalid_data)
    assert response.status_code == 422
