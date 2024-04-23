#!/bin/bash

echo "--- Updating ---"

# Define an array of repositories to update
repositories="elearning theme"

# Function to check if repository directory exists
check_repository_exists() {
    local repo=$1
    if [ ! -d "$repo" ]; then
        echo "Error: Directory '$repo' does not exist."
        exit 1
    fi
}

# Function to update repositories
update_repositories() {
    for repo in $repositories; do
        check_repository_exists "$repo"
        echo "--- Git pull repository: $repo ---"
        (cd "$repo" && git pull origin master)
    done
}

# Function to update npm packages
update_npm_packages() {
    echo "--- Updating npm packages ---"
    npm install
}

# Function to update python packages
update_python_packages() {
    echo "--- Updating python packages ---"
    poetry install
}

# Function to migrate database
migrate_database() {
    echo "--- Migrating Database ---"
    poetry run python manage.py migrate
}

# Function to compile translations
compile_translations() {
    echo "--- Compiling translations ---"
    poetry run python manage.py compilemessages
}

# Function to collect static files
collect_static_files() {
    echo "--- Collecting static ---"
    poetry run python manage.py collectstatic --no-input > /dev/null 2>&1
}

restart_apache() {
    echo "--- Restarting Apache ---"
    sudo systemctl restart apache2
}

# Call functions
update_repositories
update_npm_packages
update_python_packages
migrate_database
compile_translations
collect_static_files
restart_apache
