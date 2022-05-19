# cse442-spring2022-team-team-pentaneers
cse442-spring2022-team-pentaneers created by GitHub Classroom

# **Team Pentaneers**

## **Important Links**
 * http://cheshire.cse.buffalo.edu:8000/ -- Live HTTP Version of our website
 * https://cheshire.cse.buffalo.edu:9000/ -- Live HTTPS Version of our website


# **Installation**
 * Our code structure follows the **Flask framework installation and setup**. When Flask is installed and imported into the application.py file, various distributions will be automatically installed.
 * We also use a virtual environment to manage the dependencies for our project development.
 * To create and activate the virtual environment, as well as installing Flask, please refer to https://flask.palletsprojects.com/en/2.1.x/installation/.

# **Deployment**
 * Due to the fact that both Flask and MYSQL require sensitive data, we create a config.py file that does not get pushed to our GitHub. This config.py file contains our Flask secret key, our MYSQL host name, username, password, and schema name. Lastly, we also set a variable named “UBITS” that’s is a List of commas separated UBID’s in string type.

**Config.py data:**
1. SECRET_KEY = '(type in whatever you want)'
2. DATABASE_HOST = '(type in your mysql host name)'
3. DATABASE_USER = '(type in your mysql username)'
4. DATABASE_PASSWORD= '(type in your mysql password)'
5. DATABASE_SCHEMA = '(type in your mysql schema)'
6. UBITS = [‘teammate 1 ubid’, ‘teammate 2 ubid’, ‘teammate 3 ubid’, ‘teammate 4 ubid’, . . .]

## **Local Deployment:**
In the case that we want to run our application locally, this can be easily achieved by following the steps below:
1. In any IDE, clone the repo by typing the following command in the terminal:
    ```
    git clone https://github.com/xlab-classes/cse442-spring2022-team-team-pentaneers.git
    ```
2. Go to  https://flask.palletsprojects.com/en/2.1.x/installation/ and follow the steps to install Flask on your operating System.

3. To get the Flask app running, go to https://flask.palletsprojects.com/en/2.1.x/quickstart/ and follow the steps to run the application.

4. Create a **config.py** file in the root directory and fill in the necessary data. Please refer to the ```Config.py data``` above to correctly set up the file. 

5. When working in your terminal, the application to work with by exporting the FLASK_APP environment variable, make sure to use the python file that’s named “application.py”.

    Example:
    ```
    FLASK_APP=application
    ```

6. Run the Flask App by executing the following command in the terminal:
    ```
    flask run
    ```
7. Head over to the hyperlink in the terminal after the flask app has been succesfully ran. The application may be running on http://127.0.0.1:5000/.

## **UB Server Deployment**
If someone wants to deploy our code on the UB Server, they would have to follow a very similar set of instructions.

To start, begin by logging into the student web development server, cheshire. Only cheshire is configured to run Flask.

1. In your terminal, SSH into the UB development server by executing:
    ```
    ssh <your_ubid>@cheshire.cse.buffalo.edu
    ```
2. Head to the main directory of our groups project. In your terminal, change the directory by executing:
    ```
    cd /web/CSE442-542/2022-Spring/cse-442ab.
    ```
3. Go ahead and clone the GitHub repository into the directory. In your terminal, execute the following code:
    ```
    git clone https://github.com/xlab-classes/cse442-spring2022-team-team-pentaneers.git
    ```

4. Create a **config.py** file in the **cse442-spring2022-team-team-pentaneers** folder and fill in the necessary data. Please refer to the ```Config.py data``` above the ```Local Deployment``` header to correctly set up the file. 

5. Once the cloning is complete, install the Flask virtual environment (venv) by executing the command:
    ```
    python3.8 -m venv venv
    ```

    As mentioned on step 4 on ```wiki.cse.buffalo.edu/services/content/flask```, to activate your virtual environment, you'll need to run the bash shell. Change your current shell to bash. CSE sets your default shell to tcsh. But you'll need to use bash for this job.

6. Go ahead and activate your Flask virtual environment (venv) by executing the following code in your bash shell:
    ```
    . venv/bin/activate
    ```

7. Execute the following commands (in the bash shell) in the order typed here:
    *     pip install Flask
    *     pip install -r requirements.txt
    

    **If any import errors arise**, ***simply remove any imports that raised the Import Error from requirements.txt.***

8. In the bash shell, execute:
    ```
    export FLASK_APP=application
    ```
9. Lastly, execute:
    ```
    flask run --host=cheshire.cse.buffalo.edu -p 8000
    ```
10. If needed, run a screen on the website so that it can stay running even after the terminal is closed. (optional)

11. Head over to http://cheshire.cse.buffalo.edu:8000/ and verify that the DuckyForms website is running.


# **Links**
 * **Zenhub -** https://app.zenhub.com/workspaces/team-pentaneers-6203fc9905c6530016dd6fcf/board
 * **FIGMA Wireframe -** https://www.figma.com/file/KiVeuB4d64S1cwp2iVXkxA/Survey-Website-Wireframe?node-id=0%3A1
