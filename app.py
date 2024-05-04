
"""
Charlie Team, CMSC 495 Section 7381, Spring 2024
John Leckie, Shara Belton, Sirish Tadepalli, and Thomas Memmo
Mark Munoz, Professor

Astronomy Web App

This is a Flask web application for a simple astronomy website. Frontend elements were mockup
forms with no backend functionality.

For our team's project, a database was added. The users (Astronomy professors working for the
school) can now schedule a time slot for either telescope usage or instructing students using
the planetarium. These actions will test interoperability between the frontend and backend 
elements of the application.
"""

import hashlib  # Required for password hashing
from datetime import datetime,timedelta
import logging
import mysql.connector
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

app = Flask(__name__)
app.secret_key = '86753093212135889'

# Connect to the MySQL database
db = mysql.connector.connect(
    host="13.58.228.75",
    user="cmsc495",
    password="CMSC4952024",
    database="cmsc495_astro"
)

#make a cursor for writing queries
cursor = db.cursor()

# Configure logging to write to security_log.txt
security_logger = logging.getLogger("security")
security_logger.setLevel(logging.INFO)

# File handler for security log
security_handler = logging.FileHandler("security_log.txt")
security_handler.setLevel(logging.INFO)

# Formatter for the log messages
security_formatter = logging.Formatter('%(asctime)s - %(message)s')
security_handler.setFormatter(security_formatter)

# Add the handler to the security logger
security_logger.addHandler(security_handler)

# Store user data in a file
SECURITY_DATA_FILE = 'security_log.txt'

# Logger for failed login attempts
failed_login_logger = logging.getLogger

path_cwd = os.path.dirname(os.path.realpath(__file__))
path_templates = os.path.join(path_cwd,"templates")
path_static = os.path.join(path_cwd, "static")



@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register users and store their information in a database after validation.

    Returns:
        rendered template for the registration page with flash messages
    """
    flash('', 'error')  # Clears existing flash messages for the session, if any
    if request.method == 'POST': 
        username = request.form['username'] #retrieves the values for username etc from the form that got submitted
        name = request.form['name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if password and confirm_password match
        if password != confirm_password:
            flash('Password and confirm password do not match. Please try again.',
                  'error')
        else:
            # Check if the username already exists in the database 
            cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
            results = cursor.fetchall()
            if results:
                flash('Username already exists. Choose another username or return to Login via below link.', 'error')
                return render_template('register.html')

            # Validate password complexity
            if not (len(password) >= 12 and any(c.isupper() for c in password)
                    and any(c.islower() for c in password)
                    and any(c.isdigit() for c in password)
                    and any(not c.isalnum() for c in password)):
                flash('Password does not meet complexity requirements', 'error')

            # Check for spaces in username and password
            elif ' ' in username or ' ' in password:
                flash('Username and password cannot contain spaces.', 'error')
            
            else:
                # Hash the password before storing it (for security)
                hashed_password = hashlib.sha256(password.encode()).hexdigest()

                # add username and hashed password to database
                cursor.execute("INSERT INTO Users (name, username, password) VALUES (%s, %s, %s)", (name, username, hashed_password))
                
                #commit db and display success message
                db.commit()
                flash('Registration successful!', 'success')

    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    Authenticate users and log them in if valid credentials are provided.

    Returns:
        rendered template for login page with flash messages
    """
    flash('', 'error')  # Clears existing flash messages for the session, if any
    reg_message = session.pop('reg_message', None)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT password FROM Users WHERE username =  %s", (username,))
        row = cursor.fetchone()
        
        db_password = row[0]
        
        #if that password, and therefore account, exists
        if db_password:

            # Hash the provided password for comparison
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if db_password == hashed_password:
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for("home"))  # Redirect to the home page after successful login
                
            else:
                # Log the failed login attempt
                failed_login_message = (f'Failed login attempt for username: {username} from '
                                    f'IP: {request.remote_addr}')
                security_logger.info(failed_login_message)
                flash('Invalid username or password', 'error')

        #if there is no resulting_row, meaning that account doesn't exist
        else:
             # Log the failed login attempt
                failed_login_message = ('Account not found '
                                    f'IP: {request.remote_addr}')
                security_logger.info(failed_login_message)
                flash('Account not found', 'error')

    return render_template('login.html', reg_message=reg_message)

def get_available_time_slots(week_date):
    cursor.execute("SELECT time FROM Telescope WHERE date = %s AND UserID IS NULL", (week_date,))
    available_time_slots = [slot[0] for slot in cursor.fetchall()]
    return available_time_slots

