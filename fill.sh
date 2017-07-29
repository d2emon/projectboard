#! /bin/bash
python manage.py fakeuser --count=100
python manage.py fakeproject --count=150
python manage.py fakeinvite --count=150
python manage.py faketodo --count=100
python manage.py fakenotice --count=100
