# gudlift-registration

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

    - Next, type <code>source bin/activate</code> (if you are on MacOS or Linux) or <code>Scripts/activate</code> (if you are on Windows). You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code> regardless of your OS.

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

    - You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing

    Please find below a list of commands you can run using the implemented test suite:
   
    * Launching all the tests : Go to the root folder and type the following command : ```pytest tests/``` or ```pytest tests/ -vv``` should you wish to have more details about the tests.
    * Checking the test coverage : Go to the root folder and type the following command : ```pytest --cov=. tests/```
    * Launching a performance test :
      * Go to the following folder : ```oc-cg-p11/tests/performance_tests/``` and type the following command : ```locust```
      * On your browser, go to the following link : ```http://localhost:8089/```
      * Populate the fields with the following informations:
        ```
        Number of users : 1
        Spawn Rate : 1
        Host : http://127.0.0.1:5000/ 
        ```
        The host field should correspond to the address on which the application is running, please amend if yours is different.
      * Click on the ```Start swarming``` button.
      * Important reminder 1 : You have to have the application running in another terminal. Otherwise, the test won't work.
      * Important reminder 2 : Hit the stop button before leaving the Locust page.

