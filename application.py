import json
from create import Survey,Response,Account
from flask import Flask, request, redirect, url_for, render_template
#from forms import RegistrationForm, LoginForm

application = app = Flask(__name__)

# IMPORTANT: Set to environment variable!
app.config['SECRET_KEY']

# The path to our homepage.
@app.route("/")
def hello_world():
    return "Hello, World!"
#def home():
    #return render_template('home.html', title = "Homepage")

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

#path to create Surveys
@app.route("/submitSurvey", methods=['POST'])
def createSurvey():
    #print("hi!!!")
    data=json.loads(request.get_data(as_text=True))
    #print(data)
    id=Survey.survey(data)
    #print(id)
    return json.dumps(id)

#path to create account
@app.route("/signup", methods=['POST'])
def createAccount():
    data=json.loads(request.get_data(as_text=True))
    returnid=Account.account(data)
    return returnid

#path to create response
@app.route("/submitResponse", methods=['POST'])
def createResponse():
    data=json.loads(request.get_data(as_text=True))
    survey_id=Response.response(data)
    return survey_id

# @app.route("/admin/")
# def admin():
#     return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    #app.run(debug = True) # Set to false for production
