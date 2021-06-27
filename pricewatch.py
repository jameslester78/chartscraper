#youll need to create sqllie db and populate the product table with stuff you want to track before you can use this

import sqlite3

def get_urls():

    '''fetch the urls we want to track from the db'''

    conn = sqlite3.connect('pythonsqlite.db') #file has to sit in the same dir as code, if you run it from scheduler, i had to put it in sys32
    x= conn.cursor()
    sel = 'select name,url from product'
    return x.execute(sel).fetchall()


def get_price(product,url):

    '''scrape the product price from sainsburys'''

    import json
    from urllib import request

    #page = request.urlopen('https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product?filter%5Bproduct_seo_url%5D=gb/groceries/marmite-250g&include%5BASSOCIATIONS%5D=true&include%5BPRODUCT_AD%5D=citrus').read()
    page = request.urlopen(url).read()

    json = json.loads(page)
    price = json['products'][0]['retail_price']['price']


    return price,product

def ins_data(val,product):

    '''insert the current price into the db'''

    conn = sqlite3.connect('pythonsqlite.db')
    x= conn.cursor()

    ins = 'insert into history (test,product) values ("'+str(val)+'","'+product+'")'

    x.execute(ins)
    conn.commit()
    x.close()

def get_latest_value(product):

    '''find the last recorded price from the db'''

    conn = sqlite3.connect('pythonsqlite.db')
    x= conn.cursor()

    sel =  f'select test from history where product = "{product}" order by date desc limit 1'
    #print (sel)


    result = x.execute(sel).fetchall()

    x.close()

    if len(result)>0:
        return (result[0][0])
    else:
        return 0

def has_price_changed(old,new):

    '''has the price changed? durr'''

    if str(old) == str(new):
        return 0
    else:
        return 1

def send_email(product,price):

    '''send the email, you'll need to create a pickle file with gmail account and password in it, code to create file down the bottom'''

    import smtplib, ssl
    import pickle


    with open('vars.pkl','rb') as f: 
        password, email = pickle.load(f)

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = email
    receiver_email = email
    password = password
    message = f"""\
    Subject: Price Alert

    The price of {product} has changed, it now costs {price}"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


for i in get_urls():
    product = i[0]
    url = i[1]

    #print (f"{product=} {url=}")

    price,product = get_price(product,url)

    #print (f"{product=} {price=}")

    prev = get_latest_value(product)

    #print (f"{prev=}")

    ins_data(price,product)

    changed = has_price_changed(prev,price)

    if changed  == 1:
        send_email(product,price) 
        





'''

create your password file

password = 'your email password'
email = 'your email address'

with open('vars.pkl','wb') as f:
    pickle.dump([password,email],f)
'''

'''

    CREATE The following tables in your sql lite db

    CREATE TABLE history (
        date                  DEFAULT (CURRENT_TIMESTAMP),
        test,
        product VARCHAR (100) 
    );


    CREATE TABLE product (
        name,
        url
    );


'''
