from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from time import sleep
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
FILE = "offers.json"

# -*- coding: utf-8 -*-

while True:
    chrome_options = webdriver.ChromeOptions()
    # add the argument to reuse an existing tab
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--reuse-tab") 
    chrome_options.add_argument("--headless")
    #chrome_options.add_argument('--disable-dev-shm-usage')
    # create the ChromeDriver object
    driver = webdriver.Chrome(options=chrome_options) #service=Service("/usr/bin/chromedriver"), 
    link = 'https://www.wochenanzeiger.de/mietangebote/'
    try:
        driver.get(link)
    except WebDriverException:
        print("Error loading page")
        driver.quit()
        sleep(60)
        continue
    driver.implicitly_wait(10)
    iframe = (driver.find_elements("xpath", '//*[@class="content"]')[0]
    .find_elements("xpath", '//*[@class="mittlereleiste"]')[0]
    .find_elements("xpath", '//*[@class="spalten2_l560"]')[0]
    .find_elements("xpath", '//*[@class="anonza_box"]')[0]
    .find_elements("xpath", '//*[@id="iFrameResizer0"]')[0]
    ) 
    driver.switch_to.frame(iframe)
    offers = (driver.find_elements("xpath", '//*[@id="mmenu_page"]')[0]
    .find_elements("xpath", '//*[@id="mmenu_page"]')[0]
    .find_elements("xpath", '//*[@class="row"]')[0]
    .find_elements("xpath", '//*[@class="col-md-8"]')[0]
    .find_elements("xpath", '//*[@class="auk_container_rows"]')[0]
    .find_elements("xpath", '//*[@class="aukrow row"]')
    )
    
    if os.path.isfile(FILE):
        with open(FILE) as old_file:
            data_old = json.load(old_file)
    else: data_old = []
    
    offerstrs = [offer.text.encode('utf-8').decode('utf-8') for offer in offers]
    new_offers = set(offerstrs) - set(data_old)
    
    if new_offers:
        msg = MIMEMultipart()
        email = os.environ['EMAIL']
        msg['Subject'] = 'Neue Wochenanzeigen gefunden!'
        msg['From'] = email
        msg['To'] = email
        msg.attach(MIMEText('\n'.join(new_offers + [link])))

        mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(email, os.environ['EMAIL_PW'])

        mailserver.sendmail(email, [email], msg.as_string())
        mailserver.quit()
        print("New offers:")
        print(new_offers)
    else:
        print("No new offers found")
        
    with open(FILE, "w") as new_file:
        json.dump(offerstrs, new_file)
    driver.quit()
    sleep(300)
driver.quit()
display.stop()