import allure
import jsonschema
import pytest
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа  не совпал с ожидаемым"
        with allure.step("Проверка текста"):
            assert response.text == "Pet deleted", "Текст не соответствует"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {"id": 9999,
                       "name": "Non-existent Pet",
                       "status": "available"
                       }
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"
        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст не соответствует"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_information_nonexistent_pet(self):
        with allure.step("Отправка запроса на получения информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"
        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст не соответствует"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()
        with allure.step("Проверка статуса ответа и валидация JSON схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)
        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "имя питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"

    @allure.title("Добавление питомца с полными данными")
    def test_add_with_complete_data_pet(self):
        with allure.step("Подготовка данных для создания питомца с  полными данными"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": [
                    "string"
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ],
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца с полными данными"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()
        with allure.step("Проверка статуса ответа и валидация JSON схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)
        with allure.step("Проверка параметров питомца с полными данными в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "имя питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"
            assert response_json['category'] == payload['category'], "категория питомца не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по id")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение id созданного питомца"):
            pet_id = create_pet["id"]
        with allure.step("Отправка запроса на получения информации о питомце по id"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        with allure.step("Проверка ,что ответ содержит данные питомца с указанным ID"):
            assert response.json()["id"] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_information_pet(self, create_pet):
        with allure.step("Получение id созданного питомца"):
            pet_id = create_pet["id"]
        with allure.step("Отправка запроса на обновление данных питомца"):
            payload = {"id": pet_id,
                       "name": "Buddy Updated",
                       "status": "sold"}
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        with allure.step("Проверка ,что ответ содержит обновленные данные питомца"):
            assert response_json['id'] == payload['id']
            assert response_json['name'] == payload['name']
            assert response_json['status'] == payload['status']

    @allure.title("Удаление питомца по id")
    def test_delete_pet_by_id(self, create_pet):
        with allure.step("Получение id созданного питомца"):
            pet_id = create_pet["id"]
        with allure.step("Отправка запроса на удаление питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        with allure.step("Отправка запроса на получения информации о удаленном питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code, expected_type",
        [
            ("available", 200, list),
            ("pending", 200, list),
            ("sold", 200, list),
            (" ", 400, dict),
            ("invalid_status", 400, dict),
            ("", 400, dict)
        ]
    )
    def test_get_pets_by_status(self, status, expected_status_code, expected_type):
        with allure.step(f"Отправка запроса на получение питомцев по статусу '{status}'"):
            response = requests.get(url=f"{BASE_URL}/pet/findByStatus", params={"status": status})
        with allure.step(f"Проверка кода ответа для статуса '{status}'"):
            assert response.status_code == expected_status_code
        with allure.step("Проверка типа ответа"):
            assert isinstance(response.json(), expected_type)


