import launcher
import tkinter
import tkinter.messagebox

from tkinter import font as tkFont
from tkinter import ttk
from functools import partial

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
        
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        self.frames["LaunchPage"] = LaunchPage(parent=container, controller=self)
        self.frames["ProfilesPage"] = ProfilesPage(parent=container, controller=self)
        self.frames["SettingsPage"] = SettingsPage(parent=container, controller=self)
        self.frames["ProfileCreationPage"] = ProfileCreationPage(parent=container, controller=self)
        self.frames["ProfileEditingPage"] = ProfileEditingPage(parent=container, controller=self)
        self.frames["InstallationPage"] = InstallationPage(parent=container, controller=self)
        self.frames["VersionSelectionPopup"] = VersionSelectionPopup(parent=self)
        
        self.frames["LaunchPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["ProfilesPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["SettingsPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["ProfileCreationPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["ProfileEditingPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["InstallationPage"].grid(row=0, column=0, sticky="nsew")
        
        self.set_page("LaunchPage")
        self.update()
        self.frames["ProfilesPage"].create_frame()
        self.frames["ProfileCreationPage"].resize_font(0)
        self.frames["ProfileEditingPage"].resize_font(0)
        self.frames["InstallationPage"].resize_font(0)
        
        
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
        
        self.launch_page_button.place(relx=0, rely=0, relwidth=0.33, relheight=0.15, anchor="nw")
        self.profiles_page_button.place(relx=0.33, rely=0, relwidth=0.34, relheight=0.15, anchor="nw")
        self.settings_page_button.place(relx=1, rely=0, relwidth=0.33, relheight=0.15, anchor="ne")
        
        self.launch_button = tkinter.Button(self, text="Launch", command=lambda: launcher.launch_profile(self.variable.get()))
        
        self.options = launcher.load_all_profiles_by_name()
        self.variable = tkinter.StringVar(self)
        if len(self.options) == 0:
            self.options = ["None"]
        self.variable.set(self.options[0])
        self.profile_selection = tkinter.OptionMenu(self, self.variable, *self.options)
        
        self.launch_button.place(relx=0.5, rely=0.5, relwidth=0.3, relheight=0.3, anchor="center")
        self.profile_selection.place(relx=0.5, rely=0.7, relwidth=0.3, relheight=0.2, anchor="n")
        
class ProfilesPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        
        self.launch_page_button = tkinter.Button(self, command=lambda: controller.set_page("LaunchPage"))
        self.profiles_page_button = tkinter.Button(self)
        self.settings_page_button = tkinter.Button(self, command=lambda: controller.set_page("SettingsPage"))
        
        self.launch_page_button.place(relx=0, rely=0, relwidth=0.33, relheight=0.15, anchor="nw")
        self.profiles_page_button.place(relx=0.33, rely=0, relwidth=0.34, relheight=0.15, anchor="nw")
        self.settings_page_button.place(relx=1, rely=0, relwidth=0.33, relheight=0.15, anchor="ne")
        
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

        self.profile_frames = []
        
        self.add_profiles_to_canvas()
        
        self.profiles_canvas.place(relx=0.05, rely=0.2, relwidth=0.915, relheight=0.8, anchor="nw")
        self.profiles_scrollbar.place(relx=1, rely=0.2, relheight=0.8, relwidth=0.035, anchor="ne")
        
    def create_frame(self):
        self.profiles_canvas.create_window((0, 0), window=self.profiles_frame, anchor="nw", width=self.profiles_canvas.winfo_width())

    def add_profiles_to_canvas(self):
        for profile_frame in self.profile_frames:
            profile_frame.pack_forget()
        if hasattr(self, "frame"):
            self.frame.pack_forget()
        self.profiles = launcher.load_all_profiles()

        for profile in self.profiles:
            self.frame = tkinter.Frame(self.profiles_frame)
            tkinter.Label(self.frame, text=profile["id"], anchor="w").pack(side="left")
            tkinter.Button(self.frame, text="delete", anchor="w", command=partial(self.delete_profile, profile["id"])).pack(side="right")
            tkinter.Button(self.frame, text="edit", anchor="e", command=partial(self.edit_profile, profile["id"])).pack(side="right")
            self.frame.pack(side="bottom", anchor="w", fill="both", expand=True)
            self.profile_frames.append(self.frame)
        self.frame = tkinter.Frame(self.profiles_frame)
        tkinter.Button(self.frame, text="Create new Profile", command=lambda: self.controller.set_page("ProfileCreationPage")).pack()
        self.frame.pack(side="bottom", anchor="w", fill="both", expand=True)
        
    def delete_profile(self, id):
        for profile_frame in self.profile_frames:
            if profile_frame.winfo_children()[0]["text"] == id:
                profile_frame.pack_forget()
                launcher.delete_profile(id)
                option_id = self.controller.frames["LaunchPage"].options.index(id)
                self.controller.frames["LaunchPage"].profile_selection["menu"].delete(option_id, option_id)
                self.controller.frames["LaunchPage"].options.remove(id)
                if len(self.controller.frames["LaunchPage"].options) == 0:
                    self.controller.frames["LaunchPage"].variable.set("None")
                else:
                    self.controller.frames["LaunchPage"].variable.set(self.controller.frames["LaunchPage"].options[0])
                    
    def edit_profile(self, old_name):
        self.controller.frames["ProfileEditingPage"].profile_name_input.insert(0, old_name)
        self.controller.frames["ProfileEditingPage"].old_name = old_name
        for profile in launcher.load_all_profiles():
            if profile["id"] == old_name:
                self.controller.frames["ProfileEditingPage"].selected_version.set(profile["version"])
                self.controller.frames["ProfileEditingPage"].profile_ram_input.set(profile["args"][0][4:5])
        
        self.controller.set_page("ProfileEditingPage")
        
class SettingsPage(tkinter.Frame):
    def __init__(self, parent, controller):
        global login_button
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        
        launch_page_button = tkinter.Button(self, command=lambda: controller.set_page("LaunchPage"))
        profiles_page_button = tkinter.Button(self, command=lambda: controller.set_page("ProfilesPage"))
        settings_page_button = tkinter.Button(self)
        
        launch_page_button.place(relx=0, rely=0, relwidth=0.33, relheight=0.15, anchor="nw")
        profiles_page_button.place(relx=0.33, rely=0, relwidth=0.34, relheight=0.15, anchor="nw")
        settings_page_button.place(relx=1, rely=0, relwidth=0.33, relheight=0.15, anchor="ne")
        
        self.login_button = tkinter.Button(self, text="Login", command=lambda: self.login_out())
        self.install_minecraft_version_button = tkinter.Button(self, text="Install Minecraft Version", command=lambda: controller.set_page("InstallationPage"))
        
        self.login_button.place(relx=0.5, rely=0.2, relwidth=0.3, relheight=0.15, anchor="n")
        self.install_minecraft_version_button.place(relx=0.5, rely= 0.4, relwidth=0.3, relheight=0.15, anchor="n")
        
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
        
        all_installed_versions = launcher.load_all_installed_versions()
        self.selected_version = tkinter.StringVar(self)
        self.selected_version.set(all_installed_versions[0])
        
        self.title_label = tkinter.Label(self, text="Create Profile")
        self.profile_name_label = tkinter.Label(self, text="Profile name")
        self.profile_version_label = tkinter.Label(self, text="Version")
        self.profile_ram_label = tkinter.Label(self, text="Allocated RAM")
        self.profile_name_input = tkinter.Entry(self)
        self.profile_version_dropdown = tkinter.OptionMenu(self, self.selected_version, *all_installed_versions)
        self.profile_ram_input = tkinter.Scale(self, from_=1, to=8, orient="horizontal")
        self.profile_creation_button = tkinter.Button(self, text="Create", command=self.launcher_create_profile)
        
        self.title_label.place(relx=0.5, rely=0.03, relwidth=1, relheight=0.2, anchor="n")
        self.profile_name_label.place(relx=0.05, rely=0.25, relwidth=0.4, relheight=0.2, anchor="nw")
        self.profile_name_input.place(relx=0.5, rely=0.3, relwidth=0.4, relheight=0.1, anchor="nw")
        self.profile_version_label.place(relx=0.1, rely=0.45, relwidth=0.3, relheight=0.2, anchor="nw")
        self.profile_version_dropdown.place(relx=0.5, rely=0.5, relwidth=0.4, relheight=0.1, anchor="nw")
        self.profile_ram_label.place(relx=0.05, rely=0.65, relwidth=0.4, relheight=0.2, anchor="nw")
        self.profile_ram_input.place(relx=0.5, rely=0.65, relwidth=0.4, relheight=0.15, anchor="nw")
        self.profile_creation_button.place(relx=0.5, rely=0.85, relwidth=0.5, relheight=0.1, anchor="n")
        
        self.bind("<Configure>", self.resize_font)
        
    def resize_font(self, event):
        self.title_label["font"] = tkFont.Font(size=round(self.title_label.winfo_height() - self.title_label.winfo_height() / 3))
        self.profile_name_label["font"] = tkFont.Font(size=round(self.title_label.winfo_height() - self.title_label.winfo_height() / 1.35))
        self.profile_version_label["font"] = tkFont.Font(size=round(self.title_label.winfo_height() - self.title_label.winfo_height() / 1.35))
        self.profile_ram_label["font"] = tkFont.Font(size=round(self.title_label.winfo_height() - self.title_label.winfo_height() / 1.35))
        self.profile_name_input["font"] = tkFont.Font(size=round(self.profile_name_input.winfo_height() - self.profile_name_input.winfo_height() / 2))
        self.profile_ram_input["width"] = (self.profile_ram_input.winfo_height() - self.profile_ram_input.winfo_height() / 2)
        
    def launcher_create_profile(self):
        name = self.profile_name_input.get()
        version = self.selected_version.get()
        ram = self.profile_ram_input.get()
            
        launcher.create_new_profile(name, version, ram)
        
        self.controller.frames["ProfilesPage"].add_profiles_to_canvas()

        self.controller.frames["LaunchPage"].options.append(name)
        self.controller.frames["LaunchPage"].profile_selection.place_forget()
        self.controller.frames["LaunchPage"].profile_selection = tkinter.OptionMenu(self.controller.frames["LaunchPage"], self.controller.frames["LaunchPage"].variable, *self.controller.frames["LaunchPage"].options)
        self.controller.frames["LaunchPage"].profile_selection.place(relx=0.5, rely=0.7, relwidth=0.3, relheight=0.2, anchor="n")
        
        self.controller.set_page("LaunchPage")
        
class ProfileEditingPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller

        self.old_name = ""
        
        self.all_installed_versions = launcher.load_all_installed_versions()
        self.selected_version = tkinter.StringVar(self)
        self.selected_version.set(self.all_installed_versions[0])
        
        self.title_label = tkinter.Label(self, text="Edit Profile")
        self.profile_name_label = tkinter.Label(self, text="Profile name")
        self.profile_version_label = tkinter.Label(self, text="Version")
        self.profile_ram_label = tkinter.Label(self, text="Allocated RAM")
        self.profile_name_input = tkinter.Entry(self)
        self.profile_version_dropdown = tkinter.OptionMenu(self, self.selected_version, *self.all_installed_versions)
        self.profile_ram_input = tkinter.Scale(self, from_=1, to=8, orient="horizontal")
        self.profile_creation_button = tkinter.Button(self, text="Edit", command=self.launcher_edit_profile)
        
        self.title_label.place(relx=0.5, rely=0.03, relwidth=1, relheight=0.2, anchor="n")
        self.profile_name_label.place(relx=0.1, rely=0.25, relwidth=0.3, relheight=0.2, anchor="nw")
        self.profile_name_input.place(relx=0.5, rely=0.3, relwidth=0.4, relheight=0.1, anchor="nw")
        self.profile_version_label.place(relx=0.1, rely=0.45, relwidth=0.3, relheight=0.2, anchor="nw")
        self.profile_version_dropdown.place(relx=0.5, rely=0.5, relwidth=0.4, relheight=0.1, anchor="nw")
        self.profile_ram_label.place(relx=0.1, rely=0.65, relwidth=0.3, relheight=0.2, anchor="nw")
        self.profile_ram_input.place(relx=0.5, rely=0.675, relwidth=0.4, relheight=0.15, anchor="nw")
        self.profile_creation_button.place(relx=0.5, rely=0.85, relwidth=0.5, relheight=0.1, anchor="n")
        
        self.bind("<Configure>", self.resize_font)
        
    def launcher_edit_profile(self):
        if self.profile_name_input.get() != "":
            name = self.profile_name_input.get()
            version = self.selected_version.get()
            ram = self.profile_ram_input.get()

            launcher.edit_profile(self.old_name, name, version, ram)

            self.controller.frames["LaunchPage"].options.append(name)
            self.controller.frames["LaunchPage"].options.remove(self.old_name)
            self.controller.frames["LaunchPage"].variable.set(name)
            self.controller.frames["LaunchPage"].profile_selection.place_forget()
            self.controller.frames["LaunchPage"].profile_selection = tkinter.OptionMenu(self.controller.frames["LaunchPage"], self.controller.frames["LaunchPage"].variable, *self.controller.frames["LaunchPage"].options)
            self.controller.frames["LaunchPage"].profile_selection.place(relx=0.5, rely=0.7, relwidth=0.3, relheight=0.2, anchor="n")

        for profile_frame in self.controller.frames["ProfilesPage"].profile_frames:
            if profile_frame.winfo_children()[0]["text"] == self.old_name:
                profile_frame.winfo_children()[0]["text"] = name
                profile_frame.winfo_children()[1].configure(command=partial(self.controller.frames["ProfilesPage"].delete_profile, name))
                profile_frame.winfo_children()[2].configure(command=partial(self.controller.frames["ProfilesPage"].edit_profile, name))
            
            self.old_name = ""
            self.profile_name_input.delete(0, "end")
            self.controller.set_page("LaunchPage")
        
    def resize_font(self, event):
        self.title_label["font"] = tkFont.Font(size=round(self.title_label.winfo_height() - self.title_label.winfo_height() / 3))
        self.profile_name_label["font"] = tkFont.Font(size=round(self.title_label.winfo_height() - self.title_label.winfo_height() / 1.35))
        self.profile_version_label["font"] = tkFont.Font(size=round(self.title_label.winfo_height() - self.title_label.winfo_height() / 1.35))
        self.profile_ram_label["font"] = tkFont.Font(size=round(self.title_label.winfo_height() - self.title_label.winfo_height() / 1.35))
        self.profile_name_input["font"] = tkFont.Font(size=round(self.profile_name_input.winfo_height() - self.profile_name_input.winfo_height() / 2))
        self.profile_ram_input["width"] = (self.profile_ram_input.winfo_height() - self.profile_ram_input.winfo_height() / 2)

class InstallationPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller

        self.show_snapshots = tkinter.BooleanVar()

        self.all_selected_versions = launcher.load_all_release_versions()
        self.selected_version = tkinter.StringVar(self)
        if not self.all_selected_versions == []:
            self.selected_version.set(self.all_selected_versions[0])
        else:
            self.selected_version = "None"

        self.title_label = tkinter.Label(self, text="Pick Version to install")
        self.version_selection = tkinter.Button(self, text="Version", command=lambda: self.controller.frames["VersionSelectionPopup"].scrollmenu(self.all_selected_versions))
        self.show_snapshots_checkbox = tkinter.Checkbutton(self, text="Show Snapshots", variable=self.show_snapshots, command=self.reload_all_selected_versions)
        self.install_version_button = tkinter.Button(self, text="Install Version", command=self.install_minecraft_version)
        self.install_progressbar = ttk.Progressbar(self, orient="horizontal", mode="determinate", length=200)

        self.title_label.place(relx=0.5, rely=0.03, relwidth=1, relheight=0.2, anchor="n")
        self.version_selection.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.3, anchor="n")
        self.show_snapshots_checkbox.place(relx=0.5, rely=0.65, anchor="center")
        self.install_version_button.place(relx=0.5, rely=0.9, relwidth=0.3, relheight=0.15, anchor="s")
        self.install_progressbar.place(relx=0.5, rely=0.92, relheight=0.05, anchor="n")

    def resize_font(self, event):
        self.title_label["font"] = tkFont.Font(size=round(self.title_label.winfo_height() - self.title_label.winfo_height() / 3))
        self.version_selection["font"] = tkFont.Font(size=round(self.version_selection.winfo_height() - self.version_selection.winfo_height() / 1.35))
        self.install_version_button["font"] = (self.install_version_button.winfo_height() - self.install_version_button.winfo_height() / 2)

    def install_minecraft_version(self):
        version = self.version_selection["text"]
        if version == "Version":
            tkinter.messagebox.showerror("Version Error", "No version was selected")
            return
        print(f"Installing miencraft version {version}")

        callback = {
            "setStatus": lambda text: print(text),
            "setProgress": lambda value: self.set_progressbar_value(value),
            "setMax": lambda value: self.set_maximum_progressvalue(value)
        }

        launcher.minecraft_launcher_lib.install.install_minecraft_version(version, launcher.minecraft_directory, callback=callback)

    def set_maximum_progressvalue(self, value):
        self.install_progressbar["maximum"] = value

    def set_progressbar_value(self, value):
        self.install_progressbar["value"] = value
        self.controller.update()

    def reload_all_selected_versions(self):
        if self.show_snapshots.get() == True:
            self.all_selected_versions = launcher.load_all_available_versions()
        else:
            self.all_selected_versions = launcher.load_all_release_versions()

class VersionSelectionPopup:
    def __init__(self, parent):
        self.parent = parent

    def scrollmenu(self, list):
        self.scrollmenu_window = tkinter.Toplevel()
        self.scrollmenu_window.geometry(f"{round(self.parent.winfo_x() / 2)}x{round(self.parent.winfo_y())}")
        self.scrollmenu_window.geometry("+%d+%d" %(self.parent.winfo_pointerx(), self.parent.winfo_pointery()))
        self.scrollmenu_window.overrideredirect(True)

        self.scrollmenu_window.bind("<FocusOut>", self.quit)

        self.scroll_canvas = tkinter.Canvas(self.scrollmenu_window)
        options_frame = tkinter.Frame(self.scroll_canvas)

        self.scroll_canvas.bind("<Enter>", self.bind_mousewheel)
        self.scroll_canvas.bind("<Leave>", self.unbind_mousewheel)
        options_frame.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(
                scrollregion=self.scroll_canvas.bbox("all")
            )
        )

        self.scroll_canvas.place(relx=0, rely=0, relheight=1, relwidth=0.9, anchor="nw")

        self.scroll_canvas.create_window((0, 0), anchor="nw", window=options_frame)

        for i in range(len(list)):
            button = tkinter.Button(options_frame, text=str(list[i]), border=0, anchor="w", 
            command=partial(self.set_button_text, list[i])
            )
            button.pack(fill="both")

        self.parent.update()

        max_width = button.winfo_width()
        
        self.scrollmenu_window.geometry(f"{round(max_width + max_width / 8)}x{round(self.parent.winfo_y())}")

        scrollbar = tkinter.Scrollbar(self.scrollmenu_window, command=self.scroll_canvas.yview)
        scrollbar.place(relx=0.9, rely=0, relheight=1, relwidth=0.1, anchor="nw")
        self.scroll_canvas.config(yscrollcommand=scrollbar.set)

    def set_button_text(self, text):
        self.parent.frames["InstallationPage"].version_selection["text"] = str(text)
        self.quit()

    def quit(self, event=None):
        self.scrollmenu_window.destroy()

    def bind_mousewheel(self, event=None):
        self.scroll_canvas.bind_all("<MouseWheel>", self.mousewheel_move)

    def unbind_mousewheel(self, event=None):
        self.scroll_canvas.unbind_all("<MouseWheel>")
    
    def mousewheel_move(self, event):
        self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            
def update_login_button():
    if launcher.check_login() == True:
        window.frames["SettingsPage"].login_button["text"] = "Logout"
    else:
        window.frames["SettingsPage"].login_button["text"] = "Login"

if __name__ == "__main__":
    window = Window()
    launcher.refresh_login()
    update_login_button()
    window.minsize(420, 270)
    window.mainloop()
