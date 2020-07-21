from flask import Flask
<<<<<<< HEAD
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from graderx import views
=======

app = Flask(__name__)

from graderx import views
>>>>>>> staging
