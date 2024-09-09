#  Boot Flask

## MVP Backend API

## Usage

1. Start the docker-compose stack

   The backend requires some middleware, including PostgreSQL, Redis, and Weaviate, which can be started together using `docker-compose`.

   ```bash
   cd docker
   cp middleware.env.example middleware.env
   docker compose -f docker-compose.middleware.yaml -p mvp up -d
   cd ../api
   ```

2. Copy `.env.example` to `.env`

3. Generate a `SECRET_KEY` in the `.env` file.

   ```bash
   # For Linux
   sed -i "/^SECRET_KEY=/c\SECRET_KEY=$(openssl rand -base64 42)" .env

   # For Mac
   secret_key=$(openssl rand -base64 42)
   sed -i '' "/^SECRET_KEY=/c\\
   SECRET_KEY=${secret_key}" .env
   ```

4. Create environment.

   The MVP API service uses [Poetry](https://python-poetry.org/docs/) to manage dependencies. Execute `poetry shell` to activate the environment.

5. Install dependencies

   ```bash
   poetry env use 3.10
   poetry install
   ```

6. Run migrate

   Before the first launch, migrate the database to the latest version.

   ```bash
   poetry run python -m flask db upgrade
   ```

7. Start backend

   ```bash
   poetry run python -m flask run --host 0.0.0.0 --port=5001 --debug
   ```

8. Start the frontend service (if applicable).

9. Setup your application by visiting `http://localhost:3000` (adjust the port if necessary).

10. If you need to process async tasks, start the worker service:

    ```bash
    poetry run python -m celery -A app.celery worker -P gevent -c 1 --loglevel INFO -Q main
    ```

## Testing

1. Install dependencies for both the backend and the test environment

   ```bash
   poetry install --with dev
   ```

2. Run the tests locally

   ```bash
   cd ../
   poetry run -C api bash dev/pytest/pytest_all_tests.sh
   ```
