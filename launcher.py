import minecraft_launcher_lib
import sys
import pickle
import os
import subprocess

class Launcher():
    def __init__(self):
        self.CLIENT_ID = "9ff1e48d-5b3c-42bb-883f-fd0426a583c4"
        self.SECRET = "7Hw8Q~1pfZRlrL2Pfo9QEF~cZahZw5pxhRDv0b0G"
        self.REDIRECT_URL = "http://localhost/"
        self.minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        self.login_data = None
        self.logged_in = False
        
    def login(self):
        if self.check_login == False:
            print(f"Open {minecraft_launcher_lib.microsoft_account.get_login_url(self.CLIENT_ID, self.REDIRECT_URL) } in your Browser, login and paste the url you are redirected to here: ")
            code_url = input()
            
            if not minecraft_launcher_lib.microsoft_account.url_contains_auth_code(code_url):
                print("Url invalid")
                sys.exit(1)
                
            auth_code = minecraft_launcher_lib.microsoft_account.get_auth_code_from_url(code_url)
            login_data = minecraft_launcher_lib.microsoft_account.complete_login(self.CLIENT_ID, self.SECRET, self.REDIRECT_URL, auth_code)
            with open("login.pkl", "wb") as f:
                pickle.dump(login_data, f)
            print("Login sucessful")
            self.logged_in = True
    
    def refresh_login(self):
        try:
            with open("login.pkl", "rb") as f:
                self.login_data = pickle.load(f)
            minecraft_launcher_lib.microsoft_account.complete_refresh(self.CLIENT_ID, self.SECRET, self.REDIRECT_URL, self.login_data["refresh_token"])
            print("Logged in as {}".format(self.login_data["name"]))
            self.logged_in = True
        except FileNotFoundError:
            print("No login data detected. Please login from the launcher")
        except KeyError:
            self.logged_in = False
            
    def check_login(self):
        if self.logged_in and self.login_data != None:
            return True
        else:
            return False
        
    def get_login_data(self):
        if self.check_login():
            return self.login_data
        else:
            return False
        
    def load_all_installed_versions(self):
        versions = []
        for version in minecraft_launcher_lib.utils.get_installed_versions(self.minecraft_directory):
            versions.append(version["id"])
        return versions

    def load_all_profiles(self):
        profiles = []
        for object in os.scandir("./profiles"):
            if object.is_dir():
                with open(f"./profiles/{object.name}/profile.pkl", "rb") as f:
                    profile = pickle.load(f)
                    profiles.append(profile)
        return profiles
    
    def load_all_profiles_by_name(self):
        profiles = []
        for object in os.scandir("./profiles"):
            if object.is_dir():
                with open(f"./profiles/{object.name}/profile.pkl", "rb") as f:
                    profile = pickle.load(f)
                    profiles.append(profile["id"])
        return profiles
    
    def create_new_profile(self, name, version, args):
        os.mkdir(f"./profiles/{name}")
        profile = {
            "id": name,
            "version": version,
            "args": args
        }
        with open(f"./profiles/{name}/profile.pkl", "wb") as f:
            pickle.dump(profile, f)
            
    def launch_profile(self, id):
        for profile in self.load_all_profiles():
            if id == profile["id"]:
                minecraft_launch_options = {
                    "username": self.login_data["name"],
                    "uuid": self.login_data["id"],
                    "token": self.login_data["access_token"],
                    "jvmArguments": profile["args"],
                    "executablePath": "C:/Program Files/Java/jdk-17.0.2/bin/javaw.exe"
                }
                minecraft_launch_command = minecraft_launcher_lib.command.get_minecraft_command(
                    "1.8.9", 
                    self.minecraft_directory, 
                    minecraft_launch_options
                )
                minecraft_launcher_lib.microsoft_account.complete_refresh(self.CLIENT_ID, self.SECRET, self.REDIRECT_URL, self.login_data["refresh_token"])
                print("Refreshed Login. Starting Version {}".format(profile["version"]))
                subprocess.call(minecraft_launch_command)
