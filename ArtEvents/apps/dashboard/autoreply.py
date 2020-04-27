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
    server.login(fromaddr, "PASSWORD FOR FROMADDR")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
