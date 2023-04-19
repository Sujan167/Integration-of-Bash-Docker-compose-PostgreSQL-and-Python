#!/bin/bash

# Create and activate virtual environment
python3 -m venv env

#Activate virtual environment for windows as we as mac and linux 
# mac and linux have same command for starting virtual environment
if [[ $(uname) == "CYGWIN_NT-10.0" ]]
then
    echo "Activating virtual machine in windows"
    .\env\Scripts\Activate.ps1
else
    echo "Activating virtual machine in mac/linux"
    source env/bin/activate
fi

# Install psycopg2-binary in virtual environment
pip install psycopg2-binary

# Start Docker containers
docker-compose up -d

# Wait for Docker to start up
echo "Wait Docker is waking up"
sleep 5

# Upload data to database
echo "Now Uploading in database"
python3 python-script.py

# Stop Docker containers
docker-compose down

# Deactivate virtual environment
deactivate

echo '''
host = localhost
port = 5432
user = postgres
password = postgres
dbname = postgres
'''