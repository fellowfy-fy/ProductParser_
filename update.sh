git pull
set -e
#docker-compose exec web pipenv run pytest .
#docker-compose exec web python3 manage.py collectstatic --no-input
docker compose restart web huey
./migrate.sh
