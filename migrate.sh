#docker-compose exec web pipenv run python3 manage.py makemigrations $1
#docker-compose exec web pipenv run python3 manage.py migrate

#docker-compose exec web python3 manage.py makemigrations $1
docker compose exec web python3 manage.py migrate

