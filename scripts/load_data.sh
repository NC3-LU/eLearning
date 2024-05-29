#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'

# Define the directory to check
data_dir="theme/data"

# Ensure the data directory exists
if [ ! -d "$data_dir" ]; then
    echo "Error: The directory $data_dir does not exist."
    echo "Please make sure you are running the script from the project's root directory (./scripts/load_data.sh)"
    echo "or verify if the 'theme' folder exists in the project."
    exit 1
fi



# Find a JSON file in the directory
json_file=$(find "$data_dir" -maxdepth 1 -name "*.json" | head -n 1)

# Check if a JSON file was found
if [ -n "$json_file" ]; then
    new_path=$(pwd)

    # Create a temporary file with a .json extension to store the modified JSON content
    temp_file=$(mktemp --suffix=.json)

    # Use sed to replace <install_path> with the new path and write to the temporary file
    sed "s|<install_path>|$new_path|g" "$json_file" > "$temp_file"

    # Run the loaddata command using the temporary file
    poetry run python manage.py loaddata "$temp_file"

    # Clean up the temporary file
    rm "$temp_file"

    echo "--- Load finished ---"
    echo -e "${GREEN}You can now restart the service.${NC} Example:"
    echo "    sudo systemctl restart apache2.service"

else
    # Output error message if no JSON file is found
    echo "Error: No JSON file found in $data_dir."
    exit 1
fi
