from flask import Flask,render_template,request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user

#my database connection
local_server=True
app = Flask(__name__)
app.secret_key="thrisshapatil"

#app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@Localhost/database_table_name
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/hms'
db=SQLAlchemy(app)

#here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True) 
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True) 
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

# here we will pass the end points and run the functions
@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/doctors")
def doctors():
    return render_template('doctors.html')
    
@app.route("/patients")
def patients():
    return render_template('patients.html')

@app.route("/bookings")
def bookings():
    return render_template('bookings.html')

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        # print(username,email,password)
        user=User.query.filter_by(email=email).first()
        if user:
            print("Email Already Exist")
            return render_template('/signup.html')
        else:
            encpassword=generate_password_hash(password)
            new_user = User(username=username, email=email, password=encpassword)
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html')
    else:
        return render_template('signup.html')
    

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        print(email)
    #     user=User.query.filter_by(email=email).first()
    #     print
    #     if user and check_password_hash(user.password,password):
    #         login_user(user)
    #         return redirect(url_for('/'))
    return render_template('login.html')

@app.route("/logout")
def logout():
    return render_template('login.html')


@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is connected'
    except:
        return 'My database is not connected'



app.run(debug=True)