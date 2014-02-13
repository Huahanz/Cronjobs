import smtplib
from email.mime.text import MIMEText


class EmailManager:
    def __init__(self):
        return

    def send_email_to_single_address_localhost(self, to_addr, from_addr, subject, textfile):
        fp = open(textfile, 'rb')
        msg = MIMEText(fp.read())
        fp.close()

        msg['Subject'] = subject
        msg['From'] = to_addr
        msg['To'] = from_addr

        s = smtplib.SMTP('localhost')
        s.sendmail(from_addr, [to_addr], msg.as_string())
        s.quit()


    def send_email_to_single_address_gmail(self, to_addr, gmail_user, gmail_pwd, subject, body):
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        try:
	    smtpserver.login(gmail_user, gmail_pwd)
	except:
	    print 'Email failed login'
	    return
        header = 'To:' + to_addr + '\n' + 'From: ' + gmail_user + '\n' + subject + ' \n'
        msg = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (gmail_user, to_addr, subject, body)
        #        print msg
        smtpserver.sendmail(gmail_user, to_addr, msg)
        print 'done!'
        smtpserver.close()

    def send_to_defaults(self, subject, body):
	#self.send_email_to_single_address_gmail('nasdaqstock.cronjobs@gmail.com', 'nasdaqstock.cronjobs@gmail.com', 'testemail123', subject, body)
	#self.send_email_to_single_address_gmail('huahanzh@gmail.com', 'nasdaqstock.cronjobs@gmail.com', 'testemail123', subject, body)
	self.send_email_to_single_address_gmail('huahanzh@gmail.com', 'huahanzh@gmail.com', 'testemail123', subject, body)

#em = EmailManager()
#em.send_email_to_single_address_gmail('6509317719@tmomail.net', 'huahanzh@gmail.com', 'testemail123', 'test', 'isss body')
