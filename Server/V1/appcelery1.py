# app.py (Flask application)

from flask import Flask, request, jsonify
from Server.V1.tasks import schedule_task
import pymysql
import schedule
import threading
import time
import bcrypt
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MySQL CONNECTION=============================
HOST = 'localhost'
USER = 'root'
PASSWORD = 'Mysqlvarun#2004'
DATABASE = 'RAMCO_TESTDB'

conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
conn.commit()
print(conn)

# UTILITY FUNCTIONS===========================

def format_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(hashed_password, password):
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    if isinstance(password, str):
        password = password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)

# CELERY TASK SCHEDULING======================
def execute_scheduled_tasks():
    print("Checking for pending jobs at:", datetime.now().strftime("%X (%d/%m/%y)"))
    cursor = conn.cursor()
    query = "SELECT * FROM EMP_NT"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    for row in rows:
        empid, reportname, needtime, email = row
        formatted_needtime = format_datetime(needtime)
        print(f"Scheduling task for EmpId: {empid}, ReportName: {reportname}, NeedTime: {formatted_needtime} , email : {email}")
        schedule_task.apply_async(args=(empid, reportname, email, formatted_needtime))

def start_scheduler():
    schedule.every().minute.do(execute_scheduled_tasks)
    while True:
        schedule.run_pending()
        time.sleep(1)

# API ROUTES==================================

# API ROUTES=========================
@app.route('/schedule_report', methods=['POST','OPTIONS'])
def schedule_report():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)
    data = request.json
    empid = data.get('empid')
    reportName = data.get('reportName')
    email = data.get('email')
    datetime_str = data.get('datetime')  # assuming needtime is provided in proper format

    cursor = conn.cursor()
    cursor.execute("INSERT INTO EMP_NT (empid, reportname, needtime, email) VALUES (%s, %s, %s, %s)",
                   (empid, reportName, datetime_str, email))
    conn.commit()
    cursor.close()

    schedule_task.apply_async(args=(empid, reportName, email, datetime_str))

    return jsonify({"message": "Report scheduled successfully."}), 200

@app.route('/get_records/<int:empid>', methods=['GET'])
def get_records(empid):
    cursor = conn.cursor()
    # Fetch records from EMP_NT table
    query = "SELECT * FROM EMP_NT WHERE EmpId = %s ORDER BY status DESC, needtime ASC"
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




# Your other routes...

if __name__ == '__main__':
    scheduler_thread = threading.Thread(target=start_scheduler)
    scheduler_thread.start()
    app.run(debug=True)
