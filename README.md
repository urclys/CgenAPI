# erp-bet flask 
flask metronic template for ERP-BET application

In this application template you will find all the usefull flask plugins already configured. check the requirements.txt for the details.
The project uses Metronic V7 HTML admin demo1 template. Metronic is based on Booostrap 4 and contains every thing you'll need to build your pages.Check the metronic page for front side documentations [https://keenthemes.com/metronic/](https://keenthemes.com/metronic/).

The project is build using flask blueprints. Two blueprints are implemented Base and Home. The file structure is as follow

```
└── erp-bet
    ├── app
    │   ├── __init__.py # main init file
    │   ├── base        # base blueprint folder
    │   ├── home        # home blueprint folder
    ├── config.py       # the app config file containing different configuration for development, production or debug mode 
    ├── .env            # all the app environement variable are set here
    ├── .gitignore
    ├── requirements.txt
    └── run.py         # the application entry point
```
The authentication is done using a rest API, the rest of the app uses Jinja templating and WTForm 

###### Base blueprint
The base blueprint contains authentication logic, the project models, different usefull tools and the project static files.
```
└── base
    ├── static             # all the app static files folder
    ├── template            # html files
    ├── __init__.py         # the blueprint initialisation
    ├── auth.py             # authentication classes using rest api
    ├── forms.py            # authentication forms and validation using WTForm
    ├── models.py           # all the project models
    ├── orm_tools.py        # database related tools
    ├── routes.py           # main application routes
    ├── tools.py            # different util functions and classes 
```

###### Home blueprint
The home blueprint contains the authenticated users main pages
```
└── home
    ├── template            # html files
    ├── __init__.py         # the blueprint initialisation
    ├── forms.py            # authentication forms and validation using WTForm
    ├── routes.py           # the home blueprint routes
```

# Requirement

Python 3.7, virtualenv, mysql

# Installation

The project uses Mysql for the database, make sure to create a mysql database before proceding to the project building

````
mysql -u root

mysql> CREATE USER 'erpbet_admin'@'localhost' IDENTIFIED BY 'SQLP455>erpbe';
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE DATABASE erpbet_db0;
Query OK, 1 row affected (0.00 sec)

mysql> GRANT ALL PRIVILEGES ON erpbet_db0 . * TO 'erpbet_admin'@'localhost';
Query OK, 0 rows affected (0.00 sec)
````
The use a differente database or creadentials make sure to change the SQLALCHEMY_DATABASE_URI value in the project .env file.

Before procedding the the installation you should install virtualenv and create a new dev environement.
After that switch to your new environement and install all the project requirements

```
pip install -r requirements.txt
```

set the flask env variable
```
set FLASK_APP=run.py
```
use alembic the build the database

init : to initialize almebic migration. 
migrate: to generate the migration file. 
upgrade: to create the tables. 

```
flask db init
flask db migrate
flask db upgrade
```
Switch to the flask shell to create an admin user.
```
flask shell
```

In the flask shell import User model and db, and initialize a new user object

```
from app.base..models.users import User
from app import db

admin = User(email="admin@mabet.ma", first_name="administrateur", last_name="mabet", password="mabetP455")
```
Make the user admin and activate it
```
admin.is_admin = true
admin.is_active = true
```
Add the new user to the database and commit the changes
```
db.session.add(admin)
db.session.commit()
```
exit the flask shell
```
exit()
```
Run the app

```
python run.py
```

If everything went smoothly the app should be running on http://127.0.0.1:5000/
