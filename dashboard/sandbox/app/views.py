# encoding: utf-8
from flask import render_template, flash, redirect,jsonify, Response,url_for
from app import app,db, models
from app import conn
from forms import LoginForm
from models import Webuser, ROLE_USER, ROLE_ADMIN
import cubes
from petl import *
from pprint import pprint


MODEL_PATH = "model.json"
DB_URL = "sqlite:///data.sqlite"
CUBE_NAME = "irbd_balance"

# Some global variables. We do not have to care about Flask provided thread
# safety here, as they are non-mutable.

workspace = None
model = None

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', 
        title = 'Sign In',
        form = form)

@app.route('/')       
@app.route('/index')
def index():
    #return render_template('index.html')
    return redirect(url_for('static', filename='index.html'))
def index2():
    result=conn.execute("select * from project where id in (select project_id from initiative_project where initiative_id=1)")
    print result
    entries = [{"id" : row[0], "project_number" :row[3],"project_name":row[5],"url":row[4]} for row in result.fetchall()]
    return render_template('index.html', entries=entries)

@app.route("/dim")
@app.route("/dim/<dim_name>")
def report(dim_name=None):
    return "Hello " + str(dim_name)
    
@app.route('/mnch.csv')
def generate_full_csv():
    sql = "select full_project_number from project where id in (select project_id from initiative_project where initiative_id=1)"
    table = fromdb(conn, sql)
    pn = itervalues(table, 'full_project_number')
    fields="fiscal_year, project_number, title, country, maximum_cida_contribution, amount_spent"
    ids = [p for p in pn]
    id_strings = "'"+"','".join(ids)+"'"
    sql = "select {} from cida where project_number in ({})".format(fields,id_strings)
    
    table = fromdb(conn, sql)

    def generate():
        yield  "Year, Code, title, Country, Max, Spent\n"

        for row in iterdata(table):
            print row
            l = [unicode(x).encode('utf-8','xmlcharrefreplace') for x in list(row)]
            line =  '","'.join(l)
            yield '"' + line + '"\n'
    return Response(generate(), mimetype='text/html')
    
@app.route('/data/mnch.csv')
def static_csv():
     return redirect(url_for('static', filename='data/mnch.csv'))
    
def mnch():
    sql = "select * from project where id in (select project_id from initiative_project where initiative_id=1)"
    table = fromdb(conn, sql)
    table = cut(table, 'id','project_number')
    return tocsv(table)
    entries = [{"id" : row[0], "project_number" :row[3],"project_name":row[5],"url":row[4]} for row in result.fetchall()]
    return jsonify(result=entries) 

@app.route('/mnch')
@app.route('/mnch/<viz_type>')
def mnch(viz_type='table'):
    d ='https://docs.google.com/spreadsheet/pub?key=0AjcBMksBg7kEdHRrZXc3TG1qUHBZekdPdXdvX1BodUE&single=true&gid=0&output=csv'
    if viz_type=='table':
        return render_template('recline.html',
        title='Maternal, Newborn, and Child Health Initiative - Table',
        data=d
        )
    elif viz_type == 'graph':
        return render_template('recline_graph.html',
        title='Maternal, Newborn, and Child Health Initiative - Graph',
        data=d
        )
    else: 
        return  "error"
   
@app.route('/browser')
def browser():
    return render_template('recline_all.html', title='All Projects',
 datasource='https://docs.google.com/spreadsheet/pub?key=0AjcBMksBg7kEdG8ycU15bC1WRU9OYkhmbzBxaXIyd1E&single=true&gid=0&output=csv')

@app.route('/agencies')
def agencies():
    return render_template('recline.html', title='Agency Involvment',
    data='https://docs.google.com/spreadsheet/pub?key=0AjcBMksBg7kEdG8ycU15bC1WRU9OYkhmbzBxaXIyd1E&single=true&gid=0&output=csv')

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