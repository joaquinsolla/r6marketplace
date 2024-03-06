import asyncio
import contextlib
from auth import Auth


async def manual_check(item):
    with (contextlib.suppress(Exception)):

        creds = []
        with open('assets/credentials/ubi_credentials.txt', 'r') as credentials:
            for line in credentials:
                creds.append(line.strip())

        auth = Auth(creds[0], creds[1])
        print("[ Authenticated ]")

        try:
            auth.item_id = item
            res = await auth.try_query_db()
            if not res:
                print("[!] Rate Limited")

            json_item = {
                "url": "https://www.ubisoft.com/es-es/game/rainbow-six/siege/marketplace?route=buy%2Fitem-details&itemId=" + item,
                "data": {
                    "sellers": res[8],
                    "buyers": res[5],
                    "lowest-seller": res[6],
                    "highest-seller": res[7],
                    "lowest-buyer": res[3],
                    "highest-buyer": res[4],
                    "last-sold": res[9],
                    "roi": int(float(res[6]) / 0.9) if not isinstance(res[6], str) else "No data"
                }
            }

            print(" + Manual Item:" + str(item) +"\n"+
                "\tROI: " + str(json_item.get("data").get("roi")) + "\n"
                "\tLowest seller: " + str(json_item.get("data").get("lowest-seller")) + "\n"
                "\tHighest seller: " + str(json_item.get("data").get("highest-seller")) + "\n"
                "\tLowest buyer: " + str(json_item.get("data").get("lowest-buyer")) + "\n"
                "\tHighest buyer: " + str(json_item.get("data").get("highest-buyer")) + "\n"
                "\tSellers: " + str(json_item.get("data").get("sellers")) + "\n"
                "\tBuyers: " + str(json_item.get("data").get("buyers")) + "\n"
                "\tLast sold: " + str(json_item.get("data").get("last-sold")) + "\n"
                "\tURL: " + str(json_item.get("url")))

        finally:
            await auth.close()
            print("[ Session Closed ]")

item_id = "b550ea3c-4518-4f0e-b906-bcaa8d491cf6"
asyncio.get_event_loop().run_until_complete(manual_check(item_id))
