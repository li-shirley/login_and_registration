from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt        
# bcrypt = Bcrypt(app) 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
NAME_REGEX = re.compile(r'^[a-zA-Z]')

DATABASE = 'login_and_registration'

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod 
    def create(cls, data): 
        query = "INSERT INTO users (password, first_name , last_name , email) VALUES ( %(password)s, %(first_name)s , %(last_name)s , %(email)s );"
        return connectToMySQL(DATABASE).query_db( query, data)

    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) <1:
            return False
        return cls(results[0])


    @staticmethod
    def validate_registration(user):
        is_valid = True
        if len(user['first_name']) < 2 or len(user['first_name']) > 45:
            flash('First name must be between 2 and 45 characters.', 'err_users_first_name')
            is_valid = False
        if not NAME_REGEX.match(user['first_name']) and len(user['first_name']) >= 1:
            flash('First name can only contain letters', 'err_users_first_name')

        if len(user['last_name']) < 2 or len(user['last_name']) > 45:
            flash('Last name must be between 2 and 45 characters.', 'err_users_last_name')
            is_valid = False
        if not NAME_REGEX.match(user['first_name']) and len(user['last_name']) >= 1:
            flash('Last name can only contain letters', 'err_users_last_name')

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'err_users_email')
            is_valid = False
        else:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            results = connectToMySQL(DATABASE).query_db(query,user)
            if len(results) >= 1:
                flash ("Email already in use. Please try another.", 'err_users_email')
                is_valid = False

        if len(user['password']) < 8: 
            flash("Password must contain at least 8 characters", 'err_users_password')
        if (user['password']) != (user['confirm_password']):
            flash("Passwords do not match. Please try again.", 'err_users_password')
        return is_valid

