# Simple Google OAuth2 Disk backend
**Проект "Simple Google OAuth2 Disk"** - веб-аплікація на основі FastAPI та OAuth2 , яка дозволяє користувачам управляти своїми папками та файлами на Google Disk .

Кожен користувач має можливість:
1.	Переглядати свої папки та файли.
2.	Додавати нові елементи.
3.	Видаляти існуючі елементи.
4.	Переміщувати об'єкти між папками.
5.	Редагувати файли.

Інтерфейс користувача - простий фронтенд (без стилів), який виконує базові операції управління файлами.

## Стек технологій
![Python](https://img.shields.io/badge/Python-3.10.5-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-28a745)

Повний перелік залежностей - [requirements.txt](./requirements.txt)

# Налаштування проекту
## Змінні оточення
Мінімальні вимоги для запуску проекту
```bash
# Filename: .env

SECRET="<str>"


GOOGLE_OAUTH_CLIENT_ID=<str>
GOOGLE_OAUTH_CLIENT_SECRET=str

REDIRECT_URL="str"
```

Повний перелік змінних оточення - [.env.example](./.env.example)

## Налаштування оточення
Створіть та активуйте віртуальне оточення
```bash
python -m venv venv
source ./venv/bin/activate
```

Активуйте pre-commit
```bash
pre-commit install
```

# Запуск проекту
Зробіть запуск серверу backend за допомогою команди
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

## Swagger
Для переходу до сторінки автодокументації у браузері потрібно ввести, наприклад:
http://localhost:8000/docs,
де http://localhost:8000/ - url адреса вашого backend серверу.

## Docker
Для запуску контейнера необхідно створити в корені проекту файл .docker.env на основі цього файлу [.docker.env.example](./.docker.env.example)
У файлі docker-compose.yml у строці *image: vitlilg/web_vpn_service:latest* замість vitlilg вставити назву свого облікового запису для docker.
Потім виконати:
```bash
docker compose build
docker compose up
```

# Робота з проектом
1. Початок роботи починається зі сторінки логіну:
http://127.0.0.1:8000/auth/login
Тестові дані для входу:
Логін: vitlilg.test@gmail.com
Пароль: Test@pp1234

2. Після успішної аутентифікації відкриється список папок та файлів.
