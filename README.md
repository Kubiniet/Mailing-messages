# Message Service

API for message service

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

```
Django
Celery_beat
Celery_worker
Flower
Redis
Prometheus
Grafana
Postgres
```

## Основное задание

### Endpoints

```json
{
  "users": "http://127.0.0.1:8000/api/users/",
  "clients": "http://127.0.0.1:8000/api/clients/",
  "mailing": "http://127.0.0.1:8000/api/mailing/",
  "messages": "http://127.0.0.1:8000/api/messages/",
  "documentacion": "http://127.0.0.1:8000/api/docs/",
  "admin": "http://127.0.0.1:8000/admin/"
}
```

После создания новой рассылки (ПОСТ на "http://127.0.0.1:8000/api/mailing/"), если текущее время больше времени начала и меньше времени окончания - должны быть выбраны из справочника все клиенты, которые подходят под значения фильтра, указанного в этой рассылке и запущена отправка для всех этих клиентов.

Если создаётся рассылка с временем старта в будущем - отправка стартует автоматически по наступлению этого времени без дополнительных действий со стороны пользователя системы.

По ходу отправки сообщений должна собираться статистика через Flower на http://127.0.0.1:5555/ и Grafana на http://127.0.0.1:3000/ по каждому сообщению для последующего формирования отчётов .

Проблемы с внешним сервисом не должны влиять на стабильность работы разрабатываемого сервиса рассылок.

## Дополнительные задания

### 1.Организовать тестирование написанного кода

Pytest для тестов и FactoryBoy для создания данных

    $ docker-compose -f local.yml run --rm django pytest

### 2.Обеспечить автоматическую сборку/тестирование с помощью GitLab CI

[.gitlab-ci.yml](https://github.com/Kubiniet/Mailing-messages/blob/main/.gitlab-ci.yml)

### 3.Подготовить docker-compose для запуска всех сервисов проекта одной командой

Именно разработал всё под [local.yml](https://github.com/Kubiniet/Mailing-messages/blob/main/local.yml)

### 4 делать так, чтобы по адресу /docs/ открывалась страница со Swagger UI и в нём отображалось описание разработанного

APDocumentation of API endpoints of Message Service
http://127.0.0.1:8000/api/docs/

### 5. реализовать администраторский Web UI для управления рассылками и получения статистики по отправленным сообщениям

Django admin может использовать модели для автоматического создания части сайта, предназначенной для создания, просмотра, обновления и удаления записей.Можем создать рассылки и отправить те которые еще не отправленны
http://127.0.0.1:8000/admin/

### 9.Задержки в работе внешнего сервиса никак не должны оказывать влияние на работу сервиса рассылок.

Сделал систему очередей с Redis и Celery, а обработку всех ошибок

### 10.реализовать отдачу метрик в формате prometheus и задокументировать эндпоинты и экспортируемые метрики

Запускал prometheus http://127.0.0.1:9090 в контейнере Докера с интеграцией grafana http://127.0.0.1:3000/

[prometheus.yml](https://github.com/Kubiniet/Mailing-messages/blob/main/prometheus.yml)
