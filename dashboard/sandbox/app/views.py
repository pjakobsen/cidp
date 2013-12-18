from flask import render_template, flash, redirect
from app import app,db, models
from app import conn
from forms import LoginForm
from models import Webuser, ROLE_USER, ROLE_ADMIN


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', 
        title = 'Sign In',
        form = form)

@app.route('/')       
@app.route('/index')
def index():
    result=conn.execute("select * from project where id in (select project_id from initiative_project where initiative_id=1)")
    print result
    entries = [{"id" : row[0], "project_number" :row[3],"project_name":row[5],"url":row[4]} for row in result.fetchall()]
    return render_template('index.html', entries=entries)

@app.route('/detail/<project_number>')
def detail(project_number):
    sql="select * from cida where project_number='{}'".format(project_number)
    print sql
    result =conn.execute(sql)
    details = [dict(row) for row in result.fetchall()]
    return render_template('detail.html', details=details)

@app.route('/users')
def show_users():
    entries = models.Webuser.query.all()
    return render_template('show_entries.html', entries=entries)