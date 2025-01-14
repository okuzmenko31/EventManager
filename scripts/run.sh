#!/bin/sh

# Define the application base directory
APP_DIR="/event_manager_app/api"

# Wait for dependent services to be ready (PostgreSQL, Redis etc)
sleep 5

# Automatically load the appropriate .env file based on MODE
set -a
ENV_FILE="$APP_DIR/.env"

if [ -e "$ENV_FILE" ]; then
    # Load .env file safely, handling quotes and whitespace
    while IFS='=' read -r key value; do
        # Trim whitespace from the key and value
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)

        # Skip comments and empty lines
        case "$key" in
            \#* | "") continue ;;
        esac

        # Remove surrounding quotes from the value if present
        value=$(echo "$value" | sed 's/^['\''"]//;s/['\''"]$//')

        # Export the variable
        export "$key=$value"
    done < "$ENV_FILE"
    echo "Loaded environment file: $ENV_FILE"
else
    echo "No environment file found at $ENV_FILE. Exiting."
    exit 1
fi
set +a

# Navigate to the application directory
cd "$APP_DIR" || { echo "Failed to change directory to $APP_DIR. Exiting."; exit 1; }

# Database migration
if grep -qi '^RUN_MIGRATIONS=True' $ENV_FILE; then
    python3.13 manage.py migrate || { echo "Database migration failed. Exiting."; exit 1; }
fi

# Start Django application
python3.13 manage.py runserver 0.0.0.0:$APP_PORT
