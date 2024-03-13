# R6 Marketplace Bot
Scan the marketplace, analyze items' hidden data in an HTML view and get emails with discounted prices.

## Setup

### Prequisites
- [python](https://www.python.org/)
- [pip](https://pypi.org/project/pip/)
  
First, clone the repo and add the 'data.json', 'discounts.json' and 'old_discounts.json' files to '/assets', and leave the contents as ```{}```.

Next, add an 'ids.json' file to '/assets', and place any items and their item IDs in the contents. There is a starting example with the most relevant items.

Also create an empty 'assets/log.txt' file.

It is needed to create a 'website' folder, and 'website/plots' also. Inside 'website' you have to create an empty file called 'index.html'.

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
My recommended settings: Over 200 items to check every 10 minutes.

### Automatic website commits
By default, you have to comment the line 'upload_website()' in 'main.py'. If you want to enable the auto-commit feature you have to configure your own website repository (I recommend GitHub Pages) and link it with the 'website' folder.

## Main Execution
Install dependencies
```sh
pip install -r requirements.txt
```
Run the main file
```sh
python ./main.py
```

### Workflow
The main execution of the program follows these operations in order:
1. Files checking
2. Market scan
   1. Log in Ubisoft Services
   2. Retrieve the Marketplace data
   3. Build sales plots
   4. Log out
3. Save retrieved data to a JSON file
4. Build an HTML file to display the data
5. [Disabled] Upload the HTML file to its Git repository
6. Check for discounts
7. Save discounts data to a JSON file
8. Send an email with the discounts data (if needed)
9. Write log

## Additional features

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

### Commit website changes manually
```sh
python ./git_agent.py
```

## Credit
Part of the code of this project (specially the Auth code) was sourced from https://github.com/hiibolt/r6econ and https://github.com/CNDRD/siegeapi. Special thanks to their developers.