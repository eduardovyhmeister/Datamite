# Datamite
datamite ANPAHP


# Use Docker for the service
First, you need to setup a secure secret key for Django to use. To generate a key, you can use:
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Set it as "DJANGO_SECRET_KEY" in your environment variables. On Linux, you can set it in your `.bashrc` by adding the following line:
```
export DJANGO_SECRET_KEY="my_secret_key_I_generated
```
And finally, DO NOT FORGET TO CHANGE `datamite/settings.py`, change the following lines:
```
SECRET_KEY = 'django-insecure-a52&$)8&u8^hqrov$ndwp1oaie-y(@*gi)i2b#j%6s_hkul%75'
#SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = True
#DEBUG = bool(int(os.environ.get('DEBUG',0)))
```
to:
```
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = bool(int(os.environ.get('DEBUG',0)))
```


To build the service image:
```
docker build .
```

Start the service with Docker:
```
docker compose up
```

Stop the service:
```
docker ps # To get the ID
docker stop id
```


# Reset the database
If you made changes to the models that might not be compatible with the current schema (e.g. modifying the name/type of column), then you can recreate the database by using the following commands:
```
cd foldername/
rm db.sqlite3
rm ANPAHP/migrations/*
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations ANPAHP
python manage.py migrate ANPAHP
```
If you do this, you need to repopulate the DB.


# Populate the database
The project has a script to import all the metrics and KPIs into the database.
To import, simply run the following command:
```
cd foldername/
python manage.py runscript populate_db
```
The script uses CSV files in 'static/mine' to populate the database with the Datamite data.


# Run unit tests
The project has unit tests. To run them, run the following commands:
```
cd foldername/
python manage.py test
```

If you want to generate a 'coverage' (use `pip` to install this package) report, you can instead use:
```
cd foldername/
python -m coverage run --source='.' manage.py test
python -m coverage report
```

# Checklist of things to do when adding code
Here is a checklist of things to not forget if you add code:
* **If you add a step to the ANP-AHP process:** add a view (in views/steps/), add a form (if forms/, if necessary), add/update the models (to store the new info, in particular in Evaluation), add the required HTML templates (in templates/), add the link to the page to the step list on the left by adding it to `templates/ANPAHP/Shared/_survey.html`.
* **If you add/update a model:** don't forget to rerun `python manage.py makemigration` and `python manage.py migrate`.
* **If you add a new view file:** add it to the `__init__.py` of the corresponding folder, as the others, to keep imports short. Don't forget to also add it to `urls.py` to make it accessible.
* **If you add a model:** add it to `models/__init__.py` like other models.
* **If you add a form:** add it to `forms/__init__.py` like other forms.


# TODOs
Here is a list of stuff that could be done to improve this project:
* Redo the unit tests for the new version of the code.
* Change the theme used by Bootstap to fit the identity of DATAMITE.
* Improve the overall visual of the website.
* Refactor code of similar steps (e.g. preference steps use very similar code).
* Refactor code to make it easy to change the order or add new steps.
* Add a slug to evaluations so it can be used for the URI instead of the ID.