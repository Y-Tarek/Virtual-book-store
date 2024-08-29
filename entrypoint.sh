#!/bin/sh
python manage.py migrate  --noinput
echo "database migrated"
echo "from app.models import User; User.objects.filter(email='test@paymob.com').exists() or User.objects.create_superuser(email='test@paymob.com',username='Admin',first_name='paymob',last_name='admin',password='12345678')" | python3 manage.py shell
python manage.py collectstatic --noinput
python manage.py create_books
gunicorn virtualbook.wsgi -b 0.0.0.0 --disable-redirect-access-to-syslog
