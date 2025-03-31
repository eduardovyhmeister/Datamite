# Datamite
datamite ANPAHP


# Fill up the database with metrics and KPIs
The project has a script to import all the metrics and KPIs into the database.
To import, simply run the following command:
```
cd foldername/
python manage.py runscript loadANPAHP
```


# Run unit tests
The project has unit tests. To run them, run the following commands:
```
cd foldername/
python manage.py test ANPAHP
```

If you want to generate a 'coverage' (use 'pip' to install this package) report, you can instead use:
```
cd foldername/
python -m coverage run --source='.' manage.py test ANPAHP
python -m coverage report
```
