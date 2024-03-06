from __future__ import annotations
import asyncio
import contextlib
import json
import time
import warnings
from os.path import exists
from auth import Auth
from email_agent import send_email
from datetime import datetime

from html_agent import data_to_html


def check_files():
    if not exists("assets/data.json"):
        with open('assets/data.json', 'w') as f:
            f.write("{}")

    if not exists("assets/ids.json"):
        with open('assets/ids.json', 'w') as f:
            f.write('{"black ice r4-c": "aee4bdf2-0b54-4c6d-af93-9fe4848e1f76"}')

    data_file = open("assets/data.json", "r")
    old_data = json.loads(data_file.read())
    data_file.close()

    item_id_file = open("assets/ids.json", "r")
    old_item_ids = json.loads(item_id_file.read())
    item_id_file.close()

    print("[ Files Checked ]")
    return old_data, old_item_ids

def save_to_json(source, target_url):
    with contextlib.suppress(Exception):

        data_file = open(target_url, "w")
        data_file.write(json.dumps(source, indent=2))
        data_file.close()

        print("[ Saved: " + target_url + " ]")

def write_to_log():
    with contextlib.suppress(Exception):

        now = datetime.now()
        now_formatted = now.strftime('%d/%m/%Y %H:%M')
        if email_sent:
            now_formatted += " - Discounts: " + str(len(discounts))

        data_file = open('log.txt', "a")
        data_file.write("\n" + now_formatted)
        data_file.close()

        print("[ Log updated ]")

async def scan_market():
    with (contextlib.suppress(Exception)):

        creds = []
        with open('assets/credentials/ubi_credentials.txt', 'r') as credentials:
            for line in credentials:
                creds.append(line.strip())

        auth = Auth(creds[0], creds[1])
        print("[ Authenticated ]")

        try:
            for key, item_id in item_ids.items():
                auth.item_id = item_id
                res = await auth.try_query_db()
                if not res:
                    print("[!] Rate Limited")
                    continue

                try:
                    data[item_id]
                except:
                    data[item_id] = {
                        "id-name": key,
                        "type": res[1],
                        "url": "https://www.ubisoft.com/es-es/game/rainbow-six/siege/marketplace?route=buy%2Fitem-details&itemId="+item_id,
                        "asset-url": res[10],
                        "data": None,
                        "sales_history": [],
                        "updated": time.time()
                    }

                # if in need to reset names
                # data[item_id]["id-name"] = key
                # print("RESET: " + key)

                if data[item_id]["data"] is not None:
                    if len(data[item_id]["sales_history"]) == 0:
                        avg_price = "No data"
                    else:
                        sales_history = data[item_id]["sales_history"]
                        sales = [sale[0] for sale in sales_history]
                        avg_price = int(sum(sales) / len(sales))

                if data[item_id]["data"] is None or data[item_id]["data"] != {
                    "sellers": res[8],
                    "buyers": res[5],
                    "lowest-seller": res[6],
                    "highest-seller": res[7],
                    "lowest-buyer": res[3],
                    "highest-buyer": res[4],
                    "last-sold": res[9],
                    "roi": int(float(res[6]) / 0.9) if not isinstance(res[6], str) else "No data",
                    "avg-price": avg_price
                }:
                    data[item_id]["data"] = {
                        "sellers": res[8],
                        "buyers": res[5],
                        "lowest-seller": res[6],
                        "highest-seller": res[7],
                        "lowest-buyer": res[3],
                        "highest-buyer": res[4],
                        "last-sold": res[9],
                        "roi": int(float(res[6]) / 0.9) if not isinstance(res[6], str) else "No data",
                        "avg-price": avg_price
                    }
                    data[item_id]["updated"] = time.time()
                    print(" + New DATA: \t" + key)

                if len(data[item_id]["sales_history"]) == 0 or data[item_id]["sales_history"][len(data[item_id]["sales_history"]) - 1][0] != res[9]:
                    data[item_id]["sales_history"] = data[item_id]["sales_history"] + [[res[9], time.time()]]
                    sales = [sale[0] for sale in data[item_id]["sales_history"]]
                    avg_price = int(sum(sales) / len(sales))
                    data[item_id]["data"]["avg-price"] = avg_price
                    data[item_id]["updated"] = time.time()
                    print(" + New SALES: \t" + key)

        finally:
            await auth.close()
            print("[ Session Closed ]")

def check_for_discounts():

    print("[ Checking For Discounts ]")

    with open('assets/data.json', 'r') as file:
        updated_data = json.load(file)

    for key, value in updated_data.items():
        price = value.get('data').get('lowest-seller')
        if price is not None and not isinstance(price, str):
            name = value.get('id-name')
            avg_price = value.get('data').get('avg-price')
            discounted_percentage = int((1 - (price / avg_price)) * 100)
            roi = value.get('data').get('roi')
            sellers = value.get('data').get('sellers')
            buyers = value.get('data').get('buyers')
            highest_buyer = value.get('data').get('highest-buyer')

            sales_history = value.get('sales_history')
            prices = [sale[0] for sale in sales_history]
            last_sales = prices[-5:]
            last_sales_string = "Last sales: " + ", ".join(str(price) for price in last_sales)

            url = value.get('url')
            asset_url = value.get('asset-url')

            if not name.startswith("-"):
                if not isinstance(avg_price, str):
                    if price <= (avg_price*0.8):
                        if url is not None and name is not None:
                            discounts[name] = {
                                "price": price,
                                "avg-price": avg_price,
                                "discounted-percentage": discounted_percentage,
                                "roi": roi,
                                "sellers": sellers,
                                "buyers": buyers,
                                "highest-buyer": highest_buyer,
                                "last_sales_string": last_sales_string,
                                "url": url,
                                "asset-url": asset_url,
                                "updated": time.time()
                            }
                        else:
                            print("[X] Url or Name is None")
            else:
                print(" - Item in quarantine " + name)

    if len(discounts) == 0:
        print(" - No discounts")
    else:
        for key, value in discounts.items():
            url = value.get('url')
            aligned_name = (str(key) + ":").ljust(35)
            aligned_price = (str(value.get('price'))).ljust(6)
            aligned_avg = (str(value.get('avg-price'))).ljust(6)
            aligned_percentage = (str(value.get('discounted-percentage')) + "%").ljust(3)
            print(" + " + str(aligned_name) + "\t" + str(aligned_price) + " " + str(aligned_percentage) + "\t\tAVG: " + str(aligned_avg) + "\t\t" + str(url))

# Initial settings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize vars
data, item_ids = check_files()
discounts = {}

# Execution
asyncio.get_event_loop().run_until_complete(scan_market())
save_to_json(data, "assets/data.json")
data_to_html()
check_for_discounts()
save_to_json(discounts, "assets/discounts.json")
email_sent = send_email()
write_to_log()