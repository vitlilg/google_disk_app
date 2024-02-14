# Simple Google OAuth2 Disk backend
**Проект "Simple Google OAuth2 Disk"** - веб-аплікація на основі FastAPI та OAuth2 , яка дозволяє користувачам управляти своїми папками та файлами на Google Disk (див. розділ "Робота з проектом").

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
http://127.0.0.1:8000/docs,
де http://127.0.0.1:8000/ - url адреса вашого backend серверу.

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

2. Після успішної аутентифікації відкриється список папок та файлів.

    Можливі дій на сторінці списку папок та файлів:
   - Створити папку в поточній папці;
   - Створити файл в поточній папці;
   - Відкрити (завантажити) файл або відкрити папку;
   - Перемістити файл або папку в корзину;
   - Видалити файл або папку;
   - Перемістити файл або папку в іншу папку;
   - Пошук файлів за іменем та папок за ID.
3. При переміщенні файлу в корзину відкривається сторінка корзини.

   Можливі дій на сторінці корзини:
   - Відновити файл або папку;
   - Видалити файл або папку;
   - Очистити корзину.

4. При пошуку відкривається сторінка пошуку.

   Можливі дій на сторінці пошуку:
   - Відкрити файл або папку;
   - Перемістити файл або папку в корзину;
   - Видалити файл або папку;
   - Перемістити файл або папку в іншу папку;
   - Пошук файлів за іменем та папок за ID.

5. У верхньому меню присутні кнопки швидкого переходу до корневої папки та корзини, а також кнопка виходу з сайту.
