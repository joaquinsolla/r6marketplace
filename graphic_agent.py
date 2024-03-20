import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

def item_sales_to_plot_by_id(my_item_id):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_directory, 'assets', 'data.json')
    with open(data_path, 'r') as f:
        json_data = json.load(f)

    if my_item_id in json_data:
        sales_history = json_data[my_item_id]["sales_history"][-1000:]
        item = json_data[my_item_id]["id-name"]

        if len(sales_history) > 0:
            prices = [sale[0] for sale in sales_history]
            num_sales = len(sales_history)
            sale_indices = range(1, num_sales + 1)

            timestamps = [datetime.fromtimestamp(sale[1]) for sale in sales_history]
            min_date = min(timestamps).strftime('%d/%m/%Y')
            max_date = max(timestamps).strftime('%d/%m/%Y')

            plt.figure(figsize=(12, 6))
            plt.plot(sale_indices, prices, linestyle='-')
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

            plot_name = item.lstrip("- ")

            plt.savefig(os.path.join(current_directory, 'website', 'plots', f"{plot_name}.jpg"))
            plt.close()
            print(" + Plot saved:\t" + f"{plot_name}.jpg")

            plot_path = os.path.join(current_directory, 'website', 'plots', plot_name + '.jpg')
            return plot_path
        else:
            print("[!] Cannot build plot: Item " + item + " has no sales")
            return "No data"
    else:
        plt.figure(figsize=(12, 6))
        plt.title("No data")
        plt.ylabel('Price')
        plt.xlabel('This plot will be generated when the item is sold again')
        plt.savefig(os.path.join('website', 'plots', f"no-data.jpg"))
        plt.close()
        print("[!] This plot will be generated when the item is sold again: " + str(item_id))
        return f"website/plots/no-data.jpg"

def item_sales_to_plot(item_data):

    sales_history = item_data["sales_history"][-1000:]
    item = item_data["id-name"]

    if len(sales_history) > 0:
        prices = [sale[0] for sale in sales_history]
        num_sales = len(sales_history)
        sale_indices = range(1, num_sales + 1)

        timestamps = [datetime.fromtimestamp(sale[1]) for sale in sales_history]
        min_date = min(timestamps).strftime('%d/%m/%Y')
        max_date = max(timestamps).strftime('%d/%m/%Y')

        plt.figure(figsize=(12, 6))
        plt.plot(sale_indices, prices, linestyle='-')
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

        plot_name = item.lstrip("- ")

        current_directory = os.path.dirname(os.path.abspath(__file__))
        plt.savefig(os.path.join(current_directory, 'website', 'plots', f"{plot_name}.jpg"))
        plt.close()
        print(" + Plot saved:\t" + f"{plot_name}.jpg")

        plot_path = os.path.join(current_directory, 'website', 'plots', plot_name + '.jpg')
        return plot_path
    else:
        print("[!] Cannot build plot: Item " + item + " has no sales")
        return "No data"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        item_id = sys.argv[1]
        item_sales_to_plot_by_id(item_id)
    else:
        print("[X] Argument 'item_id' is needed!")
