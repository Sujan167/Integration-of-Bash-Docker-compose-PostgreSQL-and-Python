# Integration of Bash, Docker-compose, PostgreSQL and Python


Bash Script to execute Python Script that Uploads JSON Data to PostgreSQL Database Using Docker Compose

## Project Description
This project consists of a Python script that fetches data from a JSON file and uploads it to a PostgreSQL database running in a Docker container. The project also includes a Bash script that automates the process of setting up a virtual environment, installing the required packages, starting the Docker container, executing the Python script to upload the data, stopping the Docker container, and deactivating the virtual environment.

## Prerequisites
To run this project, you will need the following:

- Docker
- Docker Compose
- Python 3

## Usage

1.) Clone this repository to your local machine.

2.) Navigate to the root directory of the project in your terminal.

3.) Run the following command to execute:
```bash
./script.sh
```
This will check the uname of your machine and activate the appropriate virtual environment (either Windows or Mac/Linux), install the required packages from the requirements.txt file, start the Docker container for PostgreSQL, execute the Python script to upload the data, stop the Docker container, and deactivate the virtual environment.

## License
This project is licensed under the MIT License - see the [LICENSE](https://choosealicense.com/licenses/mit/) file for details.
