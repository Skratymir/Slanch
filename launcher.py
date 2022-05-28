import minecraft_launcher_lib
import sys
import pickle
import os
import subprocess
import random
import string
import pyAesCrypt
import shutil
import http.server
import webbrowser
import socketserver

from threading import Thread

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
login_data = None
logged_in = False
global url

class GetURLHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global url
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        url = self.path
    
def login(CLIENT_ID, REDIRECT_URL, SECRET):
    global logged_in, login_data, url
    webbrowser.open(minecraft_launcher_lib.microsoft_account.get_login_url(CLIENT_ID, REDIRECT_URL))
    Handler = GetURLHandler
    httpd = socketserver.TCPServer(("", 8000), Handler)
    httpd.handle_request()
    code_url = url
    
    if not minecraft_launcher_lib.microsoft_account.url_contains_auth_code(code_url):
        print("Url invalid")
        sys.exit(1)
        
    auth_code = minecraft_launcher_lib.microsoft_account.get_auth_code_from_url(code_url)
    login_data = minecraft_launcher_lib.microsoft_account.complete_login(CLIENT_ID, SECRET, REDIRECT_URL, auth_code)
    with open("login.data", "wb") as f:
        pickle.dump(login_data, f)
    encrypt_login_data()
    print("Login sucessful")
    logged_in = True
    
def logout():
    global logged_in, login_data
    print("Logging out...")
    logged_in = False
    login_data = None
    decrypt_login_data()
    os.remove("login.data")

def refresh_login(CLIENT_ID, REDIRECT_URL, SECRET):
    global logged_in, login_data
    try:
        if os.path.exists("login.encrypted"):
            decrypt_login_data()
            with open("login.data", "rb") as f:
                login_data = pickle.load(f)
            encrypt_login_data()
            minecraft_launcher_lib.microsoft_account.complete_refresh(CLIENT_ID, SECRET, REDIRECT_URL, login_data["refresh_token"])
            print("Logged in as {}".format(login_data["name"]))
            logged_in = True
    except FileNotFoundError:
        print("No login data detected. Please login from the launcher")
    except KeyError:
        logged_in = False
        
def check_login():
    global logged_in, login_data
    if logged_in and login_data != None:
        return True
    else:
        return False
    
def get_login_data():
    if check_login():
        return login_data
    else:
        return False
    
def load_all_installed_versions():
    versions = []
    for version in minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory):
        versions.append(version["id"])
    return versions

def load_all_available_versions():
    versions = []
    for version in minecraft_launcher_lib.utils.get_available_versions(minecraft_directory):
        versions.append(version["id"])
    return versions

def load_all_release_versions():
    versions = []
    for version in minecraft_launcher_lib.utils.get_available_versions(minecraft_directory):
        if version["type"] == "release":
            versions.append(version["id"])
    return versions

def load_all_profiles():
    profiles = []
    for object in os.scandir("./profiles"):
        if object.is_dir():
            with open(f"./profiles/{object.name}/profile.info", "rb") as f:
                profile = pickle.load(f)
                profiles.append(profile)
    return profiles

def load_all_profiles_by_name():
    profiles = []
    for object in os.scandir("./profiles"):
        if object.is_dir():
            with open(f"./profiles/{object.name}/profile.info", "rb") as f:
                profile = pickle.load(f)
                profiles.append(profile["id"])
    return profiles

def create_new_profile(name, version, ram):
    os.mkdir(f"./profiles/{name}")
    os.mkdir(f"./profiles/{name}/backup/")
    profile = {
        "id": name,
        "version": version,
        "args": [f"-Xmx{ram}G"]
    }
    with open(f"./profiles/{name}/profile.info", "wb") as f:
        pickle.dump(profile, f)
        
def edit_profile(old_name, name, version, ram):
    os.rename(f"./profiles/{old_name}", f"./profiles/{name}")
    new_profile = {
        "id": name,
        "version": version,
        "args": [f"-Xmx{ram}G"]
    }
    with open(f"./profiles/{name}/profile.info", "wb") as f:
        pickle.dump(new_profile, f)
    
        
