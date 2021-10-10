from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.email import Email

@app.route('/')
def main_page():
    return render_template('email.html')

@app.route('/create', methods = ['post'])
def create_email():
    if not Email.validate_email(request.form):
        return redirect('/')
    Email.create(request.form)
    return redirect('/success')

@app.route('/success')
def success():
    return render_template('email_success.html', all_emails = Email.read_all())

@app.route('/delete/<int:id>')
def delete(id):
    data = {
        'id': id
    }
    Email.delete(data)
    return redirect('/success')