pip install -r requirements.txt

python manage.py collectstatic

python manage.py runserver 0.0.0.0:8000

GOTO http://localhost:8000/static/index.html (turn on devtools to check logs)

TO RUNNING ON YOUR OWN DATA. Place your data at convert2lexical/data.json (your data must be list of json format)

REOPEN http://localhost:8000/static/index.html
