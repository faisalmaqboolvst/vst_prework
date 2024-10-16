# To load static files run this commands
python manage.py collectstatic


# You need to create a virtual environment to help ensure isolated, conflict-free, and reproducible project setups.


# On Windows to activate virtual environment
venv\Scripts\activate


# On macOS/Linux to activate virtual environment
source venv/bin/activate


# To install the requirements
pip install -r requirements.txt


# To run django server
python manage.py runserver


# We will use Black to format the code structure. The command to run Black is:
black .
When we push our code to Git, we need to run the above command. This will structure our code and efficiently manage our import statements and indentations.

# Database Mongodb
We are using MongoDB to store the data, and the connection is set globally, so there's no need to establish a new connection on every request. This helps reduce response time and database costs. You need to manage the credentials in a secret file.


# Unit Test
We have written the unit tests, and you can test the APIs against them by using the following command:
python manage.py test


# Models or Collections
Sometimes, we need to use both SQL and NoSQL databases. In the case of Django with an SQL database like PostgreSQL, we define our models in models.py. Similarly, when working with a NoSQL database, we should also define our collection names in models.py, following Django standards. This ensures better organization and helps developers easily identify all collections and models within an app.