from flask_mysqldb import MySQL
from flask import *
import MySQLdb.cursors
import re
import datetime

app = Flask(__name__)
 
 
app.secret_key = 'ashghfghdhshfh133772'
 
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'G@nesh24'
app.config['MYSQL_DB'] = 'blog_portal'
 
 
mysql = MySQL(app)

def mapUsertoPost(num):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT userid FROM post WHERE postid = %s', (num, ))
    data = cursor.fetchone()
    if data["userid"] != session.get("userid"):
        return True
    else:
        return False


@app.route("/delete/<int:num>", methods=["GET"])
def delete(num):
    if session.get("loggedin") == False or mapUsertoPost(num):
        return redirect(url_for("login"))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(''' Delete from post where postid = %s''',(num,))
    mysql.connection.commit()
        
    return redirect(url_for("list_blogs"))




@app.route("/modify/<int:num>", methods=["GET", "POST"])
def modify(num):
    
    if session.get("loggedin") == False or mapUsertoPost(num):
        return redirect(url_for("login"))
    postid = session.get("postid")
    title = session.get("title")
    category = session.get("category")
    if request.method == "POST":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        content=request.form["content"]
        updated = datetime.date.today().strftime("%Y-%m-%d")
        cursor.execute(''' Update post set  body = %s, updated=%s where postid = %s
        ''',(content, updated, postid))
        mysql.connection.commit()
        return redirect(url_for("list_blogs"))
    return render_template("modify.html", **locals())

@app.route("/blogs")
def list_blogs():
    if session.get("loggedin") == False:
        return redirect(url_for("login"))
    user_id = int(session.get("userid"))
    print(user_id)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT postid, title, updated, categoryname FROM post WHERE userid = %s', (user_id, ))
    data = cursor.fetchall()
    final_data = [[i['postid'],i['title'], i['updated'].date().strftime("%Y-%m-%d"), i["categoryname"] ] for i in data]
    print(final_data)
    return render_template("list.html", **locals())

@app.route("/blogs/<int:num>")
def view(num):
    if session.get("loggedin") == False or mapUsertoPost(num):
        return redirect(url_for("login"))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM post WHERE postid = % s', (num, ))
    data = cursor.fetchone()
    title = data["Title"]
    postid = num
    session["postid"] = num
    session["title"] = title
    category = data["categoryname"]
    session["category"] = category
    content = data["body"]
    Author = session.get("username")
    Published = data["published"].date().strftime("%Y-%m-%d")
    Updated = data["updated"].date().strftime("%Y-%m-%d")
    return render_template("view.html", **locals())

@app.route("/add_blog", methods=["POST", "GET"])
def addblog():
    if session.get("loggedin") == False:
        return redirect(url_for("login"))
    if request.method == "POST":
        title=request.form["titlename"]
        category=request.form["categoryname"]
        content=request.form["content"]
        published = datetime.date.today().strftime("%Y-%m-%d")
        updated = datetime.date.today().strftime("%Y-%m-%d")
        userid = session.get("userid")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''insert into post(Title, body,published, updated, userId, categoryname) 
                        values(%s,%s,%s,%s,%s,%s)''',(title, content, published, updated, userid, category))
        mysql.connection.commit()
        return redirect(url_for("list_blogs"))
        
    return render_template("add.html")
    
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            msg = '<p class="text-danger">Account already exists !</p>'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = '<p class="text-danger">Invalid email address !</p>'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = '<p class="text-danger">name must contain only characters and numbers !</p>'
        else:
            cursor.execute('INSERT INTO user(username, email, password) VALUES (% s, % s, % s)', (username, email, password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return redirect(url_for("login"))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)


@app.route("/")
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ""
    session["loggedin"] = False
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        print(account)
        if account:
            session["username"] = account["username"]
            session["userid"] = account["userid"]
            session["loggedin"] = True
            return redirect(url_for('list_blogs'))
            
        else:
            msg = "<p class='text-danger'>Check Email and password</p>"
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('login.html', msg = msg)

@app.route("/logout")
def logout():
    session["loggedin"] = False
    session.pop('username', None)
    session.pop('userid', None)
    session.pop('postid', None)
    session.pop('title', None)
    session.pop('category', None)
    return redirect(url_for("login"))



# @app.route("/welcome", methods = ["GET", "POST"])
# def welcome():
#     #print(session.get("loggedin"))
#     if session.get("loggedin"):
#         return f"Welcome {session.get('username')}"
#     else:
#         #print("Here")
#         return redirect(url_for('login'))

app.run(debug = True)
