#!/bin/bash



# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"

# Activate the virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the Flask app
echo "Starting Flask API service on http://localhost:5001 ..."
python -u app.py

 /opt/homebrew/bin/python3.11 app.py