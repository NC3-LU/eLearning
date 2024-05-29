#!/bin/bash


GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Define usage message
usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -u, --update-repositories   Update git repositories"
    echo "  -npm, --update-npm-packages Update npm packages"
    echo "  -p, --update-python-packages Update python packages"
    echo "  -m, --migrate-database      Migrate database"
    echo "  -c, --compile-translations  Compile translations"
    echo "  -s, --collect-static        Collect static files"
    echo "  -a, --update-all            Update all components"
    echo "  --help                      Display this help message"
    exit 1
}

# Define an array of repositories to update
repositories=("elearning" "theme")

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
    for repo in "${repositories[@]}"; do
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

# Function to update finish
update_finished() {
    echo "--- Update finished ---"
    echo -e "${GREEN}You can now restart the service.${NC} Example:"
    echo "    sudo systemctl restart apache2.service"
}


# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -u|--update-repositories) update_repositories; update_finished; shift ;;
        -npm|--update-npm-packages) update_npm_packages; update_finished; shift ;;
        -p|--update-python-packages) update_python_packages; update_finished; shift ;;
        -m|--migrate-database) migrate_database; update_finished; shift ;;
        -c|--compile-translations) compile_translations; update_finished; shift ;;
        -s|--collect-static) collect_static_files; update_finished; shift ;;
        -a|--update-all)
            update_repositories
            update_npm_packages
            update_python_packages
            migrate_database
            compile_translations
            collect_static_files
            update_finished
            exit 0
            ;;
        --help) usage ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
done
