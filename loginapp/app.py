from flask import Flask, render_template, request, redirect, session, flash, url_for
from functools import wraps
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_sample'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


# Login
@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    status = True
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["upass"]
        cur = mysql.connection.cursor()
        cur.execute("select * from users where EMAIL=%s and UPASS=%s", (email, pwd))
        data = cur.fetchone()
        if data:
            session['logged_in'] = True
            session['username'] = data["UNAME"]
            flash('Login Successfully', 'success')
            return redirect('home')
        else:
            flash('Invalid Login. Try Again', 'danger')
    return render_template("login.html")


# check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login'))

    return wrap


# signup
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    status = False
    if request.method == 'POST':
        usname = request.form["uname"]
        Name= request.form["name"]
        email = request.form["email"]
        pwd = request.form["upass"]
        mobnum = request.form["umobnum"]
        cur = mysql.connection.cursor()
        cur.execute("insert into users(UNAME,UPASS,EMAIL) values(%s,%s,%s)", (usname,Name, pwd, email,mobnum))
        mysql.connection.commit()
        cur.close()
        flash('SignUp Successfully. Login Here...', 'success')
        return redirect('login')
    return render_template("signup.html", status=status)


# Home page
@app.route("/home")
@is_logged_in
def home():
    return render_template('home.html')


# logout
@app.route("/logout")
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


@app.route("/post", methods=['POST', 'GET'])
def post():
    status = False
    if request.method == 'POST':
        Title = request.form["title"]
        Description = request.form["description"]
        Tags = request.form["tags"]
        Date = request.form["date"]
        cur = mysql.connection.cursor()
        cur.execute("insert into tags(Title, Description, Tags, Date)" "values(%s,%s,%s,%s)",(Title, Description, Tags, Date))
        mysql.connection.commit()
        cur.close()
        flash('post created...', 'success')
        return redirect('home')
    return render_template("post.html", status=status)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
