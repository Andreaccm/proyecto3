from logging import debug
from flask import Flask, render_template, request, session, logging,url_for, redirect,flash
import re
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'proyecto3python'

DB_HOST = 'localhost'
DB_NAME = 'python'
DB_USER = 'postgres'
DB_PWD  = 'admin'

conn = psycopg2.connect(host = DB_HOST, dbname = DB_NAME, user = DB_USER, password = DB_PWD)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'], email=session['email'])
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    if request.method == 'POST' and 'email' in request.form and 'pwd' in request.form:
        Email = request.form['email']
        pwd = request.form['pwd']
        print(pwd)
        
        cursor.execute('SELECT * FROM Username WHERE email = %s', (Email,))
        account = cursor.fetchone()
 
        if account:
            password_rs = account['pwd']
            print(password_rs)
           
            if check_password_hash(password_rs, pwd):
                
                session['loggedin'] = True
                session['email'] = account['email']
                session['username'] = account['username']
    
                return redirect(url_for('home'))
            else:
                flash('Incorrect username/password')
        else:
            flash('Incorrect username/password')
 
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'email' in request.form and 'user' in request.form and 'pwd' in request.form:
        Email = request.form['email']
        User = request.form['user']
        Pwd = request.form['pwd']      

        _hash_password = generate_password_hash(Pwd)

        print(Email)
        print(User)
        print(Pwd)
        print(_hash_password)

    if request.method == 'POST' and 'email' in request.form and 'user' in request.form and 'pwd' in request.form:
      
        Email = request.form['email']
        User = request.form['user']
        Pwd = request.form['pwd']
    
        _hashed_password = generate_password_hash(Pwd)
 
        cursor.execute('SELECT * FROM Username WHERE email = %s', (Email,))
        account = cursor.fetchone()
        print(account)
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', User):
            flash('Username must contain only characters and numbers!')
        elif not User or not Pwd or not Email:
            flash('Please fill out the form!')
        else:
            cursor.execute("INSERT INTO Username (email, username, pwd) VALUES (%s,%s,%s)", (Email, User, _hashed_password))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
     
        flash('Please fill out the form!')
    
    return render_template('register.html')
   
   
@app.route('/logout')
def logout():
   
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)

   return redirect(url_for('login'))
  
@app.route('/profile')
def profile(): 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM users WHERE email = %s', [session['email']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug = True) 
