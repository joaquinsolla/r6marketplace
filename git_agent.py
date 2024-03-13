import subprocess
from datetime import datetime
import os

def upload_website():
    now = datetime.now()
    now_formatted = now.strftime('%d/%m/%Y %H:%M')

    current_directory = os.path.dirname(os.path.abspath(__file__))
    website_directory = os.path.join(current_directory, "website")
    os.chdir(website_directory)

    commands = [
        "git add .",
        f'git commit -m "Automatic commit - {now_formatted}"',
        "git push"
    ]

    for command in commands:
        subprocess.run(command, shell=True)

    print("[ Uploaded website ]")


if __name__ == "__main__":
    upload_website()
