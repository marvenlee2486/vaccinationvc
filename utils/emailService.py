import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.config import ENV


def email_service(sharable_url, qr_code, receiver_email):
    context = ssl.create_default_context()
    
    sender_email = ENV.MAIL_ADDRESS
    receiver_email = receiver_email

    msg = MIMEMultipart('alternative')
    msg["Subject"] = "Vaccine Credentials"
    msg["From"] = sender_email
    msg["To"] = receiver_email


    html_message = f"""\
        <html>
        <head></head>
        <body>
            <p>Dear Sir/Mdm,
            <br>
            <br>
            Here is the sharable URL for your vaccine credentials: <a href={sharable_url}>Vaccine Cert URL</a>
            <br>
            <br>
            Regards
            </p>
        </body>
        </html>
    """

    part2 = MIMEText(html_message, 'html')

    msg.attach(part2)

    with smtplib.SMTP_SSL("smtp.gmail.com", ENV.MAIL_PORT, context=context) as server:
        server.login(ENV.MAIL_ADDRESS, ENV.MAIL_PASSWORD)
        server.sendmail(sender_email, receiver_email, msg.as_string())