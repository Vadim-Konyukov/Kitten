import pytest
from pytest_assert_utils import util
from model_bakery import baker
from rest_framework.test import APIClient
from REST_API.models import Breed, Kitten
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_get_breeds(client):
    breed_count = 5
    baker.make(Breed, _quantity=breed_count)
    response = client.get("/api/breeds/")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": util.Any(int),
            "name": util.Any(str)
        }
        for _ in range (breed_count)
    ]


@pytest.mark.django_db
def test_get_kittens(client):
    # Создаем пользователя и породу
    user = baker.make(User)
    breed = baker.make(Breed)

    # Логиним пользователя и получаем JWT токен
    client = APIClient()  # используем APIClient для авторизационных запросов
    client.force_authenticate(user=user)

    # Создаем 3 котят от этого пользователя
    kitten_count = 3
    baker.make(Kitten, breed=breed, owner=user, _quantity=kitten_count)

    # Выполняем запрос на получение списка котят
    response = client.get("/api/kittens/")

    # Проверяем статус ответа и содержимое
    assert response.status_code == 200
    print(response.json())
    assert response.json() == [
        {
            "id": util.Any(int),
            "name": util.Any(str),
            "color": util.Any(str),
            "age": util.Any(int),
            "breed": util.Any(str),
            "description": util.Any(str),
            "average_rating": util.Any(float),
            "owner": {
                "id": user.id,
                "username": user.username
            },
            "birth_date": util.Any(str),
        }
        for _ in range(kitten_count)
    ]
