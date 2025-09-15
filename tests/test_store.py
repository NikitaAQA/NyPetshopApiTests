import allure
import jsonschema
import pytest
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_placing_order(self):
        with allure.step("Подготовка данных для размещение заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        with allure.step("Проверка содержимого ответа"):
            assert response_json["id"] == payload["id"], "id заказа не совпадает с ожидаемым"
            assert response_json["petId"] == payload["petId"], "petid заказа не совпадает с ожидаемым"
            assert response_json["quantity"] == payload["quantity"], "количество заказа не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "статус заказа не совпадает с ожидаемым"
            assert response_json["complete"] == payload["complete"], "complete не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_store_by_id(self):
        with allure.step("Отправка запроса на получение id заказа"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")
        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200
        with allure.step("Проверка ,что ответ содержит данные заказа с ID=1"):
            assert response.json()["id"] == 1, "id не совпадает"

    @allure.title("Удаление заказа по ID")
    def test_delete_store_by_id(self):
        with allure.step("Отправка запроса на удаление питомца"):
            response = requests.delete(url=f"{BASE_URL}/store/order/1")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        with allure.step("Отправка запроса на получения информации о удаленном питомце"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_information_nonexistent_store(self):
        with allure.step("Отправка запроса на получения информации о несуществующем заказе"):
             response = requests.get(url=f"{BASE_URL}/store/order/9999")
        with allure.step("Проверка статуса ответа"):
             assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_information_inventory_store(self):
        with allure.step("Отправка запроса на получение информации о инвентаре магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
        with allure.step("Проверка статуса ответа"):
             assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
        with allure.step("Проверка данных инвентаря в ответе"):
            assert response.json() == {"approved":57,"delivered":50}, "Данные ответа не совпали с ожидаемыми"






