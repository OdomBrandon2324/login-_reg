from flask_app import app
# ! REMEMBER TO ALWAYS IMPORT THE CONTROLLER

from flask_app.controllers import users_controller


if __name__ == "__main__":
    app.run(debug=True, port=5001)
