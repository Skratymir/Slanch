import minecraft_launcher_lib
import sys
import pickle

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