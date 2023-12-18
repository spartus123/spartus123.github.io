# Final-project
Eshop mini project.
1.Create virtual environment in project's root directory:
python -m venv venv
2.Activate virtual environment:
source venv/Scripts/activate
3.Install requirements:
pip install -r requirements.txt
4.Run the project:
Create a .env file in the project's root directory and 
add DEVELOPMENT environment variables to this file.
Example .env file:
# DEVELOPMENT environment (.env ---> .env.dev)
SECRET_KEY=django-insecure-_lki!#=0zkw)rtoilxq==!i@6t9^b141j-&-o2ysm@wxjyr_2w
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=db.sqlite3
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
5.Prepare database:
Since the SQLite database file is stored in this Git repo, if you would like to use a fresh new database, remove 
this file (db.sqlite3), and then run:
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
Note: After creating a superuser, you need to add a Profile to him/her in the Django Admin page (for all other users, the Profile is created automatically on user creation).

