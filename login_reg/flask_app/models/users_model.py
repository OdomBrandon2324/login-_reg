# the model will Talk to the DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']


#=================== CREATE USER ===========================

    @classmethod
    def create (cls, data):
        query ="""
        INSERT INTO users ( first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
    """
        return connectToMySQL(DATABASE).query_db(query,data)

#================== GET USER BY ID ==================

    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT *FROM users
        WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if len(results) < 1:
            return[]
        return cls(results[0])
    



    #================== GET USER BY EMAIL ==================

    @classmethod
    def get_by_email(cls, data):
        query = """
        SELECT *FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])
    

#=============================== VALIDATIONS =====================

    @staticmethod
    def validate(data):
        is_valid = True
        

        if len(data['first_name']) < 1:
            is_valid = False
            flash("first name required", "first_name")

        if len(data['last_name']) < 1:
            is_valid = False
            flash("last name required", "reg")

        if len(data['email']) < 1:
            is_valid = False
            flash("email required", "reg")
        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "reg")
            is_valid = False
        else:
            email_dict = {
                'email': data['email']
            }
            potential_user = User.get_by_email(email_dict)
            if potential_user: #! email is not unique
                is_valid = False
                flash("email already taken, hopefully by you!", "reg")



        if len(data['password']) < 1:
            is_valid = False
            flash("password required", "reg")
        elif not data['password'] == data ['confirm_password']:
            is_valid = False
            flash("password don't match!", "reg")
        
        return is_valid





