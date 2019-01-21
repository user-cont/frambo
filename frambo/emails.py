from logging import getLogger
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
from email.mime.text import MIMEText

from frambo.utils import text_from_template


SENDER_EMAIL = ""
SMTP_SERVER = ""

logger = getLogger(__name__)


def build_email_message(template_dir, template_filename, template_data):
    """Redirect"""
    return text_from_template(template_dir, template_filename, template_data)


def send_email(text, receivers, subject):
    """
    Send an email from SENDER_EMAIL to all provided receivers
    :param text: string, body of email
    :param receivers: list, email receivers
    :param subject: string, email subject
    """
    logger.info('Sending email to: %s', str(receivers))
    sender = SENDER_EMAIL

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(receivers)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    smtp = SMTP(SMTP_SERVER)
    smtp.sendmail(sender, receivers, msg.as_string())
    smtp.close()
    logger.debug('Email sent')