@app.route('/telescope_time', methods=['POST', 'GET'])
def telescope_time():
    """
    Render the telescope time sign-up page.

    Returns:
        rendered template for telescope time page
    """
    # Check if the user is logged in, if not, redirect to the login page
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        if request.is_json:
            dataGet = request.json
            selected_date = dataGet.get('date')
            #Do what is needed with the data

            print(selected_date)

            # Convert the date string to a datetime object
            date = datetime.strptime(selected_date, '%Y-%m-%d')

            # Find the Monday of the week
            monday = date - timedelta(days=date.weekday())

            week_dates = []

            # Iterate from Monday to Sunday and add each date to the list
            for i in range(7):
                week_dates.append((monday + timedelta(days=i)).strftime('%Y-%m-%d'))

            print(week_dates)

            dates_and_times_dict = {}

            for date in week_dates:
                time_slots = get_available_time_slots(date)
                dates_and_times_dict.update({date: time_slots})
                print(dates_and_times_dict)
        
            # convert timedelta objects to strings
            for key, value in dates_and_times_dict.items():
                dates_and_times_dict[key] = [str(slot) for slot in value]
        
            print(dates_and_times_dict)

            return jsonify(dates_and_times_dict)

            # return data after getting it 

        # FOR FORM SUBMISSION
        else:
            date = request.form['date']
            time = request.form['time']
            time = convert_to_24_hour(time)
            print(time)

            username = session['username']

            #first get the userID associated with that name from the Users table
            cursor.execute("SELECT userID FROM Users WHERE username = %s", (username,))
            row = cursor.fetchone()
            userID = row[0]


            #fill that userID into the row with that date and time which are formatted into strings
            cursor.execute("UPDATE Telescope SET userID = %s WHERE date = %s AND time = %s", (userID, str(date), str(time)))

            db.commit()
            flash('Reservation successful!', 'success')
    
    return render_template('telescope_time.html')

def convert_to_24_hour(time_str):
    # Parse the time string using strptime
    time_obj = datetime.strptime(time_str, '%I:%M %p')  # %I for 12-hour format, %p for AM/PM indicator
    
    # Convert the time object to 24-hour format using strftime
    time_24_hour = time_obj.strftime('%H:%M')  # %H for 24-hour format, %M for minutes
    
    return time_24_hour

@app.route('/update_password', methods=['GET', 'POST'])
def update_password():
    """
       If the user is logged in, it verifies the current password, runs the same checks on the
       candidate new one, and updates the user's password in the file if all checks pass.

       Returns:
           Updates database with user's new password, once candidate passwords pass checks.

       """
    # Check if the user is logged in, if not, redirect to the login page
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    flash('', 'error')  # Clears existing flash messages for the session, if any

    if request.method == 'POST':

        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']
        username = session.get("username")

        hashed_current_password = hashlib.sha256(current_password.encode()).hexdigest()

        cursor.execute("SELECT password FROM Users WHERE username =  %s", (username,))
        row = cursor.fetchone()
        db_password = row[0]
        
        # Ensure current password and database password are a match
        if db_password != hashed_current_password:
            # Log the failed password change attempt
            failed_change_password_message = (f'Failed password change attempt for username: {username} from '
                                f'IP: {request.remote_addr}')
            security_logger.info(failed_change_password_message)
            flash('Invalid password', 'error')
            return redirect(url_for("update_password"))

        # Check for spaces in username and password
        if " " in new_password:
            flash("Password cannot contain spaces.",
                    "error")
            return redirect(url_for("update_password"))

        # Check if the new password and confirm password match
        if new_password != confirm_new_password:
            flash("New password and confirm password do not match. Try again.",
                    "error")
            return redirect(url_for("update_password"))

        # Password complexity validation (same as registration)
        if not (len(new_password) >= 12
                and any(c.isupper() for c in new_password)
                and any(c.islower() for c in new_password)
                and any(c.isdigit() for c in new_password)
                and any(not c.isalnum() for c in new_password)):
            flash("New password does not meet complexity requirements",
                    "error")
            return redirect(url_for("update_password"))

        # Check if the new password is in CommonPasswords.txt.
        with open("static/CommonPasswords.txt", "r",
                    encoding="utf-8") as common_passwords_file:
            print("Debug: Comparing COMMON PASSWORD LIST")
            common_passwords = [line.strip() for line in common_passwords_file]

        if new_password in common_passwords:
            flash("New password is commonly used. Choose a different password.",
                    "error")
            return redirect(url_for("update_password"))

        # Hash the new password before storing it (for security)
        hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()

        # Update the user's password in the database
        cursor.execute("UPDATE Users SET password = %s WHERE username = %s", (hashed_new_password, username))
        db.commit()
        flash("Password updated successfully", "success")
        return redirect(url_for("home"))

    return render_template('update_password.html')


@app.route('/')
def home():
    if 'logged_in' in session:
        current_time = datetime.now()
        return render_template('index.html', current_time=current_time)
    else:
        return redirect(url_for('login'))
   


@app.route('/planetarium', methods=['POST', 'GET'])
def planetarium():
    """
    Render the planetarium volunteer page.

    Returns:
        rendered template for planetarium volunteer page
    """
    # Check if the user is logged in, if not, redirect to the login page
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
     
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']

        username = session['username']

        #first get the userID associated with that name from the Users table
        cursor.execute("SELECT userID FROM Users WHERE username = %s", (username,))
        row = cursor.fetchone()
        userID = row[0]

        #fill that userID into the row with that date and time which are formatted into strings
        cursor.execute("UPDATE Planetarium SET userID = %s WHERE date = %s AND time = %s", (userID, str(date), str(time)))

        db.commit()
        flash('Reservation successful!', 'success')

    return render_template('planetarium.html')


@app.route('/logout')
def logout():
    """
    Log users out by clearing their session data.

    Returns:
        Redirects to the login page with a logout flash message
    """
    # Clear the user's session data to log them out
    session.clear()
    flash('Logout Successful - See you next time!', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()