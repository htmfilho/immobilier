#!/bin/bash
source immovenv/bin/activate
python manage.py runserver
firefox http://127.0.0.1:8000/

