# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import smtplib
import os

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def submit_app(ref):
    link = 'https://www.wg-gesucht.de/' + ref
    msg = MIMEMultipart()
    email = os.environ['EMAIL']
    msg['Subject'] = 'Neue WG-Anzeige gefunden!'
    msg['From'] = email
    msg['To'] = email
    msg.attach(MIMEText(link))

    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login(email, os.environ['EMAIL_PW'])

    mailserver.sendmail(email, [email], msg.as_string())
    mailserver.quit()

        