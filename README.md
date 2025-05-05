# my_messenger
Sample code for a small API that can run a whole messenger 

# Описание
Этот репозиторий содержит код бэкенда для приложения типа мессенджер.
На rest api есть точка для запроса истории сообщений по пути `"/history/{chat_id:UUID}"`, где в качестве chat_id нужно передать идентификатор чата.

При подключении на вебсокет можно:
- Залогиниться
- Отправить сообщение
- Создать групповой чат
- Получить уведомление о прочитанных сообщениях

Тестовые данные можно увидеть в [файле](fake_data.json)

Схему моделей базы данных можно увидеть в [файле plantUML](docs/models.puml)

# Команды

> Перед применением команд необходимо заполнить .env файл из [примера](example.env)

Чтобы запустить контейнер с проверками тестов, необходимо использовать следующее:
```bash
sh compose_tests.sh
```
Шаги процесса в команде:
1. Билд образа приложения
2. Запуск docker compose
3. Миграция
4. Запуск приложения в контейнере
5. Запуск тестов в контейнере с приложением
6. Выход с кодом завершения тестов

Чтобы запустить контейнер в режиме разработки с созданием тестовых данных:
```bash
sh compose_tests.sh
```
Шаги процесса в команде:
1. Билд образа приложения
2. Запуск docker compose
3. Миграция
4. Загрузка тестовых данных
5. Запуск приложения в контейнере
6. Ожидание

## Дополнительные команды проекта:

Установить зависимости:
```bash
pip install poetry
poetry install
```

Накатить миграции:
```bash
alembic upgrade head
```

Запустить приложение в режиме разработки:
```bash
fastapi dev app/main.py
```

Команда для загрузки данных в базу:
```bash
poetry run populate
```

Команда для создания данных в json файл:
```bash
poetry run create_json
```

# Примеры запросов

> Запросы в разделе отправляются на хост `localhost:8000`

Интерактивная дока OpenAPI

`http://localhost:8000/docs`

Запрос истории сообщений чата
```bash
curl -X 'GET' \
  'http://localhost:8000/history/27784f95-d0e0-478d-b224-f718fe2da52c?limit=10&offset=0' \
  -H 'accept: application/json'
```

Подключение к вебсокету (Принимает и отправляет в формате json)
```bash
wscat -c ws://localhost:8000/ws
```

Форматы сообщений представлены далее

# Протокол месседжинга
Вебсокет подключение принимается по пути `/ws`

Формат принимаемых сообщений:
- Залогиниться
```json
{
    "email": "nicholecarroll@example.com",
    "password": "!0Wtg"
}
```
- Отправить сообщение
```json
{
    "client_id": "dadf4d3c-ccf8-443d-ad7d-7dafca692fbd",
    "sender_id": "d61d47bb-2cd2-4c1d-8975-938263836086",
    "chat_id": "27784f95-d0e0-478d-b224-f718fe2da52c",
    "timestamp": "2025-05-04 04:45:50+00:00",
    "text": "Congress information message. Information recognize face. Form according toward evidence quite everybody."
}
```
- Создать групповой чат
```json
{
    "name": "Car.",
    "users": [
      "d61d47bb-2cd2-4c1d-8975-938263836086",
      "599e25c1-693d-4620-9abf-fde1dda5d426",
      "ef642621-024a-4db6-9ab2-5304c6e6221d"
    ]
}
```
- Сообщение прочитано
```json
{
    "message_id": "b0b47faf-fafc-4447-b983-a3cc88a4eb5f"
}
```


Формат отправляемых сообщений:
- Уведомления:
  - Общий формат

```json
{
  "type": "", // Может принимать значение "error" | "auth_success" | "message_seen"
  "detail": null // Содержит null или объект 
}
```
  - Успешная регистрация
```json
{
  "type": "auth_success",
  "detail": null
}
```
  - Сообщение прочитано всеми участниками чата
```json
{
  "type": "message_seen",
  "detail": null // Содержит формат из "Входящее сообщение"
}
```
  - Ошибка
```json
{
  "type": "error",
  "detail": {} // Содержит детали ошибки
}
```
- Входящее сообщение
```json
{
    "id": "9d5a44c4-3115-477b-83da-f7c8b4f34896",
    "sender_id": "d61d47bb-2cd2-4c1d-8975-938263836086",
    "chat_id": "27784f95-d0e0-478d-b224-f718fe2da52c",
    "timestamp": "2025-05-04 04:45:50+00:00",
    "text": "Congress information message. Information recognize face. Form according toward evidence quite everybody."
}
```
- Идентификатор отправленного сообщения (своего)
```json
{
    "client_id": "dadf4d3c-ccf8-443d-ad7d-7dafca692fbd",
    "id": "9d5a44c4-3115-477b-83da-f7c8b4f34896"
}
```

- Созданная группа
```json
{
    "name": "Car.",
    "id": "dadf4d3c-ccf8-443d-ad7d-7dafca692fbd",
    "creator_id": "ef642621-024a-4db6-9ab2-5304c6e6221d",
    "chat_id": "6aa93e81-fefe-4b8f-812c-af1a50b077ec",
    "user_group": [
        {
            "user_id": "599e25c1-693d-4620-9abf-fde1dda5d426",
            "group_id": "dadf4d3c-ccf8-443d-ad7d-7dafca692fbd"
        },
        {
            "user_id": "ef642621-024a-4db6-9ab2-5304c6e6221d",
            "group_id": "dadf4d3c-ccf8-443d-ad7d-7dafca692fbd"
        },
        {
            "user_id": "5804d97d-0fff-4444-8647-1345d5f42175",
            "group_id": "dadf4d3c-ccf8-443d-ad7d-7dafca692fbd"
        }
    ]
}
```

# Что можно улучшить или добавить
- Хэширование паролей
- Аутентификация через REST точку по куки, чтобы использовать куки при подключения вебсокета
- Возможность подключиться по вебсокету с нескольких устройств
- Сохранение истории подключений
- OAUTH 2.0 авторизация
- Базовый кэш в redis
- kafka для поддержки больше одного процесса приложения
