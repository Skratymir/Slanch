import os, shutil, sys
import pyAesCrypt
import string
import random
import io
import subprocess

def yes_no(text: str) -> bool:
    if "-y" in sys.argv:
        return True
    yes = ["yes", "ye", "y", ""]
    no = ["no", "n"]
    while True:
        choice = input(f"{text} (y/n) ")
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            continue

if not yes_no("This programm will now begin the building process. \nDo you wish to continue?"):
    quit()
client_id = input("Please enter your Client ID:\n")
secret = input("Please enter your Client Secret:\n")

if os.path.exists("./dist"):
    if not yes_no('The building process will delete all contents of the "dist" folder. \nDo you wish to continue?'):
        quit()
    shutil.rmtree("./dist")
subprocess.call([".venv\Scripts\pyinstaller.exe", "Slanch.spec", "-y"])
os.mkdir("dist/Slanch/data/")

with open("dist/Slanch/data/key.key", "w") as key_file:
    chars = string.printable
    key = "".join(random.choice(chars) for i in range(256))
    key_file.write(key)

with open("dist/Slanch/data/key.key", "r") as key:
    with open("dist/Slanch/data/secret.json", "wb") as fOut:
        secret_data = bytes('{\n    "Client ID": "' + client_id + '",\n    "Secret": "' + secret + '"\n}', encoding="utf-8")
        fIn = io.BytesIO(secret_data)
        pyAesCrypt.encryptStream(fIn, fOut, key.read(), 64 * 1024)

shutil.copyfile("logged_in.html", "dist/Slanch/logged_in.html")

print("\n\nBuilding process complete!")
