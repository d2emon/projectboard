#! /bin/bash
python src/manage.py fakeuser --count=100
python src/manage.py fakeproject --count=150
python src/manage.py fakeinvite --count=150
python src/manage.py faketodo --count=100
python src/manage.py fakenotice --count=100
