echo "Running makemigrations"
python manage.py makemigrations
echo "Running migrate"
python manage.py migrate
echo "Running collectstatics"
python manage.py collectstatic --noinput
echo "Running server"
python manage.py runserver
