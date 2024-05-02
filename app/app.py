from flask import Flask, render_template, request, redirect, url_for, session, render_template_string
from flask_mysqldb import MySQL
import MySQLdb.cursors
from modules.model.model import get_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'SQLi'

app.secret_key = "KrupalPatel"

mysql = MySQL(app)

@app.after_request
def add_no_cache_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        abc = "SELECT * FROM users WHERE UID = '" + username + "'"
        is_injection_prone1 = predict_injection(abc)
        print(f"The string {abc} is {'SQL injection prone' if is_injection_prone1 else 'not SQL injection prone'}")
        abc = "'" + username + "'"
        is_injection_prone2 = predict_injection(abc)
        print(f"The string {abc} is {'SQL injection prone' if is_injection_prone2 else 'not SQL injection prone'}")
        username_is_injection_prone = is_injection_prone1 and is_injection_prone2
        print(username_is_injection_prone)

        abc = "SELECT * FROM users WHERE Password = '" + password + "'"
        is_injection_prone1 = predict_injection(abc)
        print(f"The string {abc} is {'SQL injection prone' if is_injection_prone1 else 'not SQL injection prone'}")
        abc = "'" + password + "'"
        is_injection_prone2 = predict_injection(abc)
        print(f"The string {abc} is {'SQL injection prone' if is_injection_prone2 else 'not SQL injection prone'}")
        password_is_injection_prone = is_injection_prone1 and is_injection_prone2

        is_injection_prone = password_is_injection_prone or username_is_injection_prone
        print("Final Output : ", is_injection_prone)

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
    print(msg)
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        # Assuming 'username' is stored in the session when the user logs in
        username = session['username']
        print(username)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customers WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            user['profile_image'] = 'https://bootdey.com/img/Content/avatar/avatar1.png'
            user['dob'] = user['dob'].strftime('%Y-%m-%d')
            print(user)
            return render_template('profile.html', user=user)
        else:
            return 'User not found', 404
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'loggedin' in session:
        #create_database()
        results = []
        cursor = mysql.connection.cursor()
        try:
            sql_query = "SELECT * FROM products"
            cursor.execute(sql_query)
            results = cursor.fetchall()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            cursor.close()

        return render_template('home.html', results=results, username=session['username'])
    return redirect(url_for('login'))

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'repassword' in request.form and 'mailId' in request.form and 'phoneNo' in request.form and 'dob' in request.form :
        username = request.form['username']
        password = request.form['password']
        mailId = request.form['mailId']
        phoneNo = request.form['phoneNo']
        dob = request.form['dob']
        print("INSERT INTO Customers (username, password, mail_id, phone_no, dob) VALUES ('{}', '{}', '{}', '{}', '{}')".format(username, password, mailId, phoneNo, dob))
        cursor = mysql.connection.cursor()
        account = cursor.execute("INSERT INTO customers (username, password, mail_id, phone_no, dob) VALUES ('{}', '{}', '{}', '{}', '{}')".format(username, password, mailId, phoneNo, dob))
        mysql.connection.commit()
        if account:
            msg = "user data added into database."
        else:
            msg = "User was not created."
        return render_template('login.html', msg=msg)
    return render_template('sign_up.html')


@app.route('/search')
def search():
    msg = ''
    query = request.args.get('query', '')  # Default to empty string if no query
    results = []
    if query:  # Only execute search if there's a query
        cursor = mysql.connection.cursor()
        try:
            is_injection_prone = predict_injection(query)
            if not is_injection_prone:
                sql_query = "SELECT * FROM products WHERE name LIKE %s"
                like_pattern = f"%{query}%"
                cursor.execute(sql_query, (like_pattern,))
                results = cursor.fetchall()
            else:
                msg = f"{query} is SQL injection Prone."
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            cursor.close()

    return render_template('home.html', query=query, results=results, msg=msg)

def create_database():
    print("creating search table")
    cursor = mysql.connection.cursor()

    # Create table
    #cursor.execute('''CREATE TABLE products
    #             (id INTEGER PRIMARY KEY, name TEXT, description TEXT, price REAL)''')

    # Insert some sample data
    products = [
        (1, 'Laptop', 'A personal computer for mobile use.', 1200.00),
        (2, 'Smartphone', 'A mobile phone with advanced features.', 800.00),
        (3, 'Tablet', 'A portable personal computer with a touchscreen.', 450.00)
    ]

    for p in products:
        cursor.execute('INSERT INTO products (id, name, description, price) VALUES (%s,%s,%s,%s)', p)

    # Save (commit) the changes and close the connection
    mysql.connection.commit()


def create_model():
    global model, tokenizer
    model, tokenizer = get_model()

def predict_injection(text):
    sequence = tokenizer.texts_to_sequences([text])

    padded = pad_sequences(sequence, maxlen=100, padding='post')
    prediction = model.predict(padded)
    return prediction[0][0] > 0.8  # Returns True if SQL injection prone, False otherwise

if __name__ == '__main__':
    create_model()
    app.run(host="0.0.0.0", port=5000, debug=True)
