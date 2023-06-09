from flaskext.mysql import MySQL
from flask import Flask


# App configurations
app = Flask(__name__)
app.debug = True

# App configurations
app.config['FILE_UPLOADS'] = './uploads'

# MySQL configurations
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'secret'
app.config['MYSQL_DATABASE_DB'] = 'copyscience'
app.config['MYSQL_DATABASE_HOST'] = 'cs_tsoev_db'
# app.config['MYSQL_DATABASE_PORT'] = '3306'

mysql.init_app(app)

# Moz API configurations
moz_access_id = 'mozscape-e48b88f1df'
moz_secret_key = '3a15f80f84912b6bf1eabbcd627e2ef5'

# SEMRush API configurations
semrush_api_key = 'decdfae7e1370cba9e5b08d92d3263b6'
