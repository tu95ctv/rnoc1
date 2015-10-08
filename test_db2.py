# -*- coding: utf-8 -*- 
import smtplib
from email.mime.text import MIMEText
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
SMTP_USERNAME = "drfuvnp"
SMTP_PASSWORD = "228787"
EMAIL_FROM = "drfuvnp@yahoo.com"
#EMAIL_TO = "nguyenductu@gmail.com"
EMAIL_TO = "tund@vinaphone.vn"
EMAIL_SUBJECT = "REMINDER:"
co_msg = """
Hello, [username]! Hello :
[Company]
Where: [companyAddress]
Time: [appointmentTime]
Company URL: [companyUrl]
Change appointment?? Add Service??
change notification preference (text msg/email)
"""
def send_email(emailto):
    msg = MIMEText(co_msg)
    msg['Subject'] = EMAIL_SUBJECT + "nhac nho thembuo n"
    msg['From'] = EMAIL_FROM 
    msg['To'] = emailto
    
    
    
    
    debuglevel = True
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mail.quit()

if __name__=='__main__':
    for et in ["tund@vinaphone.vn",'nguyenductu@gmail.com']:
        send_email(et)
    