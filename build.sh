#!/usr/bin/env bash
pip install django
pip install django-otp
pip install django-cors-headers
pip install requests
pip install django-crispy-forms
pip install crispy-bootstrap5
pip install python-dotenv
pip install google-api-python-client
pip install whitenoise
pip install gunicorn
pip install cryptography
pip install PyJWT
pip install boxsdk
pip install PyPDF2
pip install reportlab
pip install python-dateutil
pip install GitPython
pip install pandas
pip install -r requirements.txt
python OPI_Signup/manage.py collectstatic --noinput
python -c"import OPI_Signup.myapp.box_api.box_api; OPI_Signup.myapp.box_api.box_api.sync_db_w_box(OPI_Signup.myapp.box_api.box_api.create_client())"
python OPI_Signup/manage.py migrate
python OPI_Signup/manage.py makemigrations
python OPI_Signup/manage.py loaddata OPI_Signup/myapp/box_api/fixtures.json

#this will erase the dblite