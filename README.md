CSE586 Project1 MyWayPoint
________________________________________________________________________________________________________________________________

Tips:
Please check the all files in the project diretory: main_DB.py, main_no_DB.py, index.html and test.html in templates.
________________________________________________________________________________________________________________________________

Ruquires:
1.Flask
2.flask_sqlalchemy
3.flask_mysqldb
4.requests
5.json
________________________________________________________________________________________________________________________________

How to use:

1.No database version:

-- Simply run the main_no_DB.py
-- Open the web browser,type http://127.0.0.1:5000/.
-- Just type the start location and end location then press the button.
-- If the page return "Not Found Correct Route, Please reopen the web and check your input information", don't refresh the web, but colse it and reopen the url. Please ensure the locations you put are valid.
-- If the route does not fit your real location, please input the exact address separated by space.


2.Database version:

-- Before run the program,please ensure that you have installed Mysql in your PC and create a database for the project.
-- Remember the name of database, and change the config in line 8, please change the sql config in the following format:
	mysql://<your MySql username>:<your MySql password>@127.0.0.1/<your project database name>
-- Please ensure you have install the Flask-SQLAlchemy else you will fail to connect to your Mysql server.
-- Run the code file "main_DB.py" and open http://127.0.0.1:5000/ in browser.
-- Everytime you execute the query, you can check the status of query in the console:
	"Find it!" : find the route information from database
	"Not found" : find nothing in the database and execute the GOOGLE MAP API
	"add done" : add the query result to the database successfully
	