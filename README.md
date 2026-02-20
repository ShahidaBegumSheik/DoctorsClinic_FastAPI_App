# Clinic API
Objective:

To build a complete backend system using FastAPI that includes authentication, authorization, business logic, and database persistence for managing Doctors and Patients. 
The app name : Clinic API

I. Tech stack: 
Python 3.9+
FastAPI
Pydantic
SQLAlchemy
PostgreSQL
JWT based Authentication,
Uvicorn

II. Install Dependencies

If you face bcrypt error:

    pip uninstall -y bcrypt passlib
    pip install “passlib[bcrypt]==1.7.4” “bcrypt<4.0”

Install Software for running this FastAPI application 
Go to Python website: https://www.python.org/downloads/windows/
and download Python and install it in your system by double-clicking it.

From the command prompt check the version of the Python installed using the command :
      
      python –version
 
Create a folder “doctorsApp” for the project and open it in VSCode

Create a python virtual environment for this project in VSCode and activate it

        python -m venv venv
        ./venv/Scripts/activate

Install the required software in this environment. Create a “requirements.txt” in the project folder and add the software with versions in it
  	
    fastapi>=0.110
    uvicorn[standard]>=0.27
    SQLAlchemy>=2.0
    psycopg2-binary>=2.9
    pydantic>=2.5
    pydantic-settings>=2.1
    python-jose[cryptography]>=3.3
    passlib[bcrypt]>=1.7
    alembic>=1.13
    pytest>=8.0
    httpx>=0.27
    slowapi>=0.1.9
    python-multipart>=0.0.9
    email-validator>=2.1
    asyncpg>=0.29.0

  Run the following command :
  	
  	    pip install -r requirements.txt

Start the “uvicorn” server:
   
        uvicorn app.main:app –reload
  	
III. PostgreSQL Setup
1. Install PostgreSQL on your machine
    pgAdmin app shows the hostname, portnumber, username that will be used in the python code
2. Create a database

       CREATE DATABASE <db_name>;
   
4. Set the .env:
       
       DATABASE_URL=postgresql://postgres:PASSWORD@localhost:<PORT_NUMBER>/<db_name>
   
IV Application 

•	Authentication and authorization using JWT
Role Based Access Control 
There are different types of users:
1. ADMIN
2. DOCTOR
3. Patient (not considered as user)
Each role has different permissions:
ADMIN – create doctors, create patients, assign patients, list all doctors and patients
DOCTOR – View only their assigned patients

Swagger UI Authorization in the Clinic API is implemented using OAuth2 with JWT bearer authentication. The application exposes a token endpoint(/auth/login) that follows the OAuth2 Password Grant flow. When a user clicks the Authorize button in Swagger UI, they are prompted to enter their credentials (username and password). Swagger UI then sends these credentials to the token endpoint to request an access token. Upon successful authentication, the server issues a JWT access token containing the user’s identity and role information. Swagger UI securely stores this token in the browser session and automatically attaches it to subsequent API requests in the HTTP header.

•	API flow
1. registration of admin and doctors - /auth/register
2. logging in of Admin or Doctor  - /auth/login
3. Swagger UI Authorization using admin or doctor credentials 
4. Once swagger UI is authorized to execute APIs, we can do CRUD operations in the Swagger UI
5. Add doctors – POST /doctors
6. View doctors – GET /doctors
7. View doctor using their id – GET /doctors/{doctor_id}
8. Update any doctor details – PUT /doctors/{doctor_id}
9. delete doctor details – DELETE /doctors/{doctor_id}
10. Add patients – POST /patients
11. View patients -  GET /patients
12. Assign patients to doctors, one doctor can have many patients and each patient can consult many doctors. 
13. View the assigned doctors – patients data – POST /{doctor_id}/patients/{patient_id}
14. rate limiter – GET /health – used to verify whether the application is running properly – here 30/minute limit is set 

V. Tests using pytest
Using pytest for Fast API app

1. Install pytest

2. Create a PostgreSQL test database

        CREATE DATABASE mydb_test

4. Create .env file in project root

        ENV=test
        
        DATABASE_URL=postgresql://postgres:<pwd>@localhost:5433/mydb
        TEST_DATABASE_URL=postgresql://postgres:<pwd>@localhost:5433/mydb_tests
        
        TEST_DB_NAME=mydb_tests
        JWT_SECRET=test-secret

5. Run Tests
     From project root:

        pytest -q

6. Check test data in pgAdmin
       - open mydb_tests
       - look at tables: users, doctors, patients
       - rows would have been created by tests
    
VI. Alembic – Migrations and Auto Generating Revisions from SQLAlchemy Models
     
  1. Create a migration environment
     
o	Install alembic and psycopg2 (PostgreSQL driver for Python)

Specified in the requirements.txt file

o	Migration environment is created using the “init” command

    alembic init myapp

o	env.py is run anytime when the alembic migrations are invoked

o	Tell the alembic how to connect to the database that is in the PostgreSQL in local system

In the alembic/ini file, update sqlalchemy.url with the actual path to the postgresql db used for migrations
                
    sqlalchemy.url = postgresql+psycopg2://postgres:<pwd>@localhost:5433/mydb

o	Make sure alembic imports your models 

In alembic/env.py you must import the model modules so they register with Base.metadata

    from app.db.base import Base
    from app.models import user, doctor, patient

    sys.path.append(str(Path(__file__).resolve().parents[1]))

    target_metadata = Base.metadata
o	Stop creating tables in FastAPI startup. So, remove this from lifespan()
        
        # Base.metadata.create_all(bind=engine)

o	Ensure your DB schema is truly empty from the pgAdmin app

 2. Create a migration
o	Run this command for the first migration

        alembic revision –autogenerate -m “initial tables”

o	Open the generated file (starting with some revision number inside the alembic/versions folder.

We can see the updations to create tables in upgrade() and drop tables in downgrade() 

o	We can make any modifications in these generated code
 4. Apply migration
    Now run :

        alembic upgrade head

VII. Docker 
       PostgreSQL and FastAPI app in Docker
    i) Installing docker in your system (Windows here)
       Docker Desktop on Windows does not run directly on Windows. It runs inside a small Linux VM using WSL2.
       
   Minimum requirements:
-	Windows 10 64-bit or Windows 11
-	Virtualization enabled in BIOS
-	At least 8 GB RAM 
-	CPU virtualization support (Intel VT-x / AMD-V)
-	WSL2
In power shell:

        wsl –install

 	 Restart PC
   In power shell, run this command
 	
        wsl -l -v

 	you should see version 2.
       
  Go to official website
  
        https://www.docker.com/products/docker-desktop/
  
  Download Docker Desktop for Windows (WSL2)
  Use this Docker app for managing containers visually + via terminal

 ii) Add a Dockerfile for the FastAPI app
     Create Dockerfile  at the project root
     Specify the installation commands for installing system deps, application deps and commands for copying 
     application code and default command

iii) Add a docker-compose.yml. It is used to run the FastAPI application and the PostgreSQL server
     Create docker-compose.yml file at the project root
     Update the db and api services sections with the values for the fields
      
iv) Make sure alembic can run inside the container. Alembic needs a Sync Postgres driver (usually psycopg2). Add 
     these to the requirements.txt 
      
        alembic>=1.13.1
        psycopg2-binary>=2.9
      
  in alembic.ini write code to replace “postgresql+asyncpg” to “postgresql+psycopg2” 

v)  Running everything from Docker desktop
     - from the project root, run the following command:
       
       docker compose up –build
       
  we can run the FastAPI app in the docker now.


