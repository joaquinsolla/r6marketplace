import contextlib
import json
import os
import smtplib
from email.mime.application import MIMEApplication
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

    current_directory = os.path.dirname(os.path.abspath(__file__))
    discounts_path = os.path.join(current_directory, 'assets', 'discounts.json')
    with open(discounts_path, 'r') as file:
        new_discounts = json.load(file)

    if len(new_discounts) == 0:
        return False, "No discounts found"

    else:
        old_discounts_path = os.path.join(current_directory, 'assets', 'old_discounts.json')
        with open(old_discounts_path, 'r') as file:
            old_discounts = json.load(file)

        if len(new_discounts) != len(old_discounts):
            return True, "Ok"

        else:
            for field in old_discounts:
                del old_discounts[field]["roi"]
                del old_discounts[field]["sellers"]
                del old_discounts[field]["buyers"]
                del old_discounts[field]["last_sales_string"]
                del old_discounts[field]["url"]
                del old_discounts[field]["asset-url"]
                del old_discounts[field]["sales-plot-path"]
                del old_discounts[field]["updated"]
            for field in new_discounts:
                del new_discounts[field]["roi"]
                del new_discounts[field]["sellers"]
                del new_discounts[field]["buyers"]
                del new_discounts[field]["last_sales_string"]
                del new_discounts[field]["url"]
                del new_discounts[field]["asset-url"]
                del new_discounts[field]["sales-plot-path"]
                del new_discounts[field]["updated"]
            return not old_discounts == new_discounts, "Same discounts as before"

def send_email():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    discounts_path = os.path.join(current_directory, 'assets', 'discounts.json')
    with open(discounts_path, 'r') as file:
        discounts_data = json.load(file)

    valid, not_valid_message = discounts_valid()
    if valid:
        save_to_json(discounts_data, discounts_path)
        message = 'All Data: http://r6marketplace.duckdns.org:8080\n\n'
        total_discounts = 0

        msg = MIMEMultipart()

        for key, value in discounts_data.items():
            price = value.get('price')
            avg_price = value.get('avg-price')
            discounted_percentage = value.get('discounted-percentage')
            roi = value.get('roi')
            sellers = value.get('sellers')
            buyers = value.get('buyers')
            highest_buyer = value.get('highest-buyer')
            last_sales_string = value.get('last_sales_string')
            url = value.get('url')
            asset_url = value.get('asset-url')
            sales_plot_path = value.get('sales-plot-path')

            total_discounts += 1
            message += ("<b>" + str(total_discounts) + ". " + str(key).upper() + ": " + str(price) + " (" + str(discounted_percentage) + "%)</b>\n" +
                        "Avg price: " + str(avg_price) + "\n" +
                        "ROI: " + str(roi) + "\n" +
                        "Sellers: " + str(sellers) + "\n" +
                        "Buyers: " + str(buyers) + "\n" +
                        "Highest buyer: " + str(highest_buyer) + "\n" +
                        last_sales_string + "\n" +
                        str(url) + "\n\n")

            response = requests.get(asset_url)
            image_data = response.content

            image_attachment = MIMEImage(image_data)
            image_attachment.add_header('Content-Disposition', 'attachment', filename=key + ".png")
            msg.attach(image_attachment)

            with open(sales_plot_path, 'rb') as file:
                image_data = file.read()

            image_attachment = MIMEImage(image_data)
            image_attachment.add_header('Content-Disposition', 'attachment', filename=(key + " plot.png"))
            msg.attach(image_attachment)

        message = f'Total Discounts: <b>{str(total_discounts)}</b>\n' + message

        now = datetime.now()
        now_formatted = now.strftime('%d/%m/%Y %H:%M')
        message += "Updated: " + now_formatted

        creds = []
        bot_credentials_path = os.path.join(current_directory, 'assets', 'credentials', 'bot_credentials.txt')
        with open(bot_credentials_path, 'r') as credentials:
            for line in credentials:
                creds.append(line.strip())

        subs = []
        subscribers_path = os.path.join(current_directory, 'assets', 'credentials', 'email_subscribers.txt')
        with open(subscribers_path, 'r') as subscribers:
            for line in subscribers:
                subs.append(line.strip())

        email_address = creds[0]
        password = creds[1]
        recipient = subs[0]
        subject = "R6 Marketplace Data"
        body = message

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # TLS Port

        msg['From'] = email_address
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText('<html><body>' + body.replace('\n', '<br>') + '</body></html>', 'html'))

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

def send_manual_email():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    discounts_path = os.path.join(current_directory, 'assets', 'discounts.json')
    with open(discounts_path, 'r') as file:
        discounts_data = json.load(file)

    message = 'All Data: http://r6marketplace.duckdns.org:8080\n\n'
    total_discounts = 0

    msg = MIMEMultipart()

    for key, value in discounts_data.items():
        price = value.get('price')
        avg_price = value.get('avg-price')
        discounted_percentage = value.get('discounted-percentage')
        roi = value.get('roi')
        sellers = value.get('sellers')
        buyers = value.get('buyers')
        highest_buyer = value.get('highest-buyer')
        last_sales_string = value.get('last_sales_string')
        url = value.get('url')
        asset_url = value.get('asset-url')
        sales_plot_path = value.get('sales-plot-path')

        total_discounts += 1
        message += ("<b>" + str(total_discounts) + ". " + str(key).upper() + ": " + str(price) + " (" + str(discounted_percentage) + "%)</b>\n" +
                    "Avg price: " + str(avg_price) + "\n" +
                    "ROI: " + str(roi) + "\n" +
                    "Sellers: " + str(sellers) + "\n" +
                    "Buyers: " + str(buyers) + "\n" +
                    "Highest buyer: " + str(highest_buyer) + "\n" +
                    last_sales_string + ".\n" +
                    str(url) + "\n\n")

        response = requests.get(asset_url)
        image_data = response.content

        image_attachment = MIMEImage(image_data)
        image_attachment.add_header('Content-Disposition', 'attachment', filename=key + ".png")
        msg.attach(image_attachment)

        with open(sales_plot_path, 'rb') as file:
            image_data = file.read()

        image_attachment = MIMEImage(image_data)
        image_attachment.add_header('Content-Disposition', 'attachment', filename=(key + " plot.png"))
        msg.attach(image_attachment)

    message = f'Total Discounts: <b>{str(total_discounts)}</b>\n' + message

    now = datetime.now()
    now_formatted = now.strftime('%d/%m/%Y %H:%M')
    message += "Updated: " + now_formatted + "\n"
    message += "Email sent manually."

    creds = []
    bot_credentials_path = os.path.join(current_directory, 'assets', 'credentials', 'bot_credentials.txt')
    with open(bot_credentials_path, 'r') as credentials:
        for line in credentials:
            creds.append(line.strip())

    subs = []
    subscribers_path = os.path.join(current_directory, 'assets', 'credentials', 'email_subscribers.txt')
    with open(subscribers_path, 'r') as subscribers:
        for line in subscribers:
            subs.append(line.strip())

    email_address = creds[0]
    password = creds[1]
    recipient = subs[0]
    subject = "R6 Marketplace Data"
    body = message

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # TLS Port

    msg['From'] = email_address
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText('<html><body>' + body.replace('\n', '<br>') + '</body></html>', 'html'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_address, password)

    server.sendmail(email_address, recipient, msg.as_string())

    server.quit()
    print('[ Email Sent ]')

if __name__ == "__main__":
    send_manual_email()