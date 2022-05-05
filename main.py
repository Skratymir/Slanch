import tkinter
import launcher
from threading import Thread

class Window(tkinter.Tk):
    def __init__(self, slanch):
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
        self.frames["SettingsPage"] = SettingsPage(parent=container, controller=self, slanch=slanch)
        
        self.frames["LaunchPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["ProfilesPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["SettingsPage"].grid(row=0, column=0, sticky="nsew")
        
        self.set_page("LaunchPage")
        
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
        
        self.launch_button = tkinter.Button(self, text="Launch")
        
        self.launch_button.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.3, relheight=0.3)
        
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
        
class SettingsPage(tkinter.Frame):
    def __init__(self, parent, controller, slanch):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        self.slanch = launcher.Launcher
        
        self.launch_page_button = tkinter.Button(self, command=lambda: controller.set_page("LaunchPage"))
        self.profiles_page_button = tkinter.Button(self, command=lambda: controller.set_page("ProfilesPage"))
        self.settings_page_button = tkinter.Button(self)
        
        self.launch_page_button.place(relx=0.165, rely=0, relwidth=0.33, relheight=0.15, anchor="n")
        self.profiles_page_button.place(relx=0.5, rely=0, relwidth=0.33, relheight=0.15, anchor="n")
        self.settings_page_button.place(relx=0.83, rely=0, relwidth=0.33, relheight=0.15, anchor="n")
        
        self.login_button = tkinter.Button(self, text="Login", command=lambda: slanch.login())
        
        self.login_button.place(relx=0.5, rely=0.2, relwidth=0.3, relheight=0.15, anchor="n")

if __name__ == "__main__":
    slanch = launcher.Launcher()
    window = Window(slanch)
    Thread(target=slanch.refresh_login).start()
    window.mainloop()