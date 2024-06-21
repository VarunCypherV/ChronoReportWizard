from flask import Flask, request, jsonify
import pymysql
import schedule
import threading
import datetime
import time
import bcrypt
from flask_cors import CORS # Import CORS from flask_cors
from apscheduler.schedulers.background import BackgroundScheduler
from crawler import crawlerImage

app = Flask(__name__)
CORS(app)
#SCHEDULER=============================================
scheduler = BackgroundScheduler()
scheduler.start()

# MySQL CONNECTION=============================
HOST = 'localhost'
USER = 'root'
PASSWORD = ''
DATABASE = 'ChronoWiz'

conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
conn.commit()
print(conn)

# UTILITY FUNCTIONS===========================

def get_time() -> str:
    return time.strftime("%X (%d/%m/%y)")

def format_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def schedulerdateformater(dt):
    return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')

def create_tag(scheduled_datetime, empid, reportName):
    return str(scheduled_datetime) + str(empid) + reportName + str(reportName)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# VERIFY PASSWORD FUNCTION
def verify_password(hashed_password, password):
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    if isinstance(password, str):
        password = password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)


# API ROUTES=========================
@app.route('/schedule_report', methods=['POST'])
def schedule_report():
    data = request.json
    empid = data.get('empid')
    reportName = data.get('reportName')
    email = data.get('email')
    datetimez = data.get('datetime') 

    # Insert into database
    cursor = conn.cursor()
    cursor.execute("INSERT INTO EMP_NT (empid, reportname, needtime, email) VALUES (%s, %s, %s, %s)",
                   (empid, reportName, datetimez, email))
    conn.commit()
    cursor.close()
    scheduled_datetime = datetime.datetime.strptime(datetimez, '%Y-%m-%d %H:%M:%S')

    scheduler.add_job(crawlerImage, 'date', run_date=scheduled_datetime, args=[reportName, "https://www.amazon.com/", empid, email])

    return jsonify({"message": "Report scheduled successfully."}), 200



@app.route('/get_records/<int:empid>', methods=['GET'])
def get_records(empid):
    cursor = conn.cursor()
    # Fetch records from EMP_NT table
    query = "SELECT * FROM EMP_NT WHERE EmpId = %s ORDER BY status DESC, needtime DESC"
    cursor.execute(query, (empid,))
    rows = cursor.fetchall()
    # Fetch email from employees table
    query_email = "SELECT email FROM employees WHERE empid = %s"
    cursor.execute(query_email, (empid,))
    email_row = cursor.fetchone()
    if email_row:
        email = email_row[0]
    else:
        email = None
    records = []
    if rows :
        for row in rows:
            requestid, empid, reportname, needtime, _, status = row  # Exclude email from EMP_NT query
            formatted_needtime = format_datetime(needtime)
            record = {
                "requestid": requestid,
                "empid": empid,
                "reportname": reportname,
                "needtime": formatted_needtime,
                "status": status
            }
            records.append(record)

    response = {
        "email": email,
        "records": records
    }
    cursor.close()
    return jsonify(response), 200


#=======================================================================
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Hash the password before storing in the database
    hashed_password = hash_password(password)

    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (email, password) VALUES (%s, %s)", (email, hashed_password))
    conn.commit()

    
    cursor.execute("SELECT LAST_INSERT_ID()")
    empid = cursor.fetchone()[0]
    cursor.close()
    
    return jsonify({"empid": empid, "message": "User registered successfully."}), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    empid = data.get('empid')
    password = data.get('password')
    print("Login request received for empid:", empid)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM employees WHERE empid = %s", (empid,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        hashed_password = row[0]
        if verify_password(hashed_password, password):
            return jsonify({"message": "Login successful."}), 200
        else:
            return jsonify({"error": "Invalid credentials."}), 401
    else:
        return jsonify({"error": "User not found."}), 404



def start_flask_app():
    app.run()

if __name__ == '__main__':
    app.run(debug=True)