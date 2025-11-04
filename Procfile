release: python manage.py collectstatic --noinput && python manage.py migrate
web: python -m daphne -b 0.0.0.0 -p $PORT config.asgi:application