# Datamite
This Django website offers a service to manage your KPIs/metrics within your strategies. It will then use an ANP-AHP method to compute the weights used to compute the KPIs/metrics that depend on others, the different Balanced Scorecard (BSC) perspectives, and your main strategy.


# Acknowledgements
This website benefited from the financial support of the European Commission under Grant number 101092989, the Science Foundation Ireland under Grant numbers 12/RC/2289-P2,16/RC/3918, and 18/CRT/6223, which are co-funded under the European Regional Development Fund.


# Use Docker for the service
First, you need to set your environment correctly. Copy `.env.template`, rename it to `.env` and set the values you want in there. All the instructions required for setting up the environment should be present in `.env.template`. In particular, note that some environment variables are mandatory and the whole thing will exit automatically if at least one of the mandatory variable was not set. Consult the logs to know what went wrong in your setup.

To build the service image:
```
docker build -t anpahp_container . # --no-cache if you want to force a rebuild (new schema for instance)
```

Start the service with Docker:
```
docker compose up
```
With the way the `docker-compose.yml` file is configured, any change in the code, the DB, etc, will be reflected in both the container and locally. You don't need to rebuild the image every time you do changes. It will prevent the DB from being reset everytime you commit new changes because it keeps it between different runs.

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
The script uses CSV files in 'ANPAHP/data' to populate the database with the Datamite data.
This script provides logs to help you identify errors in the input CSVs.

The CSVs should have the following:
- A header with the names of the fields as they are in the DB model.
- If a field is a foreign key, then it expects the primary key (e.g., BSCSubfamily has a BSCFamily as a foreign key, and BSCFamily's primary key is its unique name, so the CSV for BSCSubfamilies expect to find an existing BSCFamily name).
- If a field is a ManyToManyField, then it expect either nothing (empty string, meaning no connection), a single value, or a list of values (in the form of a JSON list OR as comma-separated values). The provided values need to correspond to the primary key of the model linked here.


# Create and populate the knowledge base for the RAG system
If you have setup your `.env` file properly, creating the knowledge base can be done by simply using the following command:
```
python manage.py runscript create_knowledge
```

This will automatically search the folders that you set in `KNOWLEDGE_FOLDERS`. If you want to search more folders, just add them to this environment variable, separated by commas. If you need more types of files to be processed, you can implement your own file processors in `ANPAHP/rag/knowledgebase/file_processors.py`. Follow the already existing processors. If you need to pass specific arguments to your processors, have a look at `ANPAHP/script/create_knowledge.py`, in particular `create_knowledge_base()` and add your specific arguments to be passed as it is already done for .csv and .pdf files.


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

NOTE: The unit tests are not up to date right now.


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
* Refactor code to make it easier to change the order or add new steps.
* Add a slug to evaluations so it can be used for the URI instead of the ID.
* Add a warning message if one of the selected BSC families has no KPIs/metrics selected.
* Improve the generated report: better format, better section/subsection separation, better colour theme for the pie charts.
* Add the possibility to download an Excel sheet with the supermatrix, the limiting supermatrix, and the automatic computation of KPIs based on measured KPIs/metrics.
* Add the knowledge base pages with a main page referencing all the pages.
* Add a search functionality to the website.
* Better integrate the taxonomy from D4.2 (add the diagrams into the KB, and add the relationships as predefined relationships in the intermetrics relationships).