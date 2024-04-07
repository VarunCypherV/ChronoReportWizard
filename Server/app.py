from flask import Flask, request, jsonify
import pymysql
import schedule
import threading
import datetime
import time
from flask_cors import CORS # Import CORS from flask_cors
from crawler import crawlerImage

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

def get_time() -> str:
    return time.strftime("%X (%d/%m/%y)")

def format_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def create_tag(scheduled_datetime, empid, reportName):
    return str(scheduled_datetime) + str(empid) + reportName + str(reportName)

# THREADING AND PROJECT OBJECTIVE FUNCTIONS========================
def start_thread(empid, reportName, email):
    job = threading.Thread(target=lambda: task(empid, reportName, email))
    job.start()

def task(empid, reportName, email):
    crawlerImage(reportName, "https://www.amazon.com/", empid, email)
    return schedule.CancelJob

def ExecuteQuery():
    print("fetched at ", get_time())
    cursor = conn.cursor()
    query = "SELECT * FROM EMP_NT"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    for row in rows:
        empid, reportname, needtime, email = row
        formatted_needtime = format_datetime(needtime)
        print(f"EmpId: {empid}, ReportName: {reportname}, NeedTime: {formatted_needtime} , email : {email}")
        schedulemytask(formatted_needtime, empid, reportname, email)

schedule.every().minute.do(ExecuteQuery)

def schedulemytask(scheduled_datetime, empid, reportName, email):
    schedule_date, scheduled_time = scheduled_datetime.split(" ")
    generated_tag = create_tag(scheduled_datetime, empid, reportName)
    if (datetime.datetime.now().strftime("%Y-%m-%d") == schedule_date and schedule.get_jobs(generated_tag) == []):
        time.sleep(1)
        schedule.every().day.at(scheduled_time).do(lambda: start_thread(empid, reportName, email)).tag(generated_tag)

#=====================SCHEDULE IS RUNNING=========================
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# API ROUTES=========================
@app.route('/schedule_report', methods=['POST'])
def schedule_report():
    data = request.json
    empid = data.get('empid')
    reportName = data.get('reportName')
    email = data.get('email')
    datetime = data.get('datetime')  # assuming needtime is provided in proper format
    print()
    print(datetime)
    print()
    # Insert into database
    cursor = conn.cursor()
    cursor.execute("INSERT INTO EMP_NT (empid, reportname, needtime, email) VALUES (%s, %s, %s, %s)",
                   (empid, reportName, datetime, email))
    conn.commit()
    cursor.close()
    # Schedule task
    schedulemytask(datetime, empid, reportName, email)
    return jsonify({"message": "Report scheduled successfully."}), 200

if __name__ == '__main__':
    threading.Thread(target=run_schedule).start()  # Start the schedule in a separate thread
    app.run(debug=True)
