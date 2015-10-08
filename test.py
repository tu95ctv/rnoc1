# -*- coding: utf-8 -*- 
import smtplib
from email.mime.text import MIMEText

#New add
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
SMTP_USERNAME = "drfuvnp"
SMTP_PASSWORD = "228787"
EMAIL_FROM = "drfuvnp@yahoo.com"
#EMAIL_TO = "nguyenductu@gmail.com"
EMAIL_TO = ["tund@vinaphone.vn",'nguyenductu@gmail.com']
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
def send_email(files=None):
    '''
    msg = MIMEText(co_msg)
    msg['Subject'] = EMAIL_SUBJECT + "nhac nho thembuo n"
    msg['From'] = EMAIL_FROM 
    msg['To'] = emailto
    '''
    
    msg = MIMEMultipart(
        From=EMAIL_FROM,
        To=COMMASPACE.join(EMAIL_TO),# s
        Date=formatdate(localtime=True),
        Subject=EMAIL_SUBJECT + "co dinh kem theo file"
    )
    msg['Subject'] = EMAIL_SUBJECT + "dinh kem"
    msg.attach(MIMEText(co_msg)) #like the first line

    for f in files or []:
        with open(f, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s"' % basename(f),
                Name=basename(f)
            ))
    
    
    debuglevel = True
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, ["tund@vinaphone.vn",'nguyenductu@gmail.com'], msg.as_string())
    mail.quit()

if __name__=='__main__':
    #et='fake'
    send_email(['/home/ductu/workspace/forum/media/for_user_download_folder/KG5733_IUB_W12_3.mo'])
    #for et in ["tund@vinaphone.vn",'nguyenductu@gmail.com']:
        #send_email(et)
    