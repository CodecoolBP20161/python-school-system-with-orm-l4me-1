from applicant import *
from mentor import *
from interview_slot import *
from school import *
from smtplib import *
import json
from email.mime.text import MIMEText

with open('login.json') as data_file:
    data = json.load(data_file)


class EmailGen():
    sender = 'l4mecc@gmail.com'
    passwd = 'hipermagnum'
    subject = None
    reciever = None
    text = None

    @classmethod
    def email_to_applicant_with_code(cls, person):
        cls.text = '<h2>Teszt </h2> <font color="green">OK</font></h2>'
        cls.reciever = person.full_name
        cls.subject = 'applicant code'
        cls.send_email()

    @classmethod
    def send_email(cls):
        msg_content = cls.text
        message = MIMEText(msg_content, 'html')
        message['From'] = cls.sender
        message['To'] = cls.reciever
        message['Cc'] = ''
        message['Subject'] = cls.subject

        try:
            smtpObj = SMTP('smtp.gmail.com:587')
            smtpObj.starttls()
            smtpObj.login(cls.sender, cls.passwd)
            smtpObj.sendmail(cls.sender, cls.reciever, cls.text)
            print("Succesfully sent email")
        except:
            print("fail")
        smtpObj.quit()

applicant = Applicant.select()[0]
EmailGen.email_to_applicant_with_code(applicant)
