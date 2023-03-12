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

python manage.py collectstatic --noinput --clear
python manage.py migrate --noinput

FIXTURES_LOADED=`echo "from django.contrib.auth import get_user_model; print(get_user_model().objects.filter(username='admin').exists())" | python manage.py shell`
if [ "$FIXTURES_LOADED" = "False" ]
then
    python manage.py loaddata db.json
    python manage.py create_user
fi

exec "$@"
