from flask import Blueprint, render_template, request, session, url_for, redirect
from database import conn

staff = Blueprint('staff', __name__)

@staff.route('/staffHome')
def staffHome():
    #unauthorized user redirect
    if session["role"] != "staff": 
        error = 'Unauthorized User: only staff members are authorized to manage this page'
        return render_template('staffHome.html', error=error)
        
    #fetch data from session
    username = session["username"]
    cursor = conn.cursor()
    query = 'SELECT first_name, last_name, airline_name FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone() 
    #debugging
    print(data["first_name"], data["last_name"], data["airline_name"])
    cursor.close()
    return render_template("staffHome.html",username = username, info = data)

@staff.route('/flightManage', methods = ['GET', 'POST'])
def viewFlight():
    #unauthorized user redirect
    if session["role"] != "staff": 
        error = 'Unauthorized User: only staff members are authorized to manage this page'
        return render_template('staffHome.html', error=error) 

    #get airline name
    airline_name = session['airline_name']

    if request.method == "POST": 
        #grabs information from the forms
        dept_from = request.form['dept_from']
        arr_at = request.form['arr_at']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        #database query
        cursor = conn.cursor()
        query = "SELECT * FROM flight WHERE airline_name = %s AND DATE(dept_time) BETWEEN DATE(%s) \
        AND DATE(%s) AND dept_from = %s AND arr_at = %s"
        cursor.execute(query, (airline_name, start_date, end_date, dept_from, arr_at))
        data1 = cursor.fetchall() 
        cursor.close()
        msg = (dept_from, arr_at, start_date, end_date)

    else: 
        # default views 
        cursor = conn.cursor()
        query = 'SELECT * FROM flight WHERE airline_name = %s AND DATE(dept_time) BETWEEN DATE(CURRENT_TIMESTAMP) \
        AND DATE(CURRENT_TIMESTAMP) + INTERVAL 30 DAY'
        cursor.execute(query, (airline_name))
        data1 = cursor.fetchall() 
        cursor.close()
        msg = "Default: Future 30 Days"

    # send to the html   
    if data1:
        for each in data1:
            print("Received Data:/n", each['airline_name'],each['flight_num'],each['dept_time'])
            return render_template('flightManage.html', flights=data1, msg = msg)
    else: 
        #returns an error message to the html page
        noFound = "No flights available within the given conditions"
        return render_template('flightManage.html', noFound = noFound)


@staff.route('/addFlights', methods = ['GET', 'POST'])
def add_flight():
    #unauthorized user redirect
    if session["role"] != "staff": 
        error = 'Unauthorized User: only staff members are authorized to manage this page'
        return render_template('staffHome.html', error=error)
    
    #get airline name
    airline_name = session['airline_name']

    if request.method == "POST":
        #grabs information from the forms
        flight_num = request.form['flight_num1']
        dept_time = request.form['dept_time1']
        arr_time = request.form['arr_time1']
        base_price = float(request.form['base_price1'])
        flight_status = "on time"
        dept_from = request.form['dept_from1']
        arr_at = request.form['arr_at1']
        airplane_id = request.form['airplane_id1']

        cursor = conn.cursor()
        
        #check foreign_key constraint and duplicate
        #airplane 
        query = "SELECT airplane_id FROM airplane"
        cursor.execute(query)
        data = cursor.fetchall()
        airplane_list = []
        for line in data:
            airplane_list.append(line["airplane_id"])
        if airplane_id not in airplane_list: 
            noFound = "Airplane ID Not Found"
            return render_template('flightManage.html', noFound = noFound)
        #airport
        query = "SELECT name FROM airport"
        cursor.execute(query)
        data = cursor.fetchall()
        airport_list = []
        for line in data:
            airport_list.append(line["name"])
        if dept_from not in airport_list or arr_at not in airport_list:
            noFound = "Airport Not Found"
            return render_template('flightManage.html', noFound = noFound)


        query = "SELECT * FROM flight WHERE (airline_name, flight_num, dept_time) = (%s, %s, %s)"
        cursor.execute(query, (airline_name, flight_num, dept_time))
        data = cursor.fetchall()
        if data: 
            noFound = "Flight Already Exist"
            return render_template('flightManage.html', noFound = noFound)

        #update database
        query = "INSERT INTO flight VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (airline_name, flight_num, dept_time, arr_time,\
            base_price, flight_status, dept_from, arr_at, airplane_id))
        print("Add Flights Success")
        return redirect("/flightManage")
    else: 
        render_template("flightManage.html")

@staff.route('/updateStatus/<string:flight_num>/<string:dept_time>', methods = ['GET', 'POST'])
def change_status(): 
    #unauthorized user redirect
    if session["role"] != "staff": 
        error = 'Unauthorized User: only staff members are authorized to manage this page'
        return render_template('staffHome.html', error=error)

    #get airline name
    airline_name = session['airline_name']

    #grabs information from the forms
    flight_num = request.form['flight_num']
    dept_time = request.form['dept_time']
    flight_status = request.form['flight_status']

    cursor = conn.cursor()
    
    #check if such flight exits
    query = "SELECT * FROM flight WHERE airline_name = %s AND flight_num = %s AND dept_time = %s"
    print(airline_name,flight_num, dept_time)
    cursor.execute(query, (airline_name,flight_num, dept_time))
    data = cursor.fetchall()
    print ("I am here", data)
    if not data: 
        noFound = "Such Flight Does not Exist"
        return render_template('flightManage.html', noFound = noFound)

    #update database
    query = "UPDATE flight SET flight_status = %s WHERE (airline_name, flight_num, dept_time) = (%s, %s, %s)"
    cursor.execute(query, (flight_status, airline_name, flight_num, dept_time))
    message = "Update Flights Success"

    #fetch data
    query = "SELECT * FROM flight WHERE airline_name = %s AND DATE(dept_time) BETWEEN DATE(CURRENT_TIMESTAMP) \
    AND DATE(CURRENT_TIMESTAMP) + INTERVAL 30 DAY"
    cursor.execute(query, (airline_name))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['airline_name'],each['flight_num'],each['dept_time'])
    cursor.close()
    return render_template('flightManage.html', flights=data1, msg = message)

@staff.route('/airplaneManage')
def managePlane():
    pass

@staff.route('/airportManage')
def manageAirport():
    pass

@staff.route('/ratings',methods=['GET', 'POST'])
def checkRatings():
    #unauthorized user redirect
    if session["role"] != "staff": 
        error = 'Unauthorized User: only staff members are authorized to manage this page'
        return render_template('staffHome.html', error=error)

    #fetch data
    cursor = conn.cursor()
    query = "CREATE VIEW averagerate as SELECT airline_name, flight_num FROM rates WHERE \
        = %s"


    pass 

@staff.route('/topAgent')
def viewTopAgent():
    pass

@staff.route('/topCustomer')
def viewTopCustomer(): 
    pass

@staff.route('/report')
def viewReport():
    pass

@staff.route('/revenueCompare')
def revenueCompare():
    pass

@staff.route('/topDestination')
def topDestination(): 
    pass












