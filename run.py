# -*- encoding: utf-8 -*-

from flask_migrate import Migrate


from os import environ
from sys import exit

from config import config_dict
from app import create_app, db

get_config_mode = environ.get('CONFIG_MODE')

try:
    config_mode = config_dict[get_config_mode.capitalize()]
    print(config_mode)
except KeyError:
    exit('Error: Invalid CONFIG_MODE environment variable entry.')

app = create_app(config_mode)


Migrate(app, db,compare_type=True)

if __name__ == "__main__":
    app.run()
