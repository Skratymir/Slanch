import launcher
import tkinter
from tkinter import font as tkFont

class Window(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Slanch")
        self.geometry(
            str(round(self.winfo_screenwidth() / 3)) + 
            "x" + 
            str(round(self.winfo_screenheight() / 3)) + 
            "+" +
            str(round(self.winfo_screenwidth() / 2 - self.winfo_screenwidth() / 6)) + 
            "+" +
            str(round(self.winfo_screenheight() / 2 - self.winfo_screenheight() / 6))
            )
        # Set up container to hold pages
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # Load pages into self.frames
        self.frames = {}
        
        self.frames["LaunchPage"] = LaunchPage(parent=container, controller=self)
        self.frames["ProfilesPage"] = ProfilesPage(parent=container, controller=self)
        self.frames["SettingsPage"] = SettingsPage(parent=container, controller=self)
        self.frames["ProfileCreationPage"] = ProfileCreationPage(parent=container, controller=self)
        
        self.frames["LaunchPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["ProfilesPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["SettingsPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["ProfileCreationPage"].grid(row=0, column=0, sticky="nsew")
        
        self.set_page("LaunchPage")
        self.update()
        self.frames["ProfilesPage"].create_frame()
        self.frames["ProfileCreationPage"].resize_font(0)
        
        
    def set_page(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
class LaunchPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        
        self.launch_page_button = tkinter.Button(self)
        self.profiles_page_button = tkinter.Button(self, command=lambda: controller.set_page("ProfilesPage"))
        self.settings_page_button = tkinter.Button(self, command=lambda: controller.set_page("SettingsPage"))
        
        self.launch_page_button.place(relx=0.165, rely=0, relwidth=0.33, relheight=0.15, anchor="n")
        self.profiles_page_button.place(relx=0.5, rely=0, relwidth=0.33, relheight=0.15, anchor="n")
        self.settings_page_button.place(relx=0.83, rely=0, relwidth=0.33, relheight=0.15, anchor="n")
        
        self.launch_button = tkinter.Button(self, text="Launch", command=lambda: launcher.launch_profile(self.variable.get()))
        
        options = launcher.load_all_profiles_by_name()
        self.variable = tkinter.StringVar(self)
        self.variable.set(options[0])
        self.profile_selection = tkinter.OptionMenu(self, self.variable, *options)
        
        self.launch_button.place(relx=0.5, rely=0.5, relwidth=0.3, relheight=0.3, anchor="center")
        self.profile_selection.place(relx=0.5, rely=0.7, relwidth=0.3, relheight=0.2, anchor="n")
        
class ProfilesPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        
        self.launch_page_button = tkinter.Button(self, command=lambda: controller.set_page("LaunchPage"))
        self.profiles_page_button = tkinter.Button(self)
        self.settings_page_button = tkinter.Button(self, command=lambda: controller.set_page("SettingsPage"))
        
        self.launch_page_button.place(relx=0.165, rely=0, relwidth=0.33, relheight=0.15, anchor="n")
        self.profiles_page_button.place(relx=0.5, rely=0, relwidth=0.33, relheight=0.15, anchor="n")
        self.settings_page_button.place(relx=0.83, rely=0, relwidth=0.33, relheight=0.15, anchor="n")
        
        self.profiles_canvas = tkinter.Canvas(self)
        self.profiles_frame = tkinter.Frame(self.profiles_canvas)
        self.profiles_scrollbar = tkinter.Scrollbar(self, orient="vertical", command=self.profiles_canvas.yview)
        
        self.profiles_frame.bind(
            "<Configure>",
            lambda e: self.profiles_canvas.configure(
                scrollregion=self.profiles_canvas.bbox("all")
            )
        )
        
        self.profiles_canvas.configure(yscrollcommand=(self.profiles_scrollbar.set))
        
        self.profiles = launcher.load_all_profiles()
        
        for profile in self.profiles:
            frame = tkinter.Frame(self.profiles_frame)
            tkinter.Label(frame, text=profile["id"], anchor="w").pack(side="left")
            tkinter.Button(frame, text="delete", anchor="w").pack(side="right")
            tkinter.Button(frame, text="edit", anchor="e").pack(side="right")
            frame.pack(side="bottom", anchor="w", fill="both", expand=True)
        frame = tkinter.Frame(self.profiles_frame)
        tkinter.Button(frame, text="Create new Profile", command=lambda: controller.set_page("ProfileCreationPage")).pack()
        frame.pack(side="bottom", anchor="w", fill="both", expand=True)
        
        self.profiles_canvas.place(relx=0.05, rely=0.2, relwidth=0.915, relheight=0.8, anchor="nw")
        self.profiles_scrollbar.place(relx=1, rely=0.2, relheight=0.8, relwidth=0.035, anchor="ne")
        
    def create_frame(self):
        self.profiles_canvas.create_window((0, 0), window=self.profiles_frame, anchor="nw", width=self.profiles_canvas.winfo_width())     
        
class SettingsPage(tkinter.Frame):
    def __init__(self, parent, controller):
        global login_button
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        
        launch_page_button = tkinter.Button(self, command=lambda: controller.set_page("LaunchPage"))
        profiles_page_button = tkinter.Button(self, command=lambda: controller.set_page("ProfilesPage"))
        settings_page_button = tkinter.Button(self)
        
        launch_page_button.place(relx=0.165, rely=0, relwidth=0.33, relheight=0.15, anchor="n")
        profiles_page_button.place(relx=0.5, rely=0, relwidth=0.33, relheight=0.15, anchor="n")
        settings_page_button.place(relx=0.83, rely=0, relwidth=0.33, relheight=0.15, anchor="n")
        
        self.login_button = tkinter.Button(self, text="Login", command=lambda: self.login_out())
        
        self.login_button.place(relx=0.5, rely=0.2, relwidth=0.3, relheight=0.15, anchor="n")
        
    def login_out(self):
        if launcher.check_login():
            launcher.logout()
        else:
            launcher.login()
        update_login_button()
            
class ProfileCreationPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        
        self.font = ("Times new Roman", 12)
        
        all_installed_versions = launcher.load_all_installed_versions()
        self.selected_version = tkinter.StringVar(self)
        self.selected_version.set(all_installed_versions[0])
        default_java_args = "-Xmx2G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M"
        
        self.title_label = tkinter.Label(self, text="Create Profile")
        self.profile_name_label = tkinter.Label(self, text="Profile name")
        self.profile_version_label = tkinter.Label(self, text="Version")
        self.profile_args_label = tkinter.Label(self, text="Java arguments")
        self.profile_name_input = tkinter.Entry(self)
        self.profile_version_dropdown = tkinter.OptionMenu(self, self.selected_version, *all_installed_versions)
        self.profile_args_input = tkinter.Entry(self)
        self.profile_args_input.insert(-1, default_java_args)
        self.profile_creation_button = tkinter.Button(self, text="Create", command=self.launcher_create_profile)
        
        self.title_label.place(relx=0.5, rely=0, relwidth=1, relheight=0.2, anchor="n")
        self.profile_name_label.place(relx=0.1, rely=0.25, relwidth=0.3, relheight=0.2, anchor="nw")
        self.profile_name_input.place(relx=0.5, rely=0.3, relwidth=0.4, relheight=0.1, anchor="nw")
        self.profile_version_label.place(relx=0.1, rely=0.45, relwidth=0.3, relheight=0.2, anchor="nw")
        self.profile_version_dropdown.place(relx=0.5, rely=0.5, relwidth=0.4, relheight=0.1, anchor="nw")
        self.profile_args_label.place(relx=0.1, rely=0.65, relwidth=0.3, relheight=0.2, anchor="nw")
        self.profile_args_input.place(relx=0.5, rely=0.7, relwidth=0.4, relheight=0.1, anchor="nw")
        self.profile_creation_button.place(relx=0.5, rely=0.85, relwidth=0.5, relheight=0.1, anchor="n")
        
    def resize_font(self, event):
        self.title_label["font"] = tkFont.Font(size=round(self.title_label.winfo_height() - self.title_label.winfo_height() / 3))
        self.profile_name_label["font"] = tkFont.Font(size=round(self.title_label.winfo_height() - self.title_label.winfo_height() / 1.35))
        self.profile_version_label["font"] = tkFont.Font(size=round(self.title_label.winfo_height() - self.title_label.winfo_height() / 1.35))
        self.profile_args_label["font"] = tkFont.Font(size=round(self.title_label.winfo_height() - self.title_label.winfo_height() / 1.35))
        
    def launcher_create_profile(self):
        name = self.profile_name_input.get()
        version = self.selected_version.get()
        args = []
        for argument in self.profile_args_input.get().split(" "):
            args.append(argument)
            
        launcher.create_new_profile(name, version, args)
        self.controller.set_page("LaunchPage")
            
def update_login_button():
    if launcher.check_login() == True:
        window.frames["SettingsPage"].login_button["text"] = "Logout"
    else:
        window.frames["SettingsPage"].login_button["text"] = "Login"

if __name__ == "__main__":
    window = Window()
    launcher.refresh_login()
    update_login_button()
    window.resizable(False, False)
    window.mainloop()
