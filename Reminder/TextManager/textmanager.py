import smtplib
from email.mime.text import MIMEText
from Reminder.EmailManager.emailmanager import EmailManager

class TextManager(EmailManager):
    def __init__(self):
	return

tm = TextManager()
tm.send_email_to_single_address_gmail('6509317719@tmomail.net', 'huahanzh@gmail.com', 'testemail123', 'test', 'isss body')
