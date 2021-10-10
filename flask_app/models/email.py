from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Email:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = 'INSERT INTO emails (email) VALUES (%(email)s);'
        result = connectToMySQL('email_validation').query_db(query, data)
        return result

    @classmethod
    def read_all(cls):
        query = 'SELECT * FROM emails;'
        results = connectToMySQL('email_validation').query_db(query)
        emails = []
        for email in results:
            emails.append(cls(email))
        return emails

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM emails WHERE id = %(id)s;'
        return connectToMySQL('email_validation').query_db(query, data)

    @staticmethod
    def validate_email(email):
        query = 'SELECT * FROM emails WHERE email = %(email)s;'
        results = connectToMySQL('email_validation').query_db(query, email)
        is_valid = True
        if not EMAIL_REGEX.match(email['email']):
            flash('Email is not valid!')
            is_valid = False
        elif len(results) >= 1:
            flash('Email is already taken.')
            is_valid = False
        else:
            flash('The email address you entered is valid! Thank you.')
        return is_valid