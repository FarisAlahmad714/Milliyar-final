#!/bin/bash

sudo service nginx reload
sudo service nginx start

source env/bin/activate
pip install -r requirements.txt
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate


  ApplicationStart:
    - location: scripts/start_server
      timeout: 6000
      runas: ubuntu