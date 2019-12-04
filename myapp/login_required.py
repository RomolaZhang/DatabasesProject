from functools import wraps
from flask import session, flash, url_for, redirect

def customer_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['role'] == 'customer':
            return f(*args, **kwargs)
        else:
            flash("You need to login as a customer first")
            return redirect(url_for('register_login.login'))
    return wrap

def customer_or_agent_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['role'] == 'customer' or session['role'] == 'agent':
            return f(*args, **kwargs)
        else:
            flash("You need to login as a customer first")
            return redirect(url_for('register_login.login'))
    return wrap

def agent_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['role'] == 'agent':
            return f(*args, **kwargs)
        else:
            flash("You need to login as a booking agent first")
            return redirect(url_for('register_login.login'))
    return wrap