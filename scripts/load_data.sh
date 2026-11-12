#!/bin/bash

set -euo pipefail

GREEN='\033[0;32m'
NC='\033[0m'

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
DATA_FILE="$PROJECT_ROOT/theme/data/data.json"

if [ ! -f "$DATA_FILE" ]; then
    echo "Error: The data file $DATA_FILE does not exist."
    echo "Please make sure the theme is installed before loading data."
    exit 1
fi

TEMP_FILE=$(mktemp --suffix=.json)
trap 'rm -f "$TEMP_FILE"' EXIT

sed "s|<install_path>|$PROJECT_ROOT|g" "$DATA_FILE" > "$TEMP_FILE"

cd "$PROJECT_ROOT"
poetry run python manage.py loaddata "$TEMP_FILE"

echo "--- Load finished ---"
echo -e "${GREEN}You can now restart the service.${NC} Example:"
echo "    sudo systemctl restart apache2.service"
