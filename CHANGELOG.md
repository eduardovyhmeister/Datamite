# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Added a script (clean_csv_from_json) to get rid of JSON lists from the a CSV file and replacing them with comma-separated values instead for format consistency.

### Fixed
- Fixed an redirection issue that prevented the creation of new KPIs.

### Changed
- Entering notes on your evaluation and validating now brings you to step 1.
- 'populate_db.py' now acceps empty values or single values in the JSONFields.
- Updated the content of KPIs.csv with new information.


## v2.0.2

### Fixed
- Fixed an issue when defining no intermetrics dependencies.


## v2.0.1

### Fixed
- Fixed an issue in the report generation when a BSC family was not set to 0 but had no KPI selected.


## v2.0.0

### Fixed
- Fixed the computation of the supermatrix and the limiting supermatrix.
- Fixed the report generation to make it more readable and with the useful data.
- Fixed the docker files to make it more production ready (will need to use gunicorn or nginx if we want to make it clean for production).
- Fixed the security issue with no actual secure key being used.
- Fixed the .gitignore that was preventing some static files from being copied properly in the Docker image.
- Fixed URLs to be more consistent.
- Fixed the favicon (i.e. the icon appearing in your tab on your browser) to use the DATAMITE logo instead.

### Added
- Added our own ANP library to not rely on an external library that was old and unmaintained.
- Added a custom logger (used in the populate_db file) to provide clean logs.
- Added some unit tests (will need to be completed eventually).
- Added a ton of documentation for most things, making it easier to understand, maintain and improve the code.
- Added warning and error messages to the steps in something might be wrong.
- Added ticks when a step has been completed for the user to know that it has been completed.
- Added that redoing certain steps will reset some following ones (e.g. reselecting KPIs/metrics will reset the preferences so the user has to set them again) thus preventing inconsistent evaluation states.
- Added the possibility to remove created objectives and KPIs/metrics (you could create them but not delete them before).
- Added the forms for the preference/importance selection through sliders + text number inputs. 
- Added a README with instructions on how to use this repo.
- Added this CHANGELOG to keep track of changes.

### Changed
- Changed the look of the website (e.g. with cleaner logos).
- Changed most models to include more information, in a cleaner schema.
- Rewrote the entire populate_db script to make it more generic and capable of handling all we need for out DB. It also generate readable logs that show immediately if something's wrong with the data files.
- Changed the steps, in particular the pairwise-comparison steps for a slider-based preference selection that prevents the possibility for inconsistencies/errors in the user's input.
- Changed the result report to make it easier to read and understand: new graph type (pie chart instead of a spider graph), and separated insights for the overall strategy, the BSC perspectives, and the KPIs/metrics that depend on others.
- Changed the content of the "How to" and "About" pages to make them clearer.
- The code structure has been completely overhauled with models, views, and forms in their own subpackages, each one containing multiple files to prevent having everything into 1 big file every time.
- Changed the custom templates to replace them by a single one that does the same thing.
- Changed the steps' templates to make them simpler and let code heavy.
- Changed the step in which you could select links between KPIs/metrics to make it much more accessible and readable.
- Changed models 'save()' method to be more consistent in what it is actually saving, in particular by enforcing validators to be run again when saving (this is not a default behaviour for some reason).
- Changed the views to make them clearer (no more partially computing the supermatrix all over the place), and more consistent in what they are doing: a link between the data and the templates.

### Removed
- Removed criteria from steps since they were not used in the overall evaluation (they are still in the code base if we want to include them in a future version though).
- Removed all the unused code files, HTML templates, etc.
- Removed a lot of dependencies that were unnecessary.
- Removed a lot of code that was unused (old views, utility functions, etc.).
- Removed all the ALTAI content that had no place in here.