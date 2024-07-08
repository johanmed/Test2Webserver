# Build a webserver app_ml
*This repository is for building a web server to access a database locally or within the same network*  

This branch contains the original version of the web (application server) created locally  

*We use python framework **Flask** to write this webserver*

## Requirements
You will need to install the following frameworks, extension or database engine to build and run the web server:  
- flask
- flask-bootstrap
- flask-wtf
- lask-migrate
- db-sqlite3

## Instructions for use
1. Clone the repository  
2. Activate python environment **ml-env**
```
source ml-env/bin/activate
```
3. Let flask know the application file
```
export FLASK_APP=app_ml.py
```
5. Run the web server*
```
flask run
```

*Happy exploration:) !!!*
