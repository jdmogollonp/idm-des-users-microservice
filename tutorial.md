# Tutorial

pip3 install fastapi fastapi-sqlalchemy pydantic alembic uvicorn python-dotenv
pip3 install psycopg2-binary
pip3 install pydantic
pip install email-validator

docker-compose build
docker-compose run app alembic upgrade head
docker-compose run app alembic revision --autogenerate -m "New Migration"
docker-compose up
