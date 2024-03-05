from __future__ import annotations
import asyncio
import contextlib
import json
import sys
import time
import warnings
from os.path import exists
from auth import Auth
from email_agent import send_email
from datetime import datetime


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

        print("[ Wrote to log ]")

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
                        "id-name": key.split(' ', 1)[1] if ' ' in key else key,
                        "type": res[1],
                        "url": "https://www.ubisoft.com/es-es/game/rainbow-six/siege/marketplace?route=buy%2Fitem-details&itemId="+item_id,
                        "asset-url": res[10],
                        "data": None,
                        "sales_history": [],
                        "updated": time.time()
                    }

                # if in need to reset names
                # data[item_id]["id-name"] = key.split(' ', 1)[1] if ' ' in key else key

                if data[item_id]["data"] is None or data[item_id]["data"] != {
                    "sellers": res[8],
                    "buyers": res[5],
                    "lowest-seller": res[6],
                    "highest-seller": res[7],
                    "lowest-buyer": res[3],
                    "highest-buyer": res[4],
                    "last-sold": res[9]
                }:
                    data[item_id]["data"] = {
                        "sellers": res[8],
                        "buyers": res[5],
                        "lowest-seller": res[6],
                        "highest-seller": res[7],
                        "lowest-buyer": res[3],
                        "highest-buyer": res[4],
                        "last-sold": res[9]
                    }
                    data[item_id]["updated"] = time.time()
                    print(" + New DATA: \t" + key)

                if len(data[item_id]["sales_history"]) == 0 or data[item_id]["sales_history"][len(data[item_id]["sales_history"]) - 1][0] != res[9]:
                    data[item_id]["sales_history"] = data[item_id]["sales_history"] + [[res[9], time.time()]]
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
        price = value.get('data', {}).get('lowest-seller')
        if price is not None:
            url = value.get('url')
            name = value.get('id-name')
            if not name.startswith("-") and not isinstance(price, str):
                if (price <= limit_premium and name.startswith("!")) or (price <= limit_high and name.startswith("*")) or (price <= limit_medium and name.startswith("^")) or (price <= limit_low and name.startswith("=")):
                    if url is not None and name is not None:
                        discounts[name] = {
                            "price": price,
                            "url": url,
                            "updated": time.time()
                        }
                    else:
                        print("[X] Url or Name is None")
        else:
            print("[X] Price is None")

    if len(discounts) == 0:
        print(" - No discounts")
    else:
        for key, value in discounts.items():
            price = value.get('price')
            url = value.get('url')
            aligned_name = (str(key) + ":").ljust(40)
            print(str(aligned_name) + "\t" + str(price) + " - " + str(url))

# Initial settings
#sys.stdout = open('output.txt', 'w')
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize vars
limit_premium = 2600
limit_high = 1100
limit_medium = 750
limit_low = 500
data, item_ids = check_files()
discounts = {}

# Execution
asyncio.get_event_loop().run_until_complete(scan_market())
save_to_json(data, "assets/data.json")
check_for_discounts()
save_to_json(discounts, "assets/discounts.json")
email_sent = send_email()
write_to_log()