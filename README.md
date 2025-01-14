# Event Manager Application

## Overview

Event Manager is a web application designed to manage event registrations. The project is containerized using Docker for easy setup and deployment.

## Installation

To get started with the Event Manager project, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone git@github.com:okuzmenko31/EventManager.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd EventManager
   ```

3. **Set Up the Environment**:
   Create a `.env` file in the root directory of the project with the following content. Replace sensitive information with your actual credentials or placeholders.

   ```env
   # Application
   APP_PORT=8000
   DEBUG=True
   SECRET_KEY=your_secret_key

   # Database
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=event_manager
   DB_USER=postgres
   DB_PASSWORD=admin
   DB_HOST=postgresql
   DB_PORT=5432

   # Internationalization
   LANGUAGE_CODE=en-us
   TIME_ZONE=UTC

   # Migrations
   RUN_MIGRATIONS=True

   # RabbitMQ
   RABBITMQ_HOST=rabbitmq
   RABBITMQ_USER=guest
   RABBITMQ_PASSWORD=guest
   RABBITMQ_PORT=5672
   RABBITMQ_PORT_SECOND=15672

   # SMTP
   EMAIL_HOST=smtp.gmail.com
   EMAIL_HOST_USER=example@gmail.com
   EMAIL_HOST_PASSWORD=password_placeholder
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   ```

## Running the Application

### Option 1: Using Makefile

Use the provided `Makefile` to manage Docker containers and Django commands easily.

#### Build and Start the Containers

```bash
make run
```

#### Stop the Containers

```bash
make stop
```

#### Access Shell in the App Container

```bash
make shell
```

#### Create a Superuser

```bash
make createsuperuser
```

### Option 2: Using Docker Compose Commands Directly

#### Build and Start the Containers

```bash
docker compose up -d --build
```

#### Stop the Containers

```bash
docker compose stop
```

#### Access Shell in the App Container

```bash
docker compose exec app bash
```

#### Create a Superuser

```bash
docker compose exec app python3.13 manage.py createsuperuser
```

## API Documentation

The application provides API documentation and schema in multiple formats:

- **Swagger**: Accessible at `/api/v1/docs`
- **ReDoc**: Accessible at `/api/v1/redoc`
- **API Schema (YAML)**: Accessible at `/api/v1/schema`

## Makefile Commands

Below are detailed descriptions of the commands available in the `Makefile`:

### Docker Commands

- **`run`**: Build and start the containers in detached mode.
- **`build`**: Build the Docker images without using cache.
- **`stop`**: Stop the running containers.
- **`down`**: Stop and remove the containers, networks, volumes, and images created by `up`.
- **`logs`**: View logs for a specific container (default is `app`).
- **`logs-all`**: View logs for all containers.
- **`restart`**: Restart a specific container (default is `app`).
- **`shell`**: Access the shell of the specified container (default is `app`).
- **`shell-root`**: Access the shell as the root user.
- **`ps`**: List all running containers.

### Django Commands

- **`startapp`**: Create a new Django app within the `api` directory.
- **`createsuperuser`**: Create a new Django superuser.

### Migration Commands

- **`migrations`**: Create new migrations based on changes in models.
- **`migrate`**: Apply migrations to the database.
- **`migrate-to`**: Migrate to a specific version.
- **`migrations-history`**: Show the history of applied migrations.

### Requirements Command

- **`pip-list`**: List all installed Python packages.

With this setup, you can easily manage and deploy the Event Manager application using Docker and Django's powerful tools. The provided Makefile simplifies common tasks, and comprehensive API documentation ensures seamless integration and usage.