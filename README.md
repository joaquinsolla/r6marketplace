# R6 Marketplace Bot
Scan the marketplace, analyze items' hidden data in an HTML view and get emails with discounted prices.

## Setup

### Prequisites
- [python](https://www.python.org/)
- [pip](https://pypi.org/project/pip/)
  
First, clone the repo and add the 'data.json', 'discounts.json' and 'old_discounts.json' files to '/assets', and leave the contents as ```{}```.

Next, add an 'ids.json' file to '/assets', and place any items and their item IDs in the contents. There is a starting example with the most relevant items.

Also create empty 'assets/data.html' and 'assets/log.txt' files.

Create folder 'assets/plots' if it doesn't exist.

Then, create the folder '/assets/credentials', then you will create 3 files inside:
- 'bot_credentials.txt'
  - Line 1: The bot email (ex. r6bot@gmail.com)
  - Line 2: The bot app-key (you will have to create one in your Google Account settings)
- 'ubi_credentials.txt'
  - Line 1: Your Ubisoft account email
  - Line 2: Your Ubisoft account password
- 'email_subscribers.txt'
  - One email per line

### Recommended scan intervals: Every 10 minutes
If you check an excessive amount of items or scan the marketplace in very small periods of time, you can get rate limited.
My settings: 175 items to check every 10 minutes.

## Main Execution
Install dependencies
```sh
pip install -r requirements.txt
```
Run the main file
```sh
python ./main.py
```

## Secondary functions

### Quarantine items
If you want to scan some items but don't want them in the discounts email, add "- " at the beginning of their names at 'assets/ids.json'. Example:
```
"- penta '19 mpx": "809185fa-0e5e-471d-8447-d0043a16164a",
```
Be careful! If you forget the space after the hyphen the quarantine won't work.
If you want to receive those items in your emails again just remove the "- ".

### Check a specific item
Paste the item's id as the 'item_id' variable in the 'manual_agent.py' file. Example:
```
item_id = "f619eb19-de6e-4dcd-96eb-08b45f80fe64"
```
Then run the file:
```sh
python .\manual_agent.py
```

### Generate HTML file from data.json
```sh
python .\html_agent.py
```
Once generated, open the file 'assets/data.html' with your Internet browser.

### Get plot of an item's sales as a picture
Paste the item's id as the 'item_id' variable in the 'graphic_agent.py' file. Example:
```
item_id = "2f4918b3-cd1e-4a3c-b08e-27b300b0e3c1"
```
Then run the file:
```sh
python .\graphic_agent.py
```

## Credit
Part of the code of this project (specially the Auth code) was sourced from https://github.com/hiibolt/r6econ and https://github.com/CNDRD/siegeapi. Special thanks to their developers.