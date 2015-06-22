# immobilier

## Contributing to the project

First, clone the project:

    $ mkdir python
    $ cd python
    $ mkdir projects
    $ cd projects
    $ git clone https://github.com/htmfilho/immobilier.git
    $ cd immobilier

### Creating a virtual environment

Check the version of Python you have installed in your machine using the command.

##### Ubuntu

    $ python3 --version
      Python 3.4.3

##### Windows

    $ python --version
      Python 3.4.3

The numbers that matter are 3 and 4. We use them to create a virtual environment on:

##### Ubuntu

Installing:

    # sudo apt-get install python-virtualenv

Creating:

    $ virtualenv --python=python3.4 immovenv
    $ chmod +x immovenv/bin/activate

Running:

    $ source immovenv/bin/activate

##### Windows

Creating:

    C:\Users\[Name]\python\projects\immobilier> C:\Python34\python -m venv immovenv

Running:

    C:\Users\[Name]\python\projects\immobilier> immovenv\Scripts\activate

### Installing Django

    (immovenv) $ pip install django==1.8

### Starting the app
    
    (immovenv) $ python manage.py migrate
    (immovenv) $ python manage.py runserver
    
After the restart, the application is available at http://localhost:8000.
    
### Developing

Everytime you change the model in any of the modules you have to generate a new migration file with the following command:

    (immovenv) $ python manage.py makemigrations

### Admin module

To access the admin module, you first have to create a user. Stop the server and run the following command:

    (immovenv) $ python manage.py createsuperuser
    
Follow the instructions and restart the server. To test your access, go to http://localhost:8000/admin and test your access.
