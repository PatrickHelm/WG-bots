# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
import smtplib
import os

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def submit_app(ref):
    try:
        link = "https://www.wg-gesucht.de/" + ref
        msg = MIMEMultipart()
        email = os.environ["EMAIL"]
        msg["Subject"] = "Neue Wohnungsanzeige kontaktiert!"
        msg["From"] = email
        msg["To"] = email
        sent = "https://www.wg-gesucht.de/nachrichten.html?filter_type=7"
        msg.attach(MIMEText(f"Contacting: {link} \n\n See message here: {sent}"))

        mailserver = smtplib.SMTP("smtp.gmail.com", 587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(email, os.environ["EMAIL_PW"])
        mailserver.sendmail(email, [email], msg.as_string())
        mailserver.quit()
    except:
        print("Email not sent")

    # change the location of the driver on your machine
    # create ChromeOptions object
    chrome_options = webdriver.ChromeOptions()

    # add the argument to reuse an existing tab
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--reuse-tab")
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--disable-dev-shm-usage')

    # create the ChromeDriver object
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get("https://www.wg-gesucht.de/nachricht-senden/" + ref)
    except WebDriverException:
        print("Error loading page")
        driver.quit()
        time.sleep(60)
        return
    try:
        driver.implicitly_wait(10)
        accept_button = driver.find_elements(
            "xpath", "//*[contains(text(), 'Accept all')]"
        )[0]
        accept_button.click()
        konto_button = driver.find_elements(
            "xpath", "//*[contains(text(), 'Bitte loggen Sie sich hier ein')]"
        )[0]
        konto_button.click()
        driver.implicitly_wait(5)
        email = driver.find_element("id", "login_email_username")
        email.send_keys(os.environ["EMAIL"])
        driver.implicitly_wait(5)
        passwd = driver.find_element("id", "login_password")
        passwd.send_keys(os.environ["WG_PW"])
        driver.implicitly_wait(5)
        login_button1 = driver.find_element("id", "login_submit")
        driver.implicitly_wait(5)
        login_button1.click()
        driver.implicitly_wait(5)
    except:
        print("Login could not be performed")
        driver.quit()
        return
    try:
        se_button1 = driver.find_element("id", "sicherheit_bestaetigung")
        se_button1.click()
    except:
        print("No sicherheit check")
    try:
        timestamp = driver.find_element("id", "message_timestamp")
        print("Timestamp = ", timestamp)
        print("Message has been sent. Will skip")
        driver.quit()
    except:
        print("No message has been sent. Will send now...")
    try:
        text_area = driver.find_element("id", "message_input")
        text_area.clear()
        name = driver.find_elements("xpath", "//*[contains(text(), 'Nachricht an')]")[
            0
        ].text[13:]
    except:
        print("No text area found")
        driver.quit()
        return
    # read your message from a file
    try:
        message_file = open("./message.txt", "r", encoding="utf-8")
        message = message_file.read().replace("NAME", name)
        print(message)
        text_area.send_keys(message)
        message_file.close()
    except:
        print("message.txt file not found!")
        driver.quit()
        return
    time.sleep(2)
    try:
        anhang_button = driver.find_elements(
            "xpath", "//button[@data-target='#attachment_options_modal']"
        )[0]
        anhang_button.click()
        driver.implicitly_wait(5)
        gesuch_button = driver.find_elements(
            "xpath", "//*[contains(text(), 'Link zu meinem')]"
        )[0]
        gesuch_button.click()
        time.sleep(2)
        select_gesuch = driver.find_elements(value="my_requests")[0].find_elements(
            "xpath", "//input[@type='checkbox']"
        )[0]
        select_gesuch.click()
        driver.implicitly_wait(5)
        confirm_button = driver.find_elements(
            "xpath", "//*[contains(text(), 'Bestätigen')]"
        )[0]
        confirm_button.click()
    except:
        print("No Gesuch attached")

    # driver.implicitly_wait(10)
    time.sleep(2)  # may not be required
    try:
        submit_button = driver.find_element(
            "xpath",
            "//button[@data-ng-click='submit()' or contains(.,'Nachricht senden')]",
        )
        submit_button.click()
    except NoSuchElementException:
        print("Cannot find submit button!")
        driver.quit()
    driver.quit()
