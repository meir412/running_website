# Usage
* Navigate to http://running-website-eu.herokuapp.com
* The `Running website` is a hobby django project intended to help users store and analyze
their running data

# Development
## Steps to run website on local django development server
1. Install all required dependencies:
    ```commandline
    sudo apt-get install python3.7
    sudo apt-get install python3-virtualenv
    sudo apt-get install python3-pip
    sudo apt-get install libpq-dev
    sudo apt-get install postgresql postgresql-contrib
    ```
2. Choose a local directory that will contain the repository and navigate to it
3. Configure python virtual environment and install python modules from `requirements.txt`:
    ```commandline
    python3.7 -m virtualenv --python=/usr/bin/python3.7 env
    source env/bin/activate
    pip install -r requirements.txt
    ```
4. Create and configure local postgres db:
    ```commandline
    sudo -u postgres psql
    create database running;
    create user local_user with password 'password';
    grant all privileges on database running_website to local_user;
    alter role local_user SUPERUSER;
    ```
5. Clone this repository
6. Install node packages:
    ```commandline
    cd running_dashboard/static
    npm install
    npm run build
    ```
7. Apply migrations, load sample data and run the server:
    ```commandline
    python manage.py migrate
    python manage.py loaddata running_dashboard/fixtures/run.json
    python manage.py runserver
    ```
8. Your local django server should be running and the website can be accessed at `http://127.0.0.1:8000/`
