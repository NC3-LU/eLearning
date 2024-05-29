#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'

# Define the directory to check
data_dir="theme/data"

# Ensure the data directory exists
if [ ! -d "$data_dir" ]; then
    echo "Error: The directory $data_dir does not exist."
    echo "Please make sure you are running the script from the project's root directory (./scripts/dump_data.sh)"
    echo "or verify if the 'theme' folder exists in the project."
    exit 1
fi

# Perform the dumpdata command
poetry run python manage.py dumpdata elearning --indent=4  --exclude=elearning.answer --exclude=elearning.knowledge --exclude=elearning.score --exclude=elearning.user > "$data_dir/data.json"

# Define the path to the JSON file
json_file="$data_dir/data.json"

# Replace $(pwd) with <install_path> in the JSON file
sed -i "s|$(pwd)|<install_path>|g" "$json_file"

echo "--- Dump completed ---"
echo -e "${GREEN}You're now ready to push the data.json file.${NC} For example:"
echo "      cd theme"
echo "      git push -am \"[data]Updated dump json file\""
