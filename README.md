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

### Предварительная настройка

1. Необходимо инициализировать переменные окружения.
В папек `env_private/` необходимо скопировать шаблоны, удалив при этом расширение `.template`.

2. Примеры переменных:
    
    `db.env.template`
    
    - POSTGRES_HOST=db
    - POSTGRES_DB=postgres
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=postgres
    
    `front_dev.env`
    
    - NODE_ENV=development
    - BROWSER_BASE_URL=http://192.168.1.1

    `front_prod.env`
    
    - NODE_ENV=production
    - BROWSER_BASE_URL=http://192.168.1.1
    
    `web.env`
    
    - DJANGO_SECRET_KEY=!6@%ch8p6o#7u!zx&=@s3kejg483y+8%c#fped_d*fb-v&#*45
    - EMAIL_HOST=smtp.yandex.ru
    - EMAIL_HOST_USER=`***`@yandex.com
    - EMAIL_HOST_PASSWORD=`***`

### Создание миграции, регистрация суперпользователя

    docker-compose run backend python manage.py makemigrations
    docker-compose run backend python manage.py migrate
>
    docker-compose run backend python manage.py createsuperuser

Потребуется ввести `Username` и `Password`.


### Сбор статики
    docker-compose run backend python manage.py collectstatic --no-input


### Запуск контейнеров

Frontend запускается на 8000 порту, backend - на 8080.

#### dev

    docker-compose up --build

#### prod

    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build


### Запуск unit тестов
    docker-compose run backend pytest
