# R6 Marketplace Bot
Scan the marketplace, analyze items' hidden data in an HTML view and get emails with discounted prices.<br>
Developed by: **_Joaquín Solla Vázquez_**

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
5. Check for discounts
6. Save discounts data to a JSON file
7. Send an email with the discounts data (if needed)
8. Write log

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

## Automation on Linux
This program was developed to run automatically and constantly on a Linux-based machine, like a Raspberry or similar, and host the website into an Apache server. To configure it on your Linux system you can follow these steps:

### Install Apache2 (if you didn't yet)
```sh
sudo apt install apache2
```

### Give permissions to the execution script
```sh
chmod 777 run_r6.sh
```
This script also copies the website files to the default Apache2 html folder, to automatically update your Apache2 webpage.

### Set up the CRON service

Open the edit view for the CRON service:
```sh
crontab -e
```

Add the line to run the program every 10 minutes every day (edit the field 'your_directory' to the directory where the cloned repository is located):
```
*/10 * * * * /your_directory/r6marketplace/run_r6.sh > /your_directory/r6marketplace/cron.log 2>&1
```

### Website visualization

Now the program will execute every 10 minutes automatically (obviously, the machine needs to be turned on). You can check your website locally in your browser at:
http://localhost:80

You can also visit the webpage from other device if you are connected to the same network by browsing the machine IP, I recommend to set up a static IP. Example: http://192.168.1.33:80

If you want to access the website from outside of this network, you have to set up port forwarding on your router (make sure your Internet provider did not set up CGNAT on your network).
You can also configure a DNS service (I recommend https://duckdns.org, it is free and easy to configure).

## Automation on Windows
You can also automate the program on Windows by using the Tasks Manager.

Press _Windows + R_ and insert the following line, then press _Enter_:
```
taskschd.msc
```

Then click on 'Create Task...'. Enter the name you want for the task.

Click on 'Triggers' and then on 'New'. Complete the following information:
```
Configuration: Once
Repeat every: 10 minutes
During: Undefined
Enabled
```

Click on 'Actions' and then on 'New'. Complete the following information (check your Python path if needed):
```
Action: Run a program
Program or script: C:\Users\YOUR_USER\AppData\Local\Programs\Python\Python310\pythonw.exe
Add arguments: main.py
Run into: C:\YOUR_PATH\r6marketplace
```
_I recommend using pythonw.exe instead of python.exe, so a terminal won't display when the program is running._

Then click 'Accept' and enable the task (if it is not enabled yet) by clicking on 'Enable'.

**NOTE:** The program was not intended to host the website on a Windows service, but you can also access to the website locally by browsing: [file:///C:/YOUR_PATH/r6marketplace/website/index.html](file:///C:/YOUR_PATH/r6marketplace/website/index.html)


## Credit
Part of the code of this project (specially the Auth code) was sourced from https://github.com/hiibolt/r6econ and https://github.com/CNDRD/siegeapi. Special thanks to their developers.