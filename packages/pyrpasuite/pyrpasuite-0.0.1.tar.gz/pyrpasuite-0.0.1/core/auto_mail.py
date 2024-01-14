import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import decode_header
import os

class AutoEmailSender:
    """
    A class to automate email operations.

    :param smtp_server: The SMTP server to use.
    :param smtp_port: The port to use for the SMTP server.
    :param email: The email address to use.
    :param password: The password for the email account.
    """

    def __init__(self, smtp_server: str, smtp_port: int, email: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    def send_email(self, to_email: str, subject: str, body: str) -> None:
        """
        Send an email.

        :param to_email: The email address to send to.
        :param subject: The subject of the email.
        :param body: The body of the email.
        """
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.email, self.password)
        text = msg.as_string()
        server.sendmail(self.email, to_email, text)
        server.quit()

    def send_email_with_attachment(self, to_email: str, subject: str, body: str, file_path: str) -> None:
        """
        Send an email with an attachment.

        :param to_email: The email address to send to.
        :param subject: The subject of the email.
        :param body: The body of the email.
        :param file_path: The path of the file to attach.
        """
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Open the file in bynary mode
        binary_file = open(file_path, "rb")

        payload = MIMEBase('application', 'octate-stream', Name=file_path)
        # To change the payload into encoded form
        payload.set_payload((binary_file).read())
        # enconding the binary into base64
        encoders.encode_base64(payload)

        # add header with pdf name
        payload.add_header('Content-Decomposition', 'attachment', filename=file_path)
        msg.attach(payload)

        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.email, self.password)
        text = msg.as_string()
        server.sendmail(self.email, to_email, text)
        server.quit()



import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import decode_header
import os

class AutoEmailReader:
    """
    A class to automate email reading operations.

    :param imap_server: The IMAP server to use.
    :param imap_port: The port to use for the IMAP server.
    :param email: The email address to use.
    :param password: The password for the email account.
    """

    def __init__(self, imap_server: str, imap_port: int, email: str, password: str):
        """
        Initialize AutoEmailReader with the necessary credentials.

        :param imap_server: The IMAP server to use.
        :param imap_port: The port to use for the IMAP server.
        :param email: The email address to use.
        :param password: The password for the email account.
        """
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.email = email
        self.password = password
    
    def read_email(self, mailbox: str = 'inbox', email_filter: str = 'ALL', attachment_path: str = r'C:\Users') -> tuple:
        """
        Read an email.

        :param mailbox: The mailbox to read from. Defaults to 'inbox'.
        :param email_filter: The filter to use when searching for emails. Defaults to 'ALL'.
        :param attachment_path: The path to save attachments to. Defaults to 'C:\\Users'.
        :return: The subject, body, and attachments of the email.
        """
        # Connect to the server
        imap = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)

        # Authenticate
        imap.login(self.email, self.password)

        try:
            # Select the mailbox
            imap.select(mailbox)

            # Search for specific mail
            res, msg_ids = imap.uid('search', None, email_filter)
            # If the email is not found, inform the user
            if not msg_ids[0]:
                return "No emails found."
            else:
                msg_id_list = msg_ids[0].split()
                latest_email_id = msg_id_list[-1] # get the latest

                # Fetch the email body (RFC822) for the given ID
                result, email_data = imap.uid('fetch', latest_email_id, '(BODY.PEEK[])')
                raw_email = email_data[0][1].decode("utf-8")
                email_message = email.message_from_string(raw_email)

                # Decode email subject
                subject = decode_header(email_message['Subject'])[0][0]
                if isinstance(subject, bytes):
                    # If it's a bytes type, decode to str
                    subject = subject.decode()

                # Get the email body
                if email_message.is_multipart():
                    for part in email_message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(decode=True)
                else:
                    body = email_message.get_payload(decode=True)

                # Get the attachments
                attachments = []
                for part in email_message.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    fileName = part.get_filename()

                    if bool(fileName):
                        filePath = os.path.join(attachment_path, fileName)
                        with open(filePath, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        attachments.append(filePath)

                return subject, body, attachments
        finally:
            imap.logout()
        
    def filter_emails(self, mailbox: str = 'inbox', search_criterion: str = 'ALL') -> list:
        """
        Filter emails.

        :param mailbox: The mailbox to filter in. Defaults to 'inbox'.
        :param search_criterion: The criterion to use when filtering emails. Defaults to 'ALL'.
        :return: A list of email IDs that match the filter.
        """
        # Connect to the server
        imap = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)

        # Authenticate
        imap.login(self.email, self.password)

        try:
            # Select the mailbox
            imap.select(mailbox)

            # Search for specific mail
            res, msg_ids = imap.uid('search', None, search_criterion)
            # If the email is not found, inform the user
            if not msg_ids[0]:
                return "No emails found."
            else:
                return msg_ids[0].split()
        finally:
            imap.logout()
