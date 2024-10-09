
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
            "breed":  {
                "id": util.Any(int),
                "name": util.Any(str),
        },
            "description": util.Any(str),
            "average_rating": util.Any(float),
            "owner": util.Any(int),
            "birth_date": util.Any(str),
        }
        for _ in range(kitten_count)
    ]


@pytest.mark.django_db
def test_get_kitten_by_breeds(client):
    # тест на получение списка котят определенной породы по фильтру

    user = baker.make(User)
    breed_1 = baker.make(Breed)
    breed_2 = baker.make(Breed)

    # Логиним пользователя и получаем JWT токен
    client = APIClient()  # используем APIClient для авторизационных запросов
    client.force_authenticate(user=user)

    # Создаем котят для каждой породы
    kitten_breed1 = baker.make(Kitten, breed=breed_1, owner=user)
    kitten_breed2 = baker.make(Kitten, breed=breed_2, owner=user)

    # Выполняем запрос на получение котят первой породы
    response = client.get('/api/kittens/', query_params={"breed": breed_1.id})

    # Проверяем статус ответа и содержимое
    assert response.status_code == 200

    # Преобразуем JSON-ответ
    response_data = response.json()

    # Выводим структуру ответа для отладки
    print("Response data:", response_data)

    # Проверяем, что в ответе вернулись только котята первой породы
    for kitten in response_data:
        print(f"Kitten Breed ID: {kitten['breed']['id']}, Expected Breed ID: {breed_1.id}")
        assert kitten['breed']['id'] == breed_1.id
    assert response.json() == [
            {
                "id": util.Any(int),
                "name": util.Any(str),
                "color": util.Any(str),
                "age": util.Any(int),
                "breed": {
                    "id": breed_1.id,
                    "name": breed_1.name
                },
                "description": util.Any(str),
                "average_rating": util.Any(float),
                "owner": util.Any(int),
                "birth_date": util.Any(str),
            }
        ]
@pytest.mark.django_db
def test_get_kitten_detail(client):
    # Получение подробной информации о котенке

    # Создаем пользователя и породу
    user = baker.make(User)
    breed = baker.make(Breed)

    # Логиним пользователя и получаем JWT токен
    client = APIClient()  # используем APIClient для авторизационных запросов
    client.force_authenticate(user=user)

    # Создаем 2 котят от этого пользователя
    kitten_1 = baker.make(Kitten, breed=breed, owner=user)
    kitten_2 = baker.make(Kitten, breed=breed, owner=user)

    # Выполняем запрос на получение детальной информации котенка
    response = client.get(f'/api/kittens/{kitten_1.id}/')

    # Преобразуем JSON-ответ
    response_data = response.json()

    print("Response data:", response_data)

    # Проверяем статус ответа и содержимое
    assert response.status_code == 200

    # Проверяем, что в ответе вернулся только первый котенок
    assert response_data['id'] == kitten_1.id
    assert response.json() == {

            "id": kitten_1.id,
            "name": kitten_1.name,
            "breed": {
                "id": util.Any(int),
                "name": util.Any(str),
            },
            "color": util.Any(str),
            "birth_date": util.Any(str),
            "age": util.Any(int),
            "description": util.Any(str),
            "owner": util.Any(int),
            "average_rating": util.Any(float),
        }


@pytest.mark.django_db
def test_create_kitten(client):
    #  Добавление информации о котенке

    # Создаем пользователя и породу
    user = baker.make(User)
    breed = baker.make(Breed)

    # Логиним пользователя и получаем JWT токен
    client = APIClient()  # используем APIClient для авторизационных запросов
    client.force_authenticate(user=user)

    # Данные для нового котенка
    kitten_data = {
        'name': 'Test Kitten',
        'color': 'Black',
        'birth_date': '2024-10-08',
        'description': 'A lovely black kitten.',
        'breed_id': breed.id,
        'owner': user.id,
    }

    # Выполняем запрос на создание котенка
    response = client.post('/api/kittens/', data=kitten_data)

    # Проверяем статус ответа
    assert response.status_code == 201  # Ожидаем статус 201 Created

    # Проверяем, что котенок был создан в базе данных
    kitten = Kitten.objects.get(id=response.json()['id'])

    # Проверяем, что все поля были сохранены правильно
    assert kitten.name == kitten_data['name']
    assert kitten.color == kitten_data['color']
    assert kitten.birth_date.isoformat() == kitten_data['birth_date']  # Проверяем формат даты
    assert kitten.description == kitten_data['description']
    assert kitten.breed.id == kitten_data['breed_id']  # Проверяем, что порода связана с котенком
    assert kitten.owner == user  # Проверяем, что владелец котенка соответствует текущему пользователю

    assert response.json() == {
        'id': kitten.id,
        'name': kitten.name,
        'color': kitten.color,
        'birth_date':  kitten.birth_date.isoformat(),
        'description': kitten.description,
        'breed': {
            'id': kitten.breed.id,
            'name': kitten.breed.name,
        },
        'age': kitten.age,
        'owner': kitten.owner.id,
        "average_rating": util.Any(float),
    }


