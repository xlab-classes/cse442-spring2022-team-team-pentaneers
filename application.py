from flask import Flask, redirect, url_for, render_template
from forms import RegistrationForm, LoginForm

application = app = Flask(__name__)

# IMPORTANT: Set to environment variable!
app.config['SECRET_KEY'] = "uggvhgjbjbn777"

#------------------The path to our homepage-----------------------
@app.route("/")
def home():
    return render_template('Homepage.html', title = "Homepage")

#------------------The path to our signup page-----------------------
@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    form = RegistrationForm()
    email = None
    print(form.email.data)
    print(form.password.data)
    print(form.confirm_password.data)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print("The form was validated")
        # Grab all of the users that have the email address that was typed into the Register form and return the first one, None if non exist
        #user = Users.query.filter_by(email=form.email.data).first()
        # If there isn't already a user with the email, add it to the database
        #if user is None:
            # Create a new user to add to the Database
            #NewDatabaseUser = Users(email=form.email.data, password=form.password.data)
            #Database.session.add(NewDatabaseUser)
            #Database.session.commit()
            #flash(f'Account created for {form.email.data}!', 'Success')

        #email = form.email.data
        # Clearing the form
        #form.email.data = ''
        #return redirect(url_for('home'))
    #print(form.errors)
    return render_template('signup.html', title = "Sign up", form = form)

##------------------The path to our login page-----------------------
@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('Login.html', title = "Login", form = form)

#------------------The path to our user homepage-----------------------
@app.route("/user_homepage")
def user_homepage():
    return render_template('User_Homepage.html', title = "User Homepage")

#------------------The path to the view survey page-----------------------
@app.route("/view_surveys")
def view_surveys():
    return render_template('View_Surveys.html', title = "'View Surveys")

# Invalid path.
@app.route("/<error>")
def error(error):
    pass
    #return f"page '{error}' does not exist!"

# @app.route("/admin/")
# def admin():
#     return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    #app.run(debug = True) # Set to false for production
