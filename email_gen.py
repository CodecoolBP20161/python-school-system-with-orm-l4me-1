from smtplib import *
import json
from email.mime.text import MIMEText


class EmailGen():
    sender = None
    passwd = None
    subject = None
    reciever = None
    text = None

    @classmethod
    def check_smtp_requirements(cls):
        try:
            with open('login.json') as data_file:
                data = json.load(data_file)
                cls.sender = data["sender"]
                cls.passwd = data["passwd"]
            smtpObj = SMTP('smtp.gmail.com:587')
            smtpObj.starttls()
            smtpObj.login(cls.sender, cls.passwd)
            smtpObj.quit()
        except SMTPAuthenticationError:
            print("Incorrect smtp details. Please check your login data in .json file")
            exit()
        except KeyError:
            print("Missing smtp details. Please check your login data in .json file")
            exit()
        except json.decoder.JSONDecodeError:
            print("Empty .json file. Please check your login data in .json file")
            exit()
        except IOError:
            print("Missing .json file. Please read README.md for instructions")
            exit()

    @classmethod
    def send_email(cls):
        msg_content = cls.text
        message = MIMEText(msg_content, 'html')
        message['From'] = cls.sender
        message['To'] = cls.reciever
        message['Cc'] = ''
        message['Subject'] = cls.subject

        msg_full = message.as_string()

        try:
            smtpObj = SMTP('smtp.gmail.com:587')
            smtpObj.starttls()
            smtpObj.login(cls.sender, cls.passwd)
            smtpObj.sendmail(cls.sender, cls.reciever, msg_full)
            print("Succesfully sent email")
        except:
            print("fail")
        smtpObj.quit()
