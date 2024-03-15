import pytest
from fastapi import status
from sqlalchemy import select

from src.models import sellers

result = {
    "sellers": [
        {"first_name": "fdhgdh", "last_name": "jdhdj", "email": "xx", "password": "PASSWORD"},
        {"first_name": "xxx", "last_name": "yyy", "email": "zzz", "password": "ttt"},
    ]
}


# Тест на ручку создающую продавца
@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = {"first_name": "xxx", "last_name": "yyy", "email": "zzz", "password": "ttt"},
    response = await async_client.post("/api/v1/sellers/", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    result_data = response.json()
    assert result_data == {
        "id": 1,
        "first_name": "xxx",
        "last_name": "yyy",
        "email": "zzz",
        "password": "ttt"
    }


# Тест на ручку получения списка продавцов
@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):
    seller = sellers.seller(first_name="Pushkin", last_name="Eugeny Onegin", email="x", password="pass")
    seller_2 = sellers.seller(first_name="Lermontov", last_name="Mziri", email="1997", password="xyz")

    db_session.add_all([seller, seller_2])
    await db_session.flush()

    response = await async_client.get("/api/v1/sellers/")

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["sellers"]) == 2  # Опасный паттерн! Если в БД есть данные, то тест упадет

    # Проверяем интерфейс ответа, на который у нас есть контракт.
    assert response.json() == {
        "sellers": [
            {"first_name": "Pushkin", "last_name": "Eugeny Onegin", "email": "x", "password": "pass", "id": seller.id},
            {"first_name": "Lermontov", "last_name": "Mziri", "email": "1997", "password": "xyz", "id": seller_2.id},
        ]
    }


# Тест на ручку получения одного продавца
@pytest.mark.asyncio
async def test_get_single_seller(db_session, async_client):
    # Создаем книги вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    seller = sellers.seller(first_name="Pushkin", last_name="Eugeny Onegin", email="x", password="pass")
    seller_2 = sellers.seller(first_name="Lermontov", last_name="Mziri", email="1997", password="xyz")

    db_session.add_all([seller, seller_2])
    await db_session.flush()

    response = await async_client.get(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_200_OK

    # Проверяем интерфейс ответа, на который у нас есть контракт.
    assert response.json() == {
        "first_name": "Pushkin",
        "last_name": "Eugeny Onegin",
        "email": "x",
        "password": "pass",
        "id": seller.id
    }


# Тест на ручку удаления продавца
@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    # Создаем книги вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    seller = sellers.seller(first_name="Pushkin", last_name="Eugeny Onegin", email="x", password="pass")

    db_session.add(seller)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_sellers = await db_session.execute(select(sellers.seller))
    res = all_sellers.scalars().all()
    assert len(res) == 0


# Тест на ручку обновления книги
@pytest.mark.asyncio
async def test_update_seller(db_session, async_client):
    # Создаем книги вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    seller = sellers.seller(first_name="Pushkin", last_name="Eugeny Onegin", email="x", password="pass")

    db_session.add(seller)
    await db_session.flush()

    response = await async_client.put(
        f"/api/v1/sellers/{seller.id}",
        json={
            "first_name": "t",
            "last_name": "z",
            "email": "x",
            "password": "pass",
            "id": seller.id
        }
    )

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    # Проверяем, что обновились все поля
    res = await db_session.get(sellers.seller, seller.id)
    assert res.first_name == "t"
    assert res.last_name == "z"
    assert res.email == "x"
    assert res.password == "pass"
    assert res.id == seller.id
