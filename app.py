#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
from decimal import *
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='192.168.64.2',
                       user='chuyi',
                       password='password',
                       db='air_ticket_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
  return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Authenticates the login
@app.route('/loginAuthCustomer', methods=['GET', 'POST'])
def loginAuthCustomer():
    #grabs information from the forms 
    email = request.form['email']
    password = request.form['password']
    print(email, password)
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM customer WHERE email = %s and password = %s'
    cursor.execute(query, (email, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['email'] = email
        return redirect(url_for('customerhome'))
    else:
        #returns an error message to the html page
        error = 'Invalid password or username'
        return render_template('login.html', error=error)

@app.route('/loginAuthAgent', methods=['GET', 'POST'])
def loginAuthAgent():
    email = request.form['email']
    password = request.form['password']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM booking_agent WHERE email = %s and password = %s'
    cursor.execute(query, (email,password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['email'] = email
        return redirect(url_for('agenthome'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

@app.route('/loginAuthStaff', methods=['GET', 'POST'])
def loginAuthStaff():
    username = request.form['username']
    password = request.form['password']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        return redirect(url_for('staffhome'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)
    

#Authenticates the register
@app.route('/registerAuthCustomer', methods=['GET', 'POST'])
def registerAuthCustomer():
    #grabs information from the forms
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    building_num = request.form['building_num']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_num = request.form['phone_num']
    passport_num = request.form['passport_num']
    passport_expr = request.form['passport_expr']
    passport_country = request.form['passport_country']
    DOB = request.form['DOB']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        cursor.close()
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (email, password, name, building_num, street, city, state, phone_num, passport_num, passport_expr, passport_country, DOB, 0))
        conn.commit()
        cursor.close()
        return render_template('index.html')

@app.route('/registerAuthAgent', methods=['GET', 'POST'])
def registerAuthAgent():    
    email = request.form['email']
    password = request.form['password']
    agent_id = request.form['id']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM booking_agent WHERE email = %s'
    cursor.execute(query, (email))
    #stores the results in a variable
    data = cursor.fetchone()
    query = 'SELECT * FROM booking_agent WHERE agent_id = %s'
    cursor.execute(query, (agent_id))
    data2 = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        cursor.close()
        return render_template('register.html', error = error)
    elif (data2):
        #If the previous query returns data, then user exists
        error = "This agent id already exists"
        cursor.close()
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO booking_agent VALUES(%s, %s, %s, %s)'
        cursor.execute(ins, (email, password, agent_id, 0))
        conn.commit()
        cursor.close()
        return render_template('index.html')

@app.route('/registerAuthStaff', methods=['GET', 'POST'])
def registerAuthStaff(): 
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    DOB = request.form['DOB']
    airline_name = request.form['airline_name']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        cursor.close()
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO airline_staff VALUES(%s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, password, first_name, last_name, DOB, airline_name))
        conn.commit()
        cursor.close()
        return render_template('index.html')
    

@app.route('/searchFlights', methods=['GET', 'POST'])
def searchFlights():
    #grabs information from the forms
    dept_from = request.form['dept_from']
    arr_at = request.form['arr_at']
    dept_date = request.form['dept_date']
    return_date = request.form['return_date']

    #open cursor
    cursor = conn.cursor()

    #excutes query for flight
    query = "select * from flight natural join airplane, airport as A, airport as B where flight.dept_from = A.name and flight.arr_at = B.name and (A.name = %s or A.city = %s) and (B.name = %s or B.city = %s) and date(dept_time) = %s "
    cursor.execute(query, (dept_from, dept_from, arr_at, arr_at, dept_date))
    #store the results
    data = cursor.fetchall()

    if return_date:
        query2 = "select * from flight natural join airplane, airport as A, airport as B where flight.dept_from = A.name and flight.arr_at = B.name and (A.name = %s or A.city = %s) and (B.name = %s or B.city = %s) and date(dept_time) = %s "
        cursor.execute(query2, ( arr_at, arr_at, dept_from, dept_from, return_date))

    #store the results
    data2 = cursor.fetchall()


    for each in data:
        #excutes query for ticket sold 
        queryTicketNum = "select count(*) from ticket natural join flight natural join airplane where airline_name = %s and flight_num = %s and dept_time=%s"
        cursor.execute(queryTicketNum, ( each['airline_name'], each['flight_num'], each['dept_time']))
        ticketNum = cursor.fetchone()
        rate = (each['seats'] - ticketNum['count(*)']) / each['seats']
        if rate > 0.7:
            each['current_price'] = Decimal(1.2) *each['base_price']
    
    for each in data2:
        #excutes query for ticket sold 
        queryTicketNum = "select count(*) from ticket natural join flight natural join airplane where airline_name = %s and flight_num = %s and dept_time=%s"
        cursor.execute(queryTicketNum, ( each['airline_name'], each['flight_num'], each['dept_time']))
        ticketNum = cursor.fetchone()
        rate = (each['seats'] - ticketNum['count(*)']) / each['seats']
        if rate > 0.7:
            each['current_price'] = Decimal(1.2) *each['base_price']
    
    cursor.close()

    error = None
    if data: #input is valid
        # for each in data: #for debugging
        #     print(each)
        if return_date: # round trip·
            if data2: 
                return render_template("search.html", flights = data, returnFlights = data2)
            else: 
                error = "The Return Flight You are Searching Is Empty"
                return render_template("search.html", error = error)
        else: #one way trip
            return render_template("search.html", flights = data)
    else: 
        #returns an error message to the html page
        error = "The Flight You are Searching Is Empty"
        return render_template("search.html", error = error)

@app.route('/checkFlight', methods=['GET', 'POST'])
def checkFlight():
    #grabs information from the forms
    airline_name = request.form['airline_name']
    flight_num = request.form['flight_num']
    dept_date = request.form['dept_date']
    arr_date = request.form['arr_date']

    #open cursor
    cursor = conn.cursor()

    #excutes query
    if dept_date and arr_date: 
        query = "select * from flight where airline_name = %s and flight_num = %s and date(dept_time) = %s and date(arr_time) = %s"
        cursor.execute(query, (airline_name, flight_num, dept_date, arr_date))
    elif dept_date:
        query = "select * from flight where airline_name = %s and flight_num = %s and date(dept_time) = %s"
        cursor.execute(query, (airline_name, flight_num, dept_date))
    elif arr_date:
        query = "select * from flight where airline_name = %s and flight_num = %s and date(arr_time) = %s"
        cursor.execute(query, (airline_name, flight_num, arr_date))
    else: 
        pass

    #store the results
    data3 = cursor.fetchall()

    cursor.close()
    error = None

    if data3: 
        return render_template("check.html", status = data3)
    else: 
        error = "The Flight You are Searching Is Empty"
        return render_template("check.html", error = error)

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('localhost', 5000, debug = True)