from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from modules.model.model import predict_sql_injection

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
        abc = "SELECT * FROM users WHERE UID = '" + username + "'"
        print(abc)
        is_injection_prone1 = predict_sql_injection(abc)
        print(f"The string {abc} is {'SQL injection prone' if is_injection_prone1 else 'not SQL injection prone'}")
        abc = "'" + username + "'"
        print(abc)
        is_injection_prone2 = predict_sql_injection(abc)
        print(f"The string {abc} is {'SQL injection prone' if is_injection_prone2 else 'not SQL injection prone'}")
        is_injection_prone = is_injection_prone1 and is_injection_prone2
        print(is_injection_prone)
        if not is_injection_prone:
            abc = "SELECT * FROM users WHERE UID = '{}' AND Password ='{}'".format(username, password)
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
        else:
            msg = "That is SQL injection Prone"
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

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'repassword' in request.form and 'mailId' in request.form and 'phoneNo' in request.form and 'dob' in request.form :
        pass
    return render_template('sign_up.html')

if __name__ == '__main__':
    app.run(debug=True)
