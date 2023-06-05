# Foodgram
### Описание
Онлайн-сервис и API для приложения Foodgram.
Foodgram: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 
### Технологии
Python 3.7

Django 3.2

Django REST Framework 3.14

### Запуск проекта в dev-режиме
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/serebrennikovalexander/foodgram-project-react.git
```

```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
python3.7 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip3 install -r requirements.txt
```

Запустить проект:

```
cd backend/foodgram_backend
```

```
python3 manage.py runserver
```

Сейчас используется база данных SQLite.
В базе есть 7 тестовых рецептов, 2 пользователя и админ.
Ингредиенты и теги добавлены в базу данных с помощью миграций.
Через Postman рецепты создавались с картинкой взятой из теории и
закодированной в base64.
 

Данные админа:
```
email: admin@admin.ru
password: foodgram1234
```

Данные пользователей:
```
email: vpupkin1@yandex.ru
password: foodgram1234

email: vpupkin2@yandex.ru
password: foodgram1234
```

### Автор
Александр Серебренников

для комита 8