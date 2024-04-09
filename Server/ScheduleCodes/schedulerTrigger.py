import pypyodbc as odbc 
#pip install pypyodbc
#pip install schedule
import time
import schedule
import threading
import datetime
from crawler import crawlerImage,crawlerContent

#MS SQL CONNECTION=============================
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME ='VARUN'
DATABASE_NAME='RAMCO_TESTDB'
connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={{{DATABASE_NAME}}};
    Trusted_Connection=yes;
"""
conn = odbc.connect(connection_string)
conn.commit()
print(conn)

#UTILITY FUNCTIONS===========================

def get_time() -> str: #return type is specified using -> str meaning return type is string
    return time.strftime("%X (%d/%m/%y)")

def format_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def create_tag(scheduled_datetime,empid,reportName):
    return str(scheduled_datetime)+str(empid)+reportName+str(reportName)

#THREADING AND PROJECT OBJECTIVE FUNCTIONS========================
def start_thread(empid,reportName,email): #If Multiple Employee schedule for same time , hence i have done threading here
    job = threading.Thread(target=lambda: task(empid,reportName,email))
    job.start()

def task(empid,reportName,email):  #Primary function for crawler and it ensures that only once it is run since package has no other option
   crawlerImage(reportName,"https://www.amazon.in",empid,email)
   crawlerContent(reportName,"https://www.amazon.in",empid,email)
   return schedule.CancelJob 

def ExecuteQuery():  #Accessing the backend for data
    print("fetched at " ,get_time())
    cursor = conn.cursor()
    query = "SELECT * FROM EMP_Trigger"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    for row in rows:
        empid, reportname, needtime , email , triggerCheck= row
        formatted_needtime = format_datetime(needtime)
        print(f"EmpId: {empid}, ReportName: {reportname}, NeedTime: {formatted_needtime} , email : {email} , Trigger :{triggerCheck}")
        if(triggerCheck=='YES'):
           schedulemytask(formatted_needtime,empid,reportname,email)

schedule.every().minute.do(ExecuteQuery) #ENTRY POINT : CUSTOMIZABLE => Testing Purpose its every 1 minute

def schedulemytask(scheduled_datetime,empid,reportName,email):
    schedule_date,scheduled_time=scheduled_datetime.split(" ")
    generated_tag=create_tag(scheduled_datetime,empid,reportName)  #generating unique tag since library tag doesnt give an id
    if(datetime.datetime.now().strftime("%Y-%m-%d")==schedule_date and schedule.get_jobs(generated_tag)==[]):
         schedule.every().day.at(scheduled_time).do(lambda: start_thread(empid,reportName,email)).tag(generated_tag)
    
#=====================SCHEDULE IS RUNNING=========================
while True:
    schedule.run_pending()
    time.sleep(1)



