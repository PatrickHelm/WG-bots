from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from time import sleep
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from webdriver_manager.chrome import ChromeDriverManager
FILE = "offers.json"

while True:
    chrome_options = webdriver.ChromeOptions()
    # add the argument to reuse an existing tab
    chrome_options.add_argument("--reuse-tab") 
    #chrome_options.add_argument("--headless")
    # create the ChromeDriver object
    driver = webdriver.Chrome(service=Service("/usr/bin/google-chrome"), options=chrome_options) 
    driver.get('https://www.wochenanzeiger.de/mietangebote/')
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
    
    offerstrs = [offer.text for offer in offers]
    new_offers = set(offerstrs) - set(data_old)
    
    if new_offers:
        msg = MIMEMultipart()
        email = os.environ['EMAIL']
        msg['Subject'] = 'Neue Wochenanzeigen gefunden!'
        msg['From'] = email
        msg['To'] = email
        msg.attach(MIMEText('\n'.join(offerstrs)))

        mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(email, os.environ['EMAIL_PW'])

        mailserver.sendmail(email, [email], msg.as_string())
        mailserver.quit()
        
    with open(FILE, "w") as new_file:
        json.dump(offers, new_file)

    sleep(60)
driver.quit()
display.stop()