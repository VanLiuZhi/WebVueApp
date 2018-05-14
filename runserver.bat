%~d0
cd %~d0%~p0
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8080
