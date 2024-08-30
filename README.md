# Virtual-bookstore
An API and admin dashboard for managing books and their reviews.

## API Documentation
https://documenter.getpostman.com/view/28439113/2sAXjKZs4W

## Prerequisite

- python (3.x)

- Docker (optional for running docker container)

## Installtion

### Using Docker


     docker-compose up --build

     A superuser is created automatically for you with this email & pass:
     
       - email: test@paymob.com
       - password: 12345678
     
    Access the admin dashboard at http://0.0.0.0:8000/admin using these credentials to manage data.

    Books are predefined automatically by running this command in entrypoint.sh:
       - python manage.py create_books

     Now container is up & running you can test APIs by following API documentation above.

 ### Manual Installation


       If you prefer to run the application manually:
       1- Database Configuration: Create a .env file to configure your database settings. For PostgreSQL or another database, include the following variables:
              - SQL_ENGINE=django.db.backends.postgresql (or any other engine)
              - SQL_DATABASE=virtual-bookstore (or any other name)
              - SQL_HOST=localhost 
              - SQL_USER=postgres (or any other name)
              - SQL_PASSWORD=postgres (or any other name)

           For SQLite (the default database), no .env file is needed.
           
         2- Set Up Virtual Environment:
            python -m venv venv.
            source venv/bin/activate  (Linux venv activation)
            venv/scripts/activate     (Windows venv activation)
            
         3- Install Dependencies:: 
             pip install -r requirememnts.txt.
             
         4- Apply Migrations:
           python manage.py makemigrations.
           python manage.py migrate.
           
         5- Create Superuser: Required for accessing the admin dashboard. You will be prompted to enter your details:
              python manage.py createsuperuser
              
         6- Run the Development Server:
            python manage.py runserver
            The server will be available at http://127.0.0.1:8000. Use the API documentation for testing and admin dashboard will be http://127.0.0.1:8000/admin.

         7- For creating books to be predifined instead of creating them using admin run:
            - python manage.py create_books
            
         8- Run Tests:
            python manage.py test
            
         9- Application Coverage: To generate coverage reports:
            coverage run manage.py test
            coverage html

 
    
