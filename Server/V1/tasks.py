# # tasks.py (Celery tasks)

# from celery import Celery
# from crawler import crawlerImage
# from datetime import datetime



# @celery.task
# def schedule_task(empid, reportName, email, datetime_str):
#     datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
#     crawlerImage(reportName, "https://www.amazon.com/", empid, email)
# tasks.py

from celery import Celery
from crawler import crawlerImage
from datetime import datetime
from Server.V1.celeryconfig import broker_url

celery = Celery(__name__)
celery = Celery('tasks', broker=broker_url)

@celery.task
def crawl_images(empid, reportName, email):
    crawlerImage(reportName, "https://www.amazon.com/", empid, email)