@pytest.mark.django_db
def test_update_kitten(client):
    # Создаем пользователя и породу
    user = baker.make(User)
    breed = baker.make(Breed)

    # Логиним пользователя и получаем JWT токен
    client = APIClient()  # используем APIClient для авторизационных запросов
    client.force_authenticate(user=user)

    # Создаем котенка от этого пользователя
    kitten = baker.make(Kitten, breed=breed, owner=user)

    # Данные для обновления котенка
    updated_kitten_data = {
        'name': 'Updated Kitten',
        'color': 'New Color',
        'birth_date': '2024-10-09',
        'description': 'Updated description.',
        'breed_id': breed.id,  # Убедитесь, что используете правильный ID породы
    }

    # Выполняем запрос на обновление информации о котенке
    response = client.put(f'/api/kittens/{kitten.id}/', data=updated_kitten_data, format='json')

    # Проверяем статус ответа
    assert response.status_code == 200

    # Преобразуем JSON-ответ
    response_data = response.json()

    # Проверяем, что данные были успешно обновлены
    assert response_data['id'] == kitten.id
    assert response_data['name'] == updated_kitten_data['name']
    assert response_data['color'] == updated_kitten_data['color']
    assert response_data['description'] == updated_kitten_data['description']
    assert response_data['birth_date'] == updated_kitten_data['birth_date']
    assert response_data['breed']['id'] == breed.id

    assert response.json() == {
        'id': kitten.id,
        'name': updated_kitten_data['name'],
        'color': updated_kitten_data['color'],
        'birth_date': updated_kitten_data['birth_date'],
        'description': updated_kitten_data['description'],
        'breed': {
            'id': breed.id,
            'name': breed.name,
        },
        'age': kitten.age,
        'owner': kitten.owner.id,
        "average_rating": util.Any(float),
    }


@pytest.mark.django_db
def test_delete_kitten(client):
    # Создаем пользователя и породу
    user = baker.make(User)
    breed = baker.make(Breed)

    # Логиним пользователя и получаем JWT токен
    client = APIClient()  # используем APIClient для авторизационных запросов
    client.force_authenticate(user=user)

    # Создаем котенка от этого пользователя
    kitten = baker.make(Kitten, breed=breed, owner=user)

    # Выполняем запрос на удаление котенка
    response = client.delete(f'/api/kittens/{kitten.id}/')

    # Проверяем статус ответа
    assert response.status_code == 204  # 204 означает, что удаление прошло успешно и ответа нет

    # Проверяем, что котенок был удален
    response_after_deletion = client.get(f'/api/kittens/{kitten.id}/')

    # После удаления, должен быть возвращен статус 404
    assert response_after_deletion.status_code == 404


@pytest.mark.django_db
def test_jwt_auth():
    # Создаем пользователя
    user = baker.make(User, username='testuser')
    user.set_password('password123')
    user.save()

    client = APIClient()

    # Запрос на получение токена
    response = client.post('/api/token/', {
        'username': 'testuser',
        'password': 'password123'
    })

    # Проверяем, что токен был успешно получен
    assert response.status_code == 200
    tokens = response.json()
    assert 'access' in tokens
    assert 'refresh' in tokens

    access_token = tokens['access']

    # Используем access токен для доступа к защищенному ресурсу
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    protected_response = client.get('/api/protected/')  # это пример защищенного маршрута

    # Проверяем, что защищенный ресурс доступен
    assert protected_response.status_code == 200