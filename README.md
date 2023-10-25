# User Service

## Environment variables

Flask service needs these environment variables

    FLASK_ENV=dev
    SECRET_KEY=SECRET_KEY


# Running on your system 

### Create virtual environment
    python3 -m venv <virtualenv path and venv name>
                    or
    sudo apt-get install virtualenv
    virtualenv <name>


### Install packages

    pip3 install -r requirements.txt
    
### database tables creation and updation

Initiate a migration folder using init command for alembic to perform the migrations.

    python migrate.py db init
Create a migration script from the detected changes in the model using the migrate command. This doesn’t affect the database yet
    
    python migrate.py db migrate --message 'initial database migration'
Apply the migration script to the database by using the upgrade command

    python migrate.py db upgrade

**Each time the database model changes, repeat the migrate and upgrade commands**

### Run all test cases

    py.test   
**If any issues, make sure change the DEBUG value to False**

### Run single Test case or file
    py.test -k <filename>/<testcase name>
    


### Run development server

    python run.py

### Open docs in browser using link

    http://localhost:5000/swagger/document

# Docker process
  # Docker running command
    Create docker-compose.yml file

    For building the containers run the below command
      ---> docker-compose up --build

