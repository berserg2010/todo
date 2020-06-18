### Установка Docker

https://docs.docker.com/engine/install/

### Создание миграции, регистрация суперпользователя

    docker-compose run web python manage.py makemigrations
    docker-compose run web python manage.py migrate
>
    docker-compose run web python manage.py createsuperuser

Потребуется ввести `Username` и `Password`.


### Иницыализация данных приложений
    docker-compose run web python manage.py loaddata <app>/fixtures/init_<app>.json

### Сбор статики
    docker-compose run web python manage.py collectstatic --no-input


### Запуск контейнеров

#### dev

    docker-compose up --build

    docker-compose up
    
#### prod

    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build


### Запуск unit тестов
    docker-compose run web pytest


### Снятие копии с базы данных приложения
    docker-compose run web python manage.py dumpdata <app> --indent 2 --output dump_<app>.json
