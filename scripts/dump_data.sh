#!/bin/bash

set -euo pipefail

GREEN='\033[0;32m'
NC='\033[0m'

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
DATA_DIR="$PROJECT_ROOT/theme/data"
DATA_FILE="$DATA_DIR/data.json"

if [ ! -d "$DATA_DIR" ]; then
    echo "Error: The directory $DATA_DIR does not exist."
    echo "Please make sure the theme is installed before dumping data."
    exit 1
fi

TEMP_FILE=$(mktemp "$DATA_DIR/.data.json.XXXXXX")
trap 'rm -f "$TEMP_FILE"' EXIT

cd "$PROJECT_ROOT"
poetry run python manage.py dumpdata elearning \
    --natural-foreign \
    --indent 4 \
    --exclude elearning.answer \
    --exclude elearning.knowledge \
    --exclude elearning.score \
    --exclude elearning.user \
    --output "$TEMP_FILE"

sed -i "s|$PROJECT_ROOT|<install_path>|g" "$TEMP_FILE"
chmod 644 "$TEMP_FILE"
mv "$TEMP_FILE" "$DATA_FILE"
trap - EXIT

echo "--- Dump finished ---"
echo -e "${GREEN}The portable data fixture is ready.${NC}"
echo "      cd theme"
echo "      git add data/data.json"
