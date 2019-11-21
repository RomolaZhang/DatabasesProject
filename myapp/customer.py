# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, session, url_for, redirect
from database import conn

customer = Blueprint('customer', __name__)

@customer.route('/customerHome')
def customerHome():
    email = session['email']
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT * FROM ticket WHERE cust_email = %s'
    cursor.execute(query, (email))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['airline_name'],each['flight_num'],each['dept_time'])
    cursor.close()
    return render_template('customerHome.html', username = username, flights=data1)