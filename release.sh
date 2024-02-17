set -e
python manage.py migrate
python manage.py createsuperuser