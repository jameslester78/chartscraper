#make this work for more than 1 watch item
#google wont support smtp send soon - move provider or move to alternative google login

import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def send_email():

    '''send the email, you'll need to create a pickle file with gmail account and password in it, code to create file down the bottom'''

    import smtplib, ssl
    import pickle

    with open('C:\\Users\\james\\Documents\\python\\vars.pkl','rb') as f: 
        password, email = pickle.load(f)

    print(email)     

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = email
    receiver_email = email
    password = password
    message = f"""Subject: Church Mead has a date"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

URL = "https://www.parkrun.org.uk/churchmead"
page = requests.get(URL ,headers=headers)

x =  page.text.find('How do I take part')

print(x)

if x<0 :
    send_email()

else:
    print ('found, do nothing')    