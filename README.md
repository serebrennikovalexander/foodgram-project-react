# Foodgram
# ![example workflow](https://github.com/serebrennikovalexander/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

### Технологии

Python 3.7, React, Django 3.2, Django REST Framework 3.14, PostgreSQL, Nginx,
Gunicorn, Docker, GitHub Actions, Yandex.Cloud

### Описание
Онлайн-сервис и API для приложения Foodgram.
Foodgram: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Приложение было упаковано в контейнера с помощью технологии [Docker](https://www.docker.com/)
и запущено на сервере в Яндекс.Облаке в трёх контейнерах: nginx, PostgreSQL и Django+Gunicorn. 
Заготовленный контейнер с фронтендом используется для сборки файлов.

Для приложния настроены CI (continuous Integration) и CD (Continuous Deployment).
CI и CD реализованы на основе облачного сервиса [GitHub Actions](https://github.com/features/actions).

В файле `foodgram-project-react/.github/workflows/foodgram_workflow.yml` описаны следующие команды:
- проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8)
- сборка и доставка докер-образа для контейнера backend на [Docker Hub](https://hub.docker.com/)
- автоматический деплой проекта на удалённом сервере

Развёрнутый на удалённом сервере, проект можно посмотреть по следующим ссылкам:
```
http://62.84.116.232/
http://62.84.116.232/admin/
http://62.84.116.232/api/docs/
```

Данные админа:
```
email: admin@admin.ru
password: foodgram12345
```

Данные пользователя:
```
email: user1@user.ru
password: foodgram987
```

### Автор
Александр Серебренников
