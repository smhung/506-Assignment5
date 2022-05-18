from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,DateField,IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange
from yelp import find_coffee
from flask_login import current_user, login_user, login_required, logout_user
from models import db, login, UserModel
from wiki import findBirths

class loginForm(FlaskForm):
    username=StringField(label="Enter username", validators=[DataRequired(), Length(min=6,max=20)])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=8)])
    submit=SubmitField(label="Login")

class LandingPage(FlaskForm):
    date = DateField('Please enter date: ')
    number = IntegerField('Please enter number of entries desired: ',validators=[NumberRange(min=1, max=20, message='Please enter an integer between 1 and 20. ')], default=10)
    submit=SubmitField(label="Search")

class registerForm(FlaskForm):
    username=StringField(label="Enter username", validators=[DataRequired(),Length(min=6,max=20)])
    email=StringField(label="Enter email", validators=[DataRequired(),Email()])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=8)])
    submit=SubmitField(label="Register")

#passwords={}
#passwords['lhhung@uw.edu']='qwerty'

app = Flask(__name__)
app.secret_key="a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)

def addUser(email, password, username):
    #check if email or username exits
    user=UserModel()
    user.set_password(password)
    user.email=email
    user.username=username
    db.session.add(user)
    db.session.commit()

@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel.query.filter_by(email = "lhhung@uw.edu").first()
    if user is None:
        addUser("lhhung@uw.edu","qwerty","Hung")    
    
@app.route("/home", methods=('GET', 'POST'))
@login_required
#def findCoffee():
    #return render_template("home.html", myData=find_coffee())
def Landing():
    form=LandingPage()
    if form.validate_on_submit():
    #if False:
        (Year, Month, Day) = str(form.date.data).split('-')
        Monthday=f'{Month}/{Day}'
        number=form.number.data
        feedData=findBirths(Monthday, Year, number)
        return render_template('landing.html', form=form, feedData=feedData)
    else:
        return render_template('landing.html', form=form)

@app.route("/")
def redirectToLogin():
    return redirect("/login")

@app.route("/login",methods=['GET','POST'])
def login():
    form=loginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            username=request.form["username"]
            pw=request.form["password"]
            user = UserModel.query.filter_by(username = username).first()
            if user is not None and user.check_password(pw) :
                login_user(user)
                return redirect('/home')
    return render_template("login.html",form=form)

@app.route("/register",methods=['GET','POST'])
def register():
    form=registerForm()
    if form.validate_on_submit():
        if request.method == "POST":
            username=request.form["username"]
            email=request.form["email"]
            pw=request.form["password"]
            #user = UserModel.query.filter_by(email = email).first()
            #if user is not None and user.check_password(pw) :
            #TODO:  check that email and username aren't taken
            addUser(email,pw,username)
            return redirect('/login')
    return render_template("register.html",form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
