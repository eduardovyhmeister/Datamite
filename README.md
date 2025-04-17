# Datamite
datamite ANPAHP


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

If you want to generate a 'coverage' (use 'pip' to install this package) report, you can instead use:
```
cd foldername/
python -m coverage run --source='.' manage.py test
python -m coverage report
```

# TODOs
Here is a list of stuff that could be done to improve this project:
* Redo the unit tests for the new version of the code.
* Change the theme used by Bootstap to fit the identity of DATAMITE.
* Improve the overall visual of the website.