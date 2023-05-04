python manage.py collectstatic --no-input
python manage.py migrate --force
daphne core.asgi:application --bind 0.0.0.0