def delete_profile(id):
    shutil.rmtree(f"profiles/{id}")
        
def launch_profile(id):
    for profile in load_all_profiles():
        if id == profile["id"]:
            minecraft_launch_options = {
                "username": login_data["name"],
                "uuid": login_data["id"],
                "token": login_data["access_token"],
                "jvmArguments": profile["args"]
            }
            print(profile["args"])
            minecraft_launch_command = minecraft_launcher_lib.command.get_minecraft_command(
                profile["version"], 
                minecraft_directory, 
                minecraft_launch_options
            )
            Thread(target=launch_minecraft, args=(profile, minecraft_directory, minecraft_launch_command)).start()

def launch_minecraft(profile, minecraft_directory, minecraft_launch_command):
    global logged_in
    print("Verifying installation of version {}".format(profile["version"]))
    minecraft_launcher_lib.install.install_minecraft_version(profile["version"], minecraft_directory)
    print("Refreshing login")
    refresh_login()
    if logged_in == True:
        print("Refreshed Login. Starting Version {}".format(profile["version"]))
        copy_minecraft_files_from_profile(profile["id"])
        subprocess.call(minecraft_launch_command)
        restore_minecraft_options(profile["id"])
    else:
        print("Refresh unsucessful. Please login again from the settings page")

def copy_minecraft_files_from_profile(profile_id):
    print("Backing files up")
    options_files = []
    for item in os.listdir(minecraft_directory):
        if os.path.isfile(minecraft_directory + "\\" + item) and "options" in item:
            options_files.append(item)

    if os.path.exists(minecraft_directory + "\\mods\\"):
        if os.path.exists(f"./profiles/{profile_id}/backup/mods/"):
            shutil.rmtree(f"./profiles/{profile_id}/backup/mods/")
        shutil.copytree(minecraft_directory + "\\mods\\", f"./profiles/{profile_id}/backup/mods/")

    for item in os.listdir(f"./profiles/{profile_id}/"):
        if item in options_files:
            shutil.copyfile(minecraft_directory + "\\" + item, f"./profiles/{profile_id}/backup/{item}")
            shutil.copyfile(f"./profiles/{profile_id}/{item}", minecraft_directory + "\\" + item)

    if os.path.exists(f"./profiles/{profile_id}/mods/"):
        shutil.copytree(f"./profiles/{profile_id}/mods/", minecraft_directory + "\\mods\\")

def restore_minecraft_options(profile_id):
    print("Restoring files")
    for item in os.listdir(f"./profiles/{profile_id}/backup/"):
        if os.path.isfile(f"./profiles/{profile_id}/backup/{item}"):
            shutil.copyfile(f"./profiles/{profile_id}/backup/{item}", minecraft_directory + "\\" + item)
            os.remove(f"./profiles/{profile_id}/backup/{item}")
    if os.path.exists(f"./profiles/{profile_id}/backup/mods/"):
        shutil.rmtree(f"./profiles/{profile_id}/backup/mods/")
    
def encrypt_login_data():
    if not os.path.exists("key.key"):
        chars = string.printable
        key = "".join(random.choice(chars) for i in range(256))
        with open("key.key", "w") as key_file:
            key_file.write(key)
    with open("key.key", "r") as key_file:
        key = key_file.read()
    pyAesCrypt.encryptFile("login.data", "login.encrypted", key)
    os.remove("login.data")
    
def decrypt_login_data():
    try:
        with open("key.key", "r") as key_file:
            key = key_file.read()
        pyAesCrypt.decryptFile("login.encrypted", "login.data", key)
        os.remove("login.encrypted")
    except FileNotFoundError:
        print("Key file not found. Please log in again from the Settings Page")

def is_vanilla_version(version, all_versions):
    if version in all_versions:
        return True
    else:
        return False
