import smtplib

def sendEmail(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login('primarymathletes@gmail.com', 'qwopzxnm10')
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail('primarymathletes@gmail.com', 'c16703349@mytudublin.ie', message)
        server.quit()
        print("Email sent successfully.")
    except:
        print("Email failed to send.")
    

subject = "Students Report"
msg = "test message"

sendEmail(subject, msg)
