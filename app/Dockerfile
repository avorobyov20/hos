# образ на основе которого создаем контейнер
# можно использовать другую версию, репозиторий образов здесь https://hub.docker.com/_/python/
# мы воспользуемся 3.10.6-alpine, который соответствует версии python в wsl2 Ubuntu
FROM python:3.10.6-alpine

# рабочая директория внутри проекта
WORKDIR /usr/src/app

# переменные окружения для python
# python не будет создавать файлы кэша .pyc
# и не будет помещать в буфер потоки stdout и stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# через менеджер пакетов контейнера устанавливаем зависимости,
# которые требуются для работы Django с Postgres.
# потом останется только добавить "psycopg2-binary==2.9.5" в app/requirements.txt
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# устанавливаем зависимости
RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# копируем содержимое текущей папки в контейнер
COPY . .

# Создадим скрипт, который при каждом запуске контейнера web_dev будет проверять
# запущен ли контейнер db_dev, дожидаться запуска postgres в db_dev и выполнять миграции автоматически.
# Важно не забыть изменить права на файл chmod 774 app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
