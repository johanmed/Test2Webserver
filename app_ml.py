#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired
from flask_migrate import Migrate
from datetime import datetime
import os
import sqlite3

# Making configurations
app=Flask(__name__)
bootstrap=Bootstrap(app)
moment=Moment(app)
app.config['SECRET_KEY']='My second webserver, you cannot guess its secret key'


class DatabaseDiabetesImmuneMicrobiome():
    """
    Models database of traits and their relationships
    3 tables: Diabetes, ImmuneSystem, GutMicrobiome
    Attributes: name (string), file (string)
    """
    def __init__(self, name, file):
        self.name=name
        self.file=file
        
    def create_database(self):
        con=sqlite3.connect(self.file)
        con.execute("CREATE TABLE IF NOT EXISTS Diabetes (diabetes_id INTEGER PRIMARY KEY, type INTEGER, diabetes_trait TEXT UNIQUE)")
        con.execute("CREATE TABLE IF NOT EXISTS ImmuneSystem (immune_id INTEGER PRIMARY KEY, immune_trait TEXT, diabetes_id INTEGER UNIQUE)")
        con.execute("CREATE TABLE IF NOT EXISTS GutMicrobiome (microbiome_id INTEGER PRIMARY KEY, microbiome_trait TEXT, diabetes_id INTEGER UNIQUE)")
        con.commit()
        con.close()
    

    def populate_database(self):
        con=sqlite3.connect(self.file)
        con.execute("INSERT INTO Diabetes VALUES (1, 1, 'insulin concentration')")
        con.execute("INSERT INTO Diabetes VALUES (2, 2, 'glycemia')")
        con.execute("INSERT INTO Diabetes VALUES (3, 2, 'lipidemia')")
        con.execute("INSERT INTO Diabetes VALUES (4, 1, 'obesity')")
        con.execute("INSERT INTO Diabetes VALUES (5, 1, 'isulin activity')")
        con.execute("INSERT INTO ImmuneSystem VALUES (1, 'T cells number', 2)")
        con.execute("INSERT INTO ImmuneSystem VALUES (2, 'cytokine concentration', 3)")
        con.execute("INSERT INTO ImmuneSystem VALUES (3, 'macrophage number', 1)")
        con.execute("INSERT INTO ImmuneSystem VALUES (4, 'B cells numbers', 4)")
        con.execute("INSERT INTO ImmuneSystem VALUES (5, 'complement system activity', 5)")
        con.execute("INSERT INTO GutMicrobiome VALUES (1, 'Escherichia abundance', 1)")
        con.execute("INSERT INTO GutMicrobiome VALUES (2, 'Akksermania abundance', 5)")
        con.execute("INSERT INTO GutMicrobiome VALUES (3, 'Clostridiales abundance', 4)")
        con.execute("INSERT INTO GutMicrobiome VALUES (4, 'Firmicutes abundance', 3)")
        con.execute("INSERT INTO GutMicrobiome VALUES (5, 'Proteobacter abundance', 2)")
        con.commit()
        con.close()

db=DatabaseDiabetesImmuneMicrobiome('database for study', 'diabetes_immune_microbiome.db')
db.create_database()
db.populate_database()

migrate=Migrate(app, db)

class DatabaseUser():
    """
    Stores users info
    Attributes: name, file (string), usernames (String),
    """
    def __init__(self, name, file, username1, username2, username3, username4, username5):
        self.name=name
        self.file=file
        self.username1=username1
        self.username2=username2
        self.username3=username3
        self.username4=username4
        self.username5=username5
    
    def create_database(self):
        con=sqlite3.connect(self.file)
        con.execute("CREATE TABLE IF NOT EXISTS Users (username TEXT UNIQUE)")
        con.commit()
        con.close()
    
    def get_users(self):
        return [self.username1, self.username2, self.username3, self.username4, self.username5]

# setting up users database
users=DatabaseUser('database of users', 'database_users.db', 'Johannes', 'Paul', 'Pjotr', 'Felix', 'Darnell')
users.create_database()

# Web form for name input of user
class NameForm(FlaskForm):
    name=StringField("Username", validators=[DataRequired()])
    password=StringField("Password")
    submit=SubmitField("Submit")
    
    
# Web form for user query
class DiabetesImmuneMicrobiome(FlaskForm):
    type_diabetes=IntegerField("In what diabetes type are you interested in?", validators=[DataRequired()])
    immune_or_microbiome=StringField("Immune System or Gut Microbiome?", validators=[DataRequired()])
    query=SubmitField("Submit")


# View function for initial request and authentification
@app.route('/', methods=['GET', 'POST'])
def home():
    name_form=NameForm()
    var=name_form.name.data
    passw=name_form.password.data
    if name_form.validate_on_submit():
        if var in users.get_users() and passw == 'default':
            return redirect(url_for('verified'))
    return render_template('home.html', name_form=name_form)
        
 
# View function for query entering
@app.route('/verified', methods=['GET', 'POST'])
def verified():
    query_form=DiabetesImmuneMicrobiome()
    var=query_form.immune_or_microbiome.data
    if query_form.validate_on_submit():
        if var=='immune' or var=='immune system':
            type_interest=query_form.type_diabetes.data
            connection= sqlite3.connect('diabetes_immune_microbiome.db')
            con=connection.cursor()
            con.execute("SELECT ImmuneSystem.immune_trait FROM ImmuneSystem, Diabetes WHERE Diabetes.type==? AND Diabetes.diabetes_id==ImmuneSystem.diabetes_id", (type_interest,))
            data=con.fetchall()
            return render_template('diabetes_immune.html', data=data, current_time=datetime.utcnow())
        elif var=='microbiome' or var=='gut microbiome':
            type_interest=query_form.type_diabetes.data
            connection= sqlite3.connect('diabetes_immune_microbiome.db')
            con=connection.cursor()
            con.execute("SELECT GutMicrobiome.microbiome_trait FROM GutMicrobiome, Diabetes WHERE Diabetes.type==? AND Diabetes.diabetes_id==GutMicrobiome.diabetes_id", (type_interest,))
            data=con.fetchall()
            return render_template('diabetes_microbiome.html', data=data, current_time=datetime.utcnow())
        else:
            return render_template('info_unavailable.html')
    return render_template('verified.html', query_form=query_form)



# View function to customize page of 'Page Not found' error
@app.errorhandler(404)
def missing_page(e):
    return render_template('404.html'), 404
    
    
    
# view function to customize page of 'Internal Server Error'
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


