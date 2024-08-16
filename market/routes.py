from market import app
from flask import render_template, redirect, url_for
from market.models import Item, User
from market.forms import RegisterForm
from market import db

''' db.drop_all()
   db.create_all()
   i1 = Item(name=a, price=price_amazon, company='Amazon', description='Yessss')
   i2 = Item(name=a, price=price_snapdeal, company='Snapdeal', description='Yesaps')
   i3 = Item(name=a, price=price_flipkart, company='Flipkart',description='Yeapss')
   db.session.add(i1)
   db.session.commit()
   db.session.add(i2)
   db.session.commit()
   db.session.add(i3)
   db.session.commit()'''

"""#HEADERS"""
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'Accept-Language':'en-in'}


"""#IMPORTS"""

import csv
import requests
import time
from bs4 import BeautifulSoup as bs








"""#INPUT FROM BACKEND"""


a = 'Iphone 10'

"""#AMAZON DATA EXTRACTION

"""

base="www.amazon.in"
def get_url(search_term):
    template='https://www.amazon.in/s?k={}&ref=nb_sb_noss_2'
    search_term=search_term.replace(' ','+')
    return template.format(search_term)
url=get_url(a)


response=requests.get(url, headers=HEADERS)
html=response.content


"""#CREATING SOUP FOR AMAZON"""

soup=bs(html,'html.parser')
results=soup.find_all('div',{'data-component-type':'s-search-result'})
item=results[0]
atag=item.h2.a
des=atag.text.strip()
url=base+atag.get('href')
price_amazon=item.find('span', 'a-offscreen').text
#price=pp.find('span', 'a-offscreen').text
#print("amazon-->" + price_amazon)

"""#SNAPDEAL EXTRACTION"""

base1="https://www.snapdeal.com/"
def get_url(search_term1):

    template='https://www.snapdeal.com/search?keyword={}&sort=rlvncy'
    search_term1=search_term1.replace(' ','+')
    return template.format(search_term1)
url = get_url(a)
response=requests.get(url)
html=response.content

"""#CREATING SOUP FOR SNAPDEAL"""

soup1=bs(html,"html.parser")
results=soup1.find_all('div',{'data-js-pos':'0'})
item=results[0]
atag1=item.a
des=atag1.text.strip()
url=atag1.get('href')
price_snapdeal=item.find('span', 'lfloat product-price').text
#price_snapdeal = price_snapdeal - 'Rs. '
#price_snapdeal = price_snapdeal + '₹'
#print("snapdeal-->" + price_snapdeal)

"""#DATA EXTRACTION FOR FLIPKART"""

base2="www.flipkart.com"
def get_url(search_term):
    template='https://www.flipkart.com/search?q={}'
    search_term=search_term.replace(' ','+')
    return template.format(search_term)
url=get_url(a)
response=requests.get(url)
html=response.content

"""#CREATING SOUP FOR FLIPKART"""

soup2=bs(html,'html.parser')
results=soup2.find_all('div',{'class':'_13oc-S'})

item=results[0]
atag3=item.a
des=atag3.text.strip()
url=base2+atag3.get('href')
url1="https://"+url
response=requests.get(url1)

html1=response.content
soup3=bs(html1,'html.parser')
results1=soup3.find_all('div', {'class':'_30jeq3'})
price_flipkart = results1[0].text


#print("flipkart-->" + price_flipkart)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():


    db.create_all()
    i1 = Item(name=a, price=price_amazon, company='Amazon', description='Yessss')
    i2 = Item(name=a, price=price_snapdeal, company='Snapdeal', description='Yesaps')
    i3 = Item(name=a, price=price_flipkart, company='Flipkart', description='Yeapss')
    db.session.add(i1)
    db.session.commit()
    db.session.add(i2)
    db.session.commit()
    db.session.add(i3)
    db.session.commit()

    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    return render_template('register.html', form=form)

