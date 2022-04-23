# Message Service

API-REST for mailing service

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Basic Commands

### Environmnet


important the env_file section

```
.envs
├── .local
│   ├── .django
│   └── .postgres
└── .production
    ├── .django
    └── .postgres
```

### Development

```bash
docker-compose -f local.yml build
docker-compose up
docker-compose -f local.yml run --rm django python manage.py migrate
docker-compose -f local.yml run --rm django python manage.py createsuperuser
```

#### Running tests with pytest

    $ docker-compose -f local.yml run --rm django pytest

### Docker Containers


- Django
- Celery_beat
- Celery_worker
- Flower
- Redis
- Prometheus
- Grafana
- Postgres
- cAdvisor
- node_exporter
- traefik

### Deployment


```bash
docker-compose -f production.yml build
docker-compose up -d
```

**django**: API running behind Gunicorn;

**postgres:** PostgreSQL database with the application’s relational data;

**redis:** Redis instance for caching;

**traefik:** Traefik reverse proxy with HTTPS on by default.

**celeryworker:** running a Celery worker process;

**celerybeat:** running a Celery beat process;

**flower:** running Flower.




## Logic

### Endpoints

```json

{
  "users": "http://127.0.0.1:8000/api/users/",
  "clients": "http://127.0.0.1:8000/api/clients/",
  "mailing": "http://127.0.0.1:8000/api/mailing/",
  "messages": "http://127.0.0.1:8000/api/messages/",
  "documentacion": "http://127.0.0.1:8000/api/docs/",
  "admin": "http://127.0.0.1:8000/admin/",
  "flower": "http://127.0.0.1:5555/",
  "Grafana": "http://127.0.0.1:3000/",
}
```
