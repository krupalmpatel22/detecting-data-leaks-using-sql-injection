from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from model.model import predict_sql_injection
import os
import re

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'SQLi'

app.secret_key = "KrupalPatel"

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #Query = "SELECT * FROM users WHERE UID = '" + username + "' AND Password = '" + password + "'"
        abc = username + password
        print(abc)
        is_injection_prone = predict_sql_injection(abc)
        print(f"The string '{abc}' is {'SQL injection prone' if is_injection_prone else 'not SQL injection prone'}")
        abc = "SELECT * FROM users WHERE UID = '{}' AND Password = '{}'".format(username, password)
        print(abc)
        cursor.execute(abc)
        account = cursor.fetchone()
        print(account)
        if account:
            session['loggedin'] = True
            # Use get method to avoid KeyError and provide a default value if 'id' doesn't exist
            session['id'] = account.get('id', 'default_id')
            session['username'] = account['UID']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/signup')
def signup():
    return render_template('sign_up.html')

if __name__ == '__main__':
    app.run(debug=True)
