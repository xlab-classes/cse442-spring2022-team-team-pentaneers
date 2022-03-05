from flask import Flask, redirect, url_for, render_template
#from forms import RegistrationForm, LoginForm

application = app = Flask(__name__)

# IMPORTANT: Set to environment variable!
app.config['SECRET_KEY']

# The path to our homepage.
@app.route("/")
def home():
    return render_template('home.html', title = "Homepage")

# The path to our sign up page.
@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    pass
    #form = RegistrationForm()
    #return render_template('signup.html', title = "Sign up", form = form)

# The path to our login page.
@app.route("/login", methods = ['GET', 'POST'])
def login():
    pass
    # form = LoginForm()
    #return render_template('login.html', title = "Login", form = form)

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
