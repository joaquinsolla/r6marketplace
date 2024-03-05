import contextlib
import json
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

import requests


def save_to_json(source, target_url):
    with contextlib.suppress(Exception):

        data_file = open(target_url, "w")
        data_file.write(json.dumps(source, indent=2))
        data_file.close()

        print("[ Saved: " + target_url + " ]")

def discounts_valid():

    with open('assets/discounts.json', 'r') as file:
        new_discounts = json.load(file)

    if len(new_discounts) == 0:
        return False, "No discounts found"

    else:
        with open('assets/old_discounts.json', 'r') as file:
            old_discounts = json.load(file)

        if len(new_discounts) != len(old_discounts):
            return True, "Ok"

        else:
            for field in old_discounts:
                if "updated" in old_discounts[field]:
                    del old_discounts[field]["updated"]
            for field in new_discounts:
                if "updated" in new_discounts[field]:
                    del new_discounts[field]["updated"]
            return not old_discounts == new_discounts, "Same discounts as before"

def send_email():
    with open('assets/discounts.json', 'r') as file:
        discounts_data = json.load(file)

    valid, not_valid_message = discounts_valid()
    if valid:
        save_to_json(discounts_data, "assets/old_discounts.json")
        message = ''
        total_discounts = 0

        msg = MIMEMultipart()

        for key, value in discounts_data.items():
            price = value.get('price')
            url = value.get('url')
            minimum_profit = value.get('minimum-profit')
            asset_url = value.get('asset-url')
            total_discounts += 1
            message += (str(total_discounts) + ". " + str(key) + ":  " + str(price) + "\n" +
                        "Minimum profit: " + str(minimum_profit) + "\n" +
                        str(url) + "\n\n")

            response = requests.get(asset_url)
            image_data = response.content

            image_attachment = MIMEImage(image_data)
            image_attachment.add_header('Content-Disposition', 'attachment', filename=(key) + ".png")
            msg.attach(image_attachment)

        now = datetime.now()
        now_formatted = now.strftime('%d/%m/%Y %H:%M')
        message += "Updated: " + now_formatted

        creds = []
        with open('assets/credentials/bot_credentials.txt', 'r') as credentials:
            for line in credentials:
                creds.append(line.strip())

        subs = []
        with open('assets/credentials/email_subscribers.txt', 'r') as subscribers:
            for line in subscribers:
                subs.append(line.strip())

        email_address = creds[0]
        password = creds[1]
        recipient = subs[0]
        subject = 'Total Discounts: ' + str(total_discounts)
        body = message

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # TLS Port

        msg['From'] = email_address
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, password)

        server.sendmail(email_address, recipient, msg.as_string())

        server.quit()
        print('[ Email Sent ]')
        return True
    else:
        print('[!] Email not sent: ' + not_valid_message)
        return False
