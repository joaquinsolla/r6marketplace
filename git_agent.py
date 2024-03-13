import subprocess
from datetime import datetime

def upload_website():
    now = datetime.now()
    now_formatted = now.strftime('%d/%m/%Y %H:%M')

    commands = [
        "cd ./website",
        "git add .",
        f'git commit -m "Automatic commit - {now_formatted}"',
        "git push"
    ]

    for command in commands:
        subprocess.run(command, shell=True)

    print("[ Uploaded website ]")


if __name__ == "__main__":
    upload_website()
