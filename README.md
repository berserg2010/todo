### Задание

Сделать сервис событий.
Сервис должен быть реализован как SPA-приложение.

Пользователь создает событие (встреча, звонок и т.д.) с заголовком, содержанием и датой проведения. 
Пользователь должен иметь возможность совершать CRUD-операции над своими событиями. 
Искать по заголовку и фильтровать по дате (события за последние месяц, неделю, день)

За час до проведения события, сервис отправляет напоминание по e-mail автору.

Технологии:
Python3, Django, DRF, vuejs, postgresql


### Установка Docker

https://docs.docker.com/engine/install/

### Создание миграции, регистрация суперпользователя

    docker-compose run backend python manage.py makemigrations
    docker-compose run backend python manage.py migrate
>
    docker-compose run backend python manage.py createsuperuser

Потребуется ввести `Username` и `Password`.


### Иницыализация данных приложений
    docker-compose run backend python manage.py loaddata <app>/fixtures/init_<app>.json

### Сбор статики
    docker-compose run backend python manage.py collectstatic --no-input


### Запуск контейнеров

#### dev

    docker-compose up --build

    docker-compose up
    
#### prod

    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build


### Запуск unit тестов
    docker-compose run backend pytest
