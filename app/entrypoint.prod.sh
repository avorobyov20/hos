#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Postgres is not running yet..."

    # Проверяем доступность хоста и порта
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "Postgres is running"
fi

exec "$@"
