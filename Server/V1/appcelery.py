# app.py

from flask import Flask, request, jsonify
from celery import Celery
from Server.V1.tasks import crawl_images
from datetime import datetime
import pymysql
import bcrypt
from flask_cors import CORS
from Server.V1.celeryconfig import broker_url
app = Flask(__name__)
CORS(app)

app.config['CELERY_BROKER_URL'] = broker_url  # Example Redis broker URL
celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])

HOST = 'localhost'
USER = 'root'
PASSWORD = 'Mysqlvarun#2004'
DATABASE = 'RAMCO_TESTDB'

conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
conn.commit()

def format_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')

@app.route('/schedule_report', methods=['POST'])
def schedule_report():
    data = request.json
    empid = data.get('empid')
    reportName = data.get('reportName')
    email = data.get('email')
    datetime_str = data.get('datetime')
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    cursor = conn.cursor()
    cursor.execute("INSERT INTO EMP_NT (empid, reportname, needtime, email) VALUES (%s, %s, %s, %s)",
                   (empid, reportName, datetime_obj, email))
    conn.commit()
    cursor.close()

    crawl_images.apply_async((empid, reportName, email), eta=datetime_obj)
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

if __name__ == '__main__':
    app.run(debug=True)
