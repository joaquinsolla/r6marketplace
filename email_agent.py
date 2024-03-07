import contextlib
import json
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
    with open('assets/discounts.json', 'r') as file:
        discounts_data = json.load(file)

    valid, not_valid_message = discounts_valid()
    if valid:
        save_to_json(discounts_data, "assets/old_discounts.json")
        message = ''
        total_discounts = 0

        msg = MIMEMultipart()

        with open('assets/data.html', 'rb') as file:
            html_attachment = MIMEApplication(file.read(), _subtype='html')
            html_attachment.add_header('Content-Disposition', 'attachment', filename='data.html')
            msg.attach(html_attachment)

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
        subject = now_formatted + " - " + str(total_discounts) + " Discounts"
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
    with open('assets/discounts.json', 'r') as file:
        discounts_data = json.load(file)

    message = ''
    total_discounts = 0

    msg = MIMEMultipart()

    with open('assets/data.html', 'rb') as file:
        html_attachment = MIMEApplication(file.read(), _subtype='html')
        html_attachment.add_header('Content-Disposition', 'attachment', filename='data.html')
        msg.attach(html_attachment)

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

    now = datetime.now()
    now_formatted = now.strftime('%d/%m/%Y %H:%M')
    message += "Updated: " + now_formatted + "\n"
    message += "Email sent manually."

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
    subject = now_formatted + " - " + str(total_discounts) + " Discounts"
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