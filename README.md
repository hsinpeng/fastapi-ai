# FastAPI Server Tutorial
The example of constructung a FastAPI server for AI applications

## Installation by uv
Project initialization
```
cd [project folder]
uv init
uv run which python
```

Package installation
```
uv pip install --no-cache-dir -r requirements.txt
```

## Run PostgreSQL container by podman
Run container with env settings
```
podman run --name fastapi_postgres_dev -e POSTGRES_USER=fastapi_tutorial -e POSTGRES_PASSWORD=fastapi_tutorial_password -e POSTGRES_DB=fastapi_tutorial -p 5432:5432 --volume [local_folder]:/var/lib/postgresql/data -d postgres
```

Run container with env_file
```
podman run --name fastapi_postgres_dev --env-file ./db.postgresql.env -p 5432:5432 --volume [local_folder]:/var/lib/postgresql/data -d postgres
```
