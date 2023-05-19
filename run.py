from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import json
import MySQLdb.cursors
import re
from forms import UserInfoForm
from wtforms import TextField, BooleanField
from wtforms.validators import Required
from wtforms import StringField

import algo

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'abcd'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'nutridiet'

mysql = MySQL(app)


@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_login WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:

        email = request.form['email']
        username = request.form['username']
        password = request.form['password']



        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_login WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user_login (username, email, password) VALUES ( % s, % s, % s)', ( username, email, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


with open('config.json', 'r') as c:
    params = json.load(c)["params"]
local_server = True

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class Contact(db.Model):
    '''sno, name, email, phone_num,msg, date'''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String, nullable=False)


class User_login (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
# class User(db.Model):
#     loginid= db.Column(db.Integer, primary_key=True)
#
#     id= db.Column(db.Integer, nullable=False)
#     Status= db.Column(db.String, nullable=False)
#     med_history= db.Column(db.String, nullable=False)
#     age= db.Column(db.Integer, nullable=False)
#     Gender = db.Column(db.String, nullable=False)
#     Height = db.Column(db.Float, nullable=False)
#     weight = db.Column(db.Float, nullable=False)
#     BMI = db.Column(db.Float, nullable=False)


@app.route("/index")
def index():
    return render_template('index.html', params=params)


@app.route('/home',methods=['GET','POST'])
def home():
	form=UserInfoForm()
	if form.validate_on_submit():
		if request.method=='POST':
			name=request.form['name']
			weight=float(request.form['weight'])
			height=float(request.form['height'])
			age=int(request.form['age'])
			gender=request.form['gender']
			phys_act=request.form['physical_activity']

			tdee=algo.calc_tdee(name,weight,height,age,gender,phys_act)
			return redirect(url_for('result',tdee=tdee))

	return render_template('home.html',title="Diet App",form=form)

@app.route('/result',methods=['GET','POST'])
def result():
	tdee=request.args.get('tdee')
	if tdee is None:
		return render_template('error.html',title="Error Page")
	
	tdee=float(tdee)
	breakfast= algo.bfcalc(tdee)
	snack1=algo.s1calc(tdee)
	lunch=algo.lcalc(tdee)
	snack2=algo.s2calc(tdee)
	dinner=algo.dcalc(tdee)
	snack3=algo.s3calc(tdee)
	return render_template('result.html',title="Result",breakfast=breakfast,snack1=snack1,lunch=lunch,snack2=snack2,dinner=dinner,snack3=snack3)

@app.route("/about")
def About():
    return render_template('about.html', params=params)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone_num = request.form.get('phone_num')
        msg = request.form.get('msg')
        '''sno, name, email, phone_num,msg, date'''

        entry = Contact(name=name, phone_num=phone_num, msg=msg, email=email)
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html', params=params)


@app.route("/ques", methods=['GET', 'POST'])
def ques():
    # if (request.method == 'POST'):
    #     age= request.form.get('age')
    #     Gender= request.form.get('Gender')
    #     Height= request.form.get('Height')
    #     weight= request.form.get('weight')
    #     BMI = request.form.get('BMI')
    #     entry = User (age=age, Gender= Gender, Height= Height,weight= weight, BMI= BMI )
    #     db.session.add(entry)
    #     db.session.commit()
    if request.method == 'POST' and 'age' in request.form and 'Gender' in request.form and 'Height' in request.form and 'weight' in request.form and 'BMI' in request.form:
        age = request.form['age']
        Gender = request.form['Gender']
        Height= request.form['Height']
        weight = request.form['weight']
        BMI = request.form['BMI']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO user (age, Gender, Height, weight, BMI) VALUES ( % s, % s, % s, %s, %s)',
                       (age, Gender, Height, weight, BMI))
        mysql.connection.commit()
        account = cursor.fetchone()


    return render_template('ques.html', params=params)


app.run(debug=True)
