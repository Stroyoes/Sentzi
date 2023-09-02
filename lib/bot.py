# the anonymous email bot

import smtplib
import typing
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from lib.config import DEV_EMAIL_ID, DEV_PASS

# email configs
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = DEV_EMAIL_ID
sender_password = DEV_PASS

def send(
        to : str, # eamil string
        From : str, # email string
        name : str, # user name
        pd_name : str, # pd name

) -> bool:
    subj = f' Sentzi : 🎉 New product from {name} ! 🎉 '
    html_msg = f"""
    <h2 id="-pd_name-"><code>{pd_name}</code></h2>
    <p><a href="mailto:{From}"><code>{name}</code></a> has just created an ✨ awesome ✨ new product (<code>{pd_name}</code>)and he&#39;d want to share it to you.</p>
    <p>So, simply spread your love 😊 . Visit <a href="https://cdn.jsdelivr.net/gh/sreezx/Sentzi/data/review.png"><code>here</code></a></p> to know more . 
    <p>Created with ❤️ using <a href="https://github.com/sreezx/Sentzi"><code>Sentzi</code></a></p>
    """

    msg = MIMEMultipart()
    msg['Subject'] = subj
    msg.attach(MIMEText(html_msg , "html"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)

        # start TLS for security
        server.starttls()

        # auth
        server.login(
            sender_email,
            sender_password
        )

        # send the msg
        server.sendmail(
            sender_email,
            to,
            msg.as_string()
        )

        # terminating the session
        server.quit()
        return True
    except Exception:
        return False


