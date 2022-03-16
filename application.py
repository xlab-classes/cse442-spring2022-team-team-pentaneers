from flask import Flask, redirect, url_for, render_template
#from forms import RegistrationForm, LoginForm

application = app = Flask(__name__)

# IMPORTANT: Set to environment variable!
app.config['SECRET_KEY']

# The path to our homepage.
@app.route("/")
def home():
    return render_template('Homepage.html', title = "Homepage")

# The path to our sign up page.
@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    #form = RegistrationForm()
    return render_template('Signup.html', title = "Sign up")  #form = form)

# The path to our login page.
@app.route("/login", methods = ['GET', 'POST'])
def login():
    #form = LoginForm()
    return render_template('Login.html', title = "Login") #form = form)

# The path to our user homepage.
@app.route("/user_homepage")
def user_homepage():
    return render_template('User_Homepage.html', title = "User Homepage")

# The path to the view survey page.
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
