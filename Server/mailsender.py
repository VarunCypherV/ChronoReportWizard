##SEND MAIL WITH ATTACHMENTS AS WELL 
import os
import smtplib
from email.message import EmailMessage
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS') #cant use gmail for sending addresses
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


def sendEmail(imgpath,receiverEmail):
    if EMAIL_ADDRESS is None or EMAIL_PASSWORD is None:
        print("Please set the EMAIL_ADDRESS and EMAIL_PASSWORD environment variables.")
    else:
        msg = EmailMessage()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = receiverEmail
        msg['Subject'] = "Test Subject"
        msg.set_content("Test Body")  #CONTENT CRAWLED CAN BE MAILED HERE BY SETTING THIS TO CONTENT

        ##ADD FOR ATTACHMENT REMOVE IF NOT REQUIRED
        with open(imgpath, "rb") as image_file:
            image_data = image_file.read()
            msg.add_attachment(image_data, maintype='image', subtype='jpeg', filename="report.jpeg")

        # with open("cat.pdf", "rb") as pdf_file: 
        #     pdf_data = pdf_file.read()
        #     msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename="cat.pdf")

        with smtplib.SMTP('smtp.outlook.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)


def sendEmailContent(textpath, receiverEmail):
    if EMAIL_ADDRESS is None or EMAIL_PASSWORD is None:
        print("Please set the EMAIL_ADDRESS and EMAIL_PASSWORD environment variables.")
    else:
        msg = EmailMessage()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = receiverEmail
        msg['Subject'] = "Test Subject"
        msg.set_content("Test Body")  # Set the email body here

        # ADD FOR ATTACHMENT REMOVE IF NOT REQUIRED
        with open(textpath, "r") as text_file:
            text_data = text_file.read()
            msg.add_attachment(text_data, filename="report.txt")

        with smtplib.SMTP('smtp.outlook.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)


