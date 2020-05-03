import smtplib
from email.mime.multipart import MIMEMultipart
# from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def autoreply(toaddr):
    """Send reply to contact submission."""
    fromaddr = "lynzbts09@gmail.com"
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Subscription reply"

    body = "Congratulations! You've successfully signed up for ArtEvents!"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "Zllovebts09")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def payreply(toaddr, payId):
    """Send reply to contact submission."""
    fromaddr = "lynzbts09@gmail.com"
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Payment reply"

    body = "Congratulations! You've successfully buy your ticket! Your payment ID: " + str(payId) + "  Have a nice day:)"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "Zllovebts09")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def canelreply(toaddr, money):
    """Send reply to contact submission."""
    fromaddr = "lynzbts09@gmail.com"
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Cancel order reply"

    body = "Congratulations! You've successfully cancel ticket! Your money: " + str(
        money) + " is refunded. Have a nice day:)"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "Zllovebts09")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

