# R6 Marketplace Bot
Scan the marketplace, analyze items' hidden data in an HTML view and get emails with discounted prices.

## Setup

### Prequisites
- [python](https://www.python.org/)
- [pip](https://pypi.org/project/pip/)
  
First, clone the repo and add the 'data.json', 'discounts.json' and 'old_discounts.json' files to '/assets', and leave the contents as ```{}```.

Next, add an 'ids.json' file to '/assets', and place any items and their item IDs in the contents. There is a starting example with the most relevant items.

Also create empty 'assets/index.html' and 'assets/log.txt' files.

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
My settings: 202 items to check every 10 minutes.

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
Execute the file 'manual_agent.py' by passing the item's id as an argument (do not use brackets ""). It also works with items that do not appear in 'assets/data.json' o 'assets/ids.json'.Example:
```sh
python ./manual_agent.py f619eb19-de6e-4dcd-96eb-08b45f80fe64
```

### Generate HTML file from data.json
```sh
python ./html_agent.py
```
Once generated, open the file 'assets/index.html' with your Internet browser.

### Get plot of an item's sales as a picture
Execute the file 'graphic_agent.py' by passing the item's id as an argument (do not use brackets ""). Note that it only works with items that have sales registered in 'assets/data.json'. Example:
```sh
python ./graphic_agent.py aee4bdf2-0b54-4c6d-af93-9fe4848e1f76
```

### Send an email manually with last scanned data
```sh
python ./email_agent.py
```

## Credit
Part of the code of this project (specially the Auth code) was sourced from https://github.com/hiibolt/r6econ and https://github.com/CNDRD/siegeapi. Special thanks to their developers.