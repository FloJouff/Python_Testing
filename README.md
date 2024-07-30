# gudlift-registration

![Python](https://img.shields.io/badge/python-3.12.x-green.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.x-green.svg)
![Pytest](https://img.shields.io/badge/Pytest-8.2.x-blue.svg)
![Locust](https://img.shields.io/badge/Locust-2.29.x-darkgreen.svg)
![Coverage](https://img.shields.io/badge/Coverage-7.5.x-blueviolet.svg)

1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

    - You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing

    (all the following instructions suppose that your virtual environnement is launched)
    (to run all the tests properly, you must use QA branch)

    The tests are carried out using Pytest.
    To do this, type the following instruction:
    You must install pytest and the other library needed:
        <code>pip install pytest flask-testing</code>

    You can run pytest by typing the following command in the terminal:
        <code>pytest</code>

    You can use the same command to run integration and functional tests.

    To measure the coverage of the project, use pip to install the coverage library in the terminal:
        <code>pip install coverage pytest-cov</code>

    Then type the following command from the terminal:
        <code>pytest --cov=.</code>

    If you want to exclude the /tests files you can create the following file at the root of the project:
        <code>.coveragerc</code>
    
    then add the following code to exclude a directory :
        <code>[run]
                omit = chemin_du_répertoire/* </code>

    An html coverage report is available in the Github repository

    You can also realize a performance test using locust.
    Before starting to create your first performance test, you need to install Locust on your environment using the command:
        <code>pip install locust</code>
    
    The locust script is available in the following directory: /tests/performance_tests/locustfile.py

    You can test it by opening a terminal on this directory and type <code>locust</code> in the terminal

    open your navigator on the following url: [here](http://localhost:8089) to see locust's web interface.
