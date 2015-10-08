# -*- coding: utf-8 -*- 
def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()
    print 'successfully sent the mail'
        
if __name__=="__main__":
    user = 'nguyenductu@gmail.com'
    pwd='Tu87cucgach'
    recipient='tund@vinaphone.vn'
    subject="hello"
    body='chuc mung ban da gui mail thanh cong'
    send_email(user, pwd, recipient, subject, body)