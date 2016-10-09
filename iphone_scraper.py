from bs4 import BeautifulSoup
from urllib2 import urlopen
import smtplib
from email.mime.text import MIMEText
import logins
import tweepy
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


EMAIL_TO = ["kaiwei_koh@mymail.sutd.edu.sg","mychkoh@yahoo.com"]
EMAIL_SPACE = ", "
EMAIL_SUBJECT = "iPhone Is Available!!!"

def get_iphone_avail(color):
  nid_codes = [["ST Shop",992,False],["Biz ST Shop",991,False],["Easy Mobile",2102,False],["Bedok Mall",2521,False],["Parkway Parade",2516,False],["Tamp Mall",2520,False],["Waterway Pt",2676,False]]
  BASE_URL = "http://info.singtel.com/personal/phones-plans/mobile/ios/iphone7-updates?type=1&device=2790&colour="+color+"&dispatcher=302"
  html = urlopen(BASE_URL).read()
  soup = BeautifulSoup(html,'html.parser')
  email_message = "The following stores have stock: \n"
  no_of_shops = 0
  for shop in nid_codes:
    if(soup.select(".nid-"+str(shop[1])+" > .available")):
      email_message += shop[0] +"\n"
      no_of_shops +=1
  return email_message, no_of_shops

def send_email(message):
  msg = MIMEText(message)
  msg['Subject'] = EMAIL_SUBJECT
  msg['To'] = EMAIL_SPACE.join(EMAIL_TO)
  msg['From'] = logins.gmail
  mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
  mail.starttls()
  mail.login(logins.gmail, logins.gmail_password)
  mail.sendmail(logins.gmail, EMAIL_TO, msg.as_string())
  mail.quit()

def auth_twitter():
  auth = tweepy.OAuthHandler(logins.t_key, logins.t_secret)
  auth.set_access_token(logins.t_access_token, logins.t_access_secret)
  api = tweepy.API(auth)
  return api

availability = get_iphone_avail("black")
# print(availability)
if(availability[1]!=0):
  send_email(availability[0])
  API = auth_twitter()
  API.update_status(status=availability[0]+"@mychkoh")
