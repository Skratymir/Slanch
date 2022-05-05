import tkinter

class Window(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
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
        self.frames["LaunchPage"].grid(row=0, column=0, sticky="nsew")
        
        self.set_page("LaunchPage")
        
    def set_page(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
class LaunchPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        self.setup()
        
    def setup(self):
        self.launch_button = tkinter.Button(self, text="Launch")
        self.launch_button.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.3, relheight=0.3)

window = Window()
window.mainloop()