import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

def item_sales_to_plot(my_item_id):
    with open('assets/data.json', 'r') as f:
        json_data = json.load(f)

    sales_history = json_data[my_item_id]["sales_history"][-50:]
    item = json_data[my_item_id]["id-name"]

    if len(sales_history) > 0:
        prices = [sale[0] for sale in sales_history]
        num_sales = len(sales_history)
        sale_indices = range(1, num_sales + 1)

        timestamps = [datetime.fromtimestamp(sale[1]) for sale in sales_history]
        min_date = min(timestamps).strftime('%d/%m/%Y')
        max_date = max(timestamps).strftime('%d/%m/%Y')

        plt.figure(figsize=(10, 6))
        plt.plot(sale_indices, prices, marker='o', linestyle='-')
        plt.title(item.upper())
        plt.ylabel('Price')
        plt.xlabel(f'Last {len(sales_history)} sales\n{min_date} to {max_date}')

        max_price = max(prices)
        min_price = min(prices)
        plt.axhline(y=max_price, color='r', linestyle='--', label=f'Max Price: {max_price}')
        plt.axhline(y=min_price, color='g', linestyle='--', label=f'Min Price: {min_price}')
        plt.legend()

        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join('assets', 'plots', f"{item}.jpg"))
        print("[ Plot saved: " + f"{item}.jpg" + " ]")
    else:
        print("[!] Cannot build plot: Item " + item + " has no sales")

item_id = "2f4918b3-cd1e-4a3c-b08e-27b300b0e3c1"
item_sales_to_plot(item_id)