from flask import Flask
app = Flask(__name__)
app.secret_key= "shhh secret key"
DATABASE = "users_login"