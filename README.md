# R6 Marketplace Bot
Scan the marketplace and get emails with discounted skins.

## Setup

### Prequisites
- [python](https://www.python.org/)
- [pip](https://pypi.org/project/pip/)
  
First, clone the repo and add the 'data.json', 'discounts.json' and 'old_discounts.json' files to /assets, and leave the contents as ```{}```.

Next, add an 'ids.json' file to /assets, and place any items and their item IDs in the contents. There is a starting example with the most relevant items.

Then, create the folder /credentials inside /assets. Inside /assets/credentials you will create 3 files:
- 'bot_credentials.txt'
  - Line 1: The bot email (ex. r6bot@gmail.com)
  - Line 2: The bot app-key (you will have to create one in your Google Account settings)
- 'ubi_credentials.txt'
  - Line 1: Your Ubisoft account email
  - Line 2: Your Ubisoft account password
- 'email_subscribers.txt'
  - One email per line

## Run
Install dependencies
```sh
pip install -r requirements.txt
```
Run the main file
```sh
python ./main.py
```

## Credit
Part of the code of this project (specially the Auth code) was sourced from https://github.com/hiibolt/r6econ and https://github.com/CNDRD/siegeapi. Special thanks to their developers.