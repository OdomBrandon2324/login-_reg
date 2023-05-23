# ROUTING
from flask_app import app
from flask import render_template, redirect, request,  session, flash
from flask_app.models.users_model import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)


# =============== LOGIN PAGE ==============


@app.route("/")
def index():
    if 'user_id' in session:
        return redirect("/dashboard")
    return render_template("index.html")


# ================= REGISTER method ------ACTION

@app.route("/users/register", methods=['post'])
def user_reg():

    print(request.form)
    if not User.validate(request.form):
        return redirect("/")
    # 1 has the password
    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    #2 get the data dict ready with the hashed password
    data = {
        **request.form,
        'password': hashed_password
    }
    # 3 pass the data dict to the User construction
    user_id = User.create(data)
    # 4 store ethe user_id in session
    session['user_id'] = user_id
    return redirect("/dashboard")


# ------------- dashboard - view----
@app.route("/dashboard")
def dash():
    # ! route guard
    if 'user_id' not in session:
        return redirect ("/")
    # grab the user
    data = {
        'id' : session['user_ id']
    }
    logged_user = User.get_by_id(data)
    return render_template("dashboard.html",
                            Logged_user=logged_user)


#--------- Logout-----------------------
@app.route("/logout")
def logout():
    # del session['user_id']
    session.clear
    return redirect("/")

#* ============ Login =============
@app.route ("/users/login", methods=['post'])
def login():
    data = {
        'email' : request.form['email']
    }
    user_in_db = User.get_by_email(data)
    # if email not found
    if not user_in_db:
        flash("invalid credentials", "log")
        return redirect("/")
    # check password
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("invalid credentials", "log")
        return redirect("/")
    #all good up to here
    session['user_id'] = user_in_db.id

    return redirect("/dashboard")