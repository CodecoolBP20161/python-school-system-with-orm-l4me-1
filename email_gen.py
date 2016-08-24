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
        cls.subject = 'qwdioqwjdioqjio'
        cls.send_email()

    @classmethod
    def send_email(cls):
        msg_content = cls.text
        message = MIMEText(msg_content, 'html')
        message['From'] = 'Codecool Team {}'.format(cls.sender)
        message['To'] = 'Receiver Name <l4mecc+{}@gmail.com>'.format(cls.reciever.lower().replace(' ', ''))
        message['Cc'] = ''
        message['Subject'] = cls.subject

        msg_full = message.as_string()
        try:
            smtpObj = SMTP('smtp.gmail.com:587')
            print("wtf")
            smtpObj.starttls()
            print("wtf")
            smtpObj.login(cls.sender, cls.passwd)
            print("wtf")
            print(cls.sender, 'l4mecc+{}@gmail.com'.format(cls.reciever.lower().replace(' ', '')), cls.text)
            smtpObj.sendmail(cls.sender, 'l4mecc+{}@gmail.com'.format(cls.reciever[:1].lower().replace(' ', '')), msg_full)
            print("Succesfully sent email")
        except:
            print("faiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiil")
        smtpObj.quit()

applicant = Applicant.select()[0]
EmailGen.email_to_applicant_with_code(applicant)
