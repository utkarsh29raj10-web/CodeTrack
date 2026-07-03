import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BG_COLOR = "#18181B"

class AnimatedButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.orig_text_color = self.cget("text_color")
        self.orig_border_color = self.cget("border_color")

        self.bind("<Button-1>", self.on_press)
        self.bind('<ButtonRelease-1>', self.on_release)

    def on_press(self, event):
        self.configure(text_color="white")
        if self.orig_border_color and self.orig_border_color != "transparent":
            self.configure(border_color="#52525b")

    def on_release(self, event):
        self.configure(text_color=self.orig_text_color)

        if self.orig_border_color and self.orig_border_color != "transparent":
            self.configure(border_color=self.orig_border_color)

class BackButton(AnimatedButton):
    def __init__(self, parent, controller, target):
        super().__init__(
            parent,
            text="←",
            width=60,
            height=50,
            fg_color="transparent",
            hover_color="#27272a",
            text_color="#F3F3F3",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=lambda:controller.show_frame(target)
        )

class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_COLOR)
        self.controller = controller

        title_label = ctk.CTkLabel(
            self,
            text="Welcome to CodeTrack",
            font = ctk.CTkFont(size=28, weight="bold"),
            text_color="#F3F3F3"
        )
        title_label.pack(pady=(50,20))

        subtitle = ctk.CTkLabel(
            self,
            text = "Choose your setup mode to begin",
            font = ctk.CTkFont(size=16),
            text_color="#A1A1AA"
        )
        subtitle.pack(pady=(0,40))

        btn_enterprise = AnimatedButton(
            self,
            text="Enterprise Mode (For Companies)",
            height = 50,
            text_color="#FFFFFF",
            font = ctk.CTkFont(size=15, weight="bold"),
            command = lambda: self.controller.show_frame("EnterpriseMenu"),
        )
        btn_enterprise.pack(pady=15, padx=60, fill="x")

        btn_indep = AnimatedButton(
            self,
            text="Independent Mode (For Freelancers/Personal Use)",
            height=50,
            fg_color = BG_COLOR,
            border_color="#3b82f6",
            border_width = 2,
            hover_color="#27272a",
            text_color="#FFFFFF",
            font = ctk.CTkFont(size=15, weight="bold"),
            command = lambda: self.controller.show_frame("IndependentScreen")
        )
        btn_indep.pack(pady=15, padx=60, fill="x")

class EnterpriseMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_COLOR)
        self.controller = controller

        BackButton(self, self.controller, target="MainMenu").place(x=20, y=20)

        title_label = ctk.CTkLabel(
            self,
            text="Enterprise Setup",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#F3F3F3"
        )
        title_label.pack(pady=(70, 20))

        subtitle = ctk.CTkLabel(
            self,
            text="Are you an employee or a new employer?",
            font = ctk.CTkFont(size=14),
            text_color="#A1A1AA"
        )
        subtitle.pack(pady=(0,40))

        btn_employer = AnimatedButton(
            self,
            text="I am an Employer",
            height=50,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=lambda: self.controller.show_frame("EmployerScreen")
        )
        btn_employer.pack(pady=15, padx=60, fill="x")

        btn_employee = AnimatedButton(
            self,
            text="I am an Employee",
            height=50,
            fg_color=BG_COLOR,
            border_color="#3b82f6",
            border_width=2,
            hover_color="#27272a",
            text_color="#ffffff",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=lambda: self.controller.show_frame("EmployeeScreen")
        )
        btn_employee.pack(pady=15, padx=60, fill="x")

class EmployerScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_COLOR)
        self.controller = controller

        BackButton(self, self.controller, target="EnterpriseMenu").place(x=20, y=20)

        title_label = ctk.CTkLabel(
            self,
            text="Employer Setup",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#F3F3F3"
        )
        title_label.pack(pady=(60,10))

        subtitle = ctk.CTkLabel(
            self,
            text="Generate special encrypted keys for your employees.",
            font=ctk.CTkFont(size=14),
            text_color="#A1A1AA"
        )
        subtitle.pack(pady=(0,20))

        self.entry_api = ctk.CTkEntry(
            self,
            placeholder_text = "Enter API key",
            height = 45,
            show="*"
        )
        self.entry_api.pack(fill="x", padx=60, pady=10)
        self.entry_url=ctk.CTkEntry(
            self,
            placeholder_text="Enter Dashboard URL (optional)",
            height=45
        )
        self.entry_url.pack(fill="x", padx=60, pady = 10)

        self.entry_name = ctk.CTkEntry(
            self,
            placeholder_text="Enter Employee Name (Optional)",
            height=45
        )
        self.entry_name.pack(fill="x", padx=60, pady=10)

        btn_generate = AnimatedButton(
            self,
            text="Generate Shareable Encrypted Code",
            height=50,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=lambda: print("It will call security manager") #todo
        )
        btn_generate.pack(pady=15, padx=60, fill="x")

        self.output_box = ctk.CTkTextbox(
            self,
            height=70,
            fg_color="#09090b",
            text_color="#34d399",
            font=ctk.CTkFont(family="Courier", size=12)
        )
        self.output_box.pack(fill="x", padx=60, pady=(0,10))
        self.output_box.insert("0.0", "Your encrypted code will appear here.")
        self.output_box.configure(state="disabled")

class EmployeeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_COLOR)
        self.controller = controller

        BackButton(self, self.controller, target="EnterpriseMenu").place(x=20, y=20)

        title_label = ctk.CTkLabel(
            self,
            text="Employee Setup",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#F3F3F3"
        )
        title_label.pack(pady=(60,10))

        subtitle = ctk.CTkLabel(
            self,
            text="Paste the secret code provided by your employer",
            font=ctk.CTkFont(size=14),
            text_color="#A1A1AA"
        )
        subtitle.pack(pady=(0,20))

        self.entry_code = ctk.CTkEntry(
            self,
            placeholder_text="Enter Secure Code", height=45
        )
        self.entry_code.pack(fill="x", padx=60, pady=10)

        self.entry_name = ctk.CTkEntry(
            self,
            placeholder_text="Enter your Full Name (Optional)",
            height=45
        )
        self.entry_name.pack(fill="x", padx=60, pady=10)

        btn_install = AnimatedButton(
            self,
            text="Install & Connect",
            height=50,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=lambda: print("installer logic later")
        )
        btn_install.pack(pady=15, padx=60, fill="x")

class IndependentScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_COLOR)
        self.controller = controller

        BackButton(self, self.controller, target="MainMenu").place(x=20, y=20)
        title_label = ctk.CTkLabel(
            self, text="Independent Setup",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#F3F3F3"
        )
        title_label.pack(pady=(70,10))

        subtitle = ctk.CTkLabel(
            self, text="Setup CodeTrack for your personal projects",
            font=ctk.CTkFont(size=14),
            text_color="#A1A1AA"
        )
        subtitle.pack(pady=(0,30))

        self.entry_api = ctk.CTkEntry(
            self,
            placeholder_text="Enter WakaTime API Key",
            height=45,
            show="*"
        )
        self.entry_api.pack(fill="x", padx=60, pady=10)

        btn_install = AnimatedButton(
            self,
            text="Install Engine",
            height=50,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=lambda: print("installer later")
        )
        btn_install.pack(pady=20, padx=60, fill="x")

class CodeTrackApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.configure(fg_color=BG_COLOR)

        self.title("CodeTrack Setup")
        self.geometry("600x450")
        self.resizable(False, False)

        self.container = ctk.CTkFrame(self, fg_color=BG_COLOR)
        self.container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        self.current_frame = None

        for F in (MainMenu, EnterpriseMenu, EmployerScreen, EmployeeScreen, IndependentScreen):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

        self.show_frame("MainMenu")

    def show_frame(self, page_name: str):
        if self.current_frame is not None:
            self.current_frame.pack_forget()

        frame = self.frames[page_name]
        frame.pack(fill="both", expand=True)

        self.current_frame = frame

if __name__ == "__main__":
    app = CodeTrackApp()
    app.mainloop()