import pickle
import os
import base64
import googleapiclient.discovery
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail(subject,body):

    pickle_path = r"C:\Users\james\Documents\python\token.pickle"
    creds = pickle.load(open(pickle_path, 'rb'))
    service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)

    my_email = 'jameslester78@gmail.com'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f'{my_email}'
    msg['To'] = f'{my_email}'
    msgPlain = body
    #msgHtml = '<b>This is my first email!</b>'
    msg.attach(MIMEText(msgPlain, 'plain'))
    #msg.attach(MIMEText(msgHtml, 'html'))
    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}

    message1 = body
    message = (
        service.users().messages().send(
            userId="me", body=message1).execute())
    print('Message Id: %s' % message['id'])