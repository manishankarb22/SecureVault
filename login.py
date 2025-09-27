import customtkinter as ctk
from tkinter import messagebox
from database import DatabaseManager
from security import SecurityManager, InputValidator

class LoginPage:
    def __init__(self, parent, show_signup_page, show_home_page, main_app=None):
        self.parent = parent
        self.show_signup_page = show_signup_page
        self.show_home_page = show_home_page
        self.db_manager = DatabaseManager()
        self.validator = InputValidator()
        self.login_username = None
        self.login_password = None
        self.main_app = main_app  # Reference to MainApp for notifications
        
        self.build_ui()
        # Remove all animation-related variables and after calls

    def build_ui(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        # Main login card
        self.login_card = ctk.CTkFrame(
            self.parent,
            width=450,
            height=650,
            corner_radius=0,
            fg_color="#FFFFFF",
            border_width=2,
            border_color="#E0E0E0"
        )
        self.login_card.place(relx=0.5, rely=0.5, anchor="center")
        self.login_card.pack_propagate(False)
        # Header section
        header_frame = ctk.CTkFrame(self.login_card, fg_color="transparent")
        header_frame.pack(pady=(30, 15))
        logo_frame = ctk.CTkFrame(
            header_frame,
            width=60,
            height=60,
            corner_radius=0,
            fg_color="#000000"
        )
        logo_frame.pack()
        ctk.CTkLabel(
            logo_frame,
            text="🔐",
            font=ctk.CTkFont(size=28),
            text_color="#FFFFFF"
        ).place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(
            header_frame,
            text="SECURE VAULT",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#000000"
        ).pack(pady=(12, 4))
        ctk.CTkLabel(
            header_frame,
            text="Access your encrypted vault",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        ).pack()
        # Form section
        form_frame = ctk.CTkFrame(self.login_card, fg_color="transparent")
        form_frame.pack(pady=12, padx=35)
        username_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        username_container.pack(pady=(0, 12), fill="x")
        ctk.CTkLabel(
            username_container,
            text="👤 USERNAME",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w", padx=5, pady=(0, 4))
        self.login_username = ctk.CTkEntry(
            username_container,
            placeholder_text="Enter your username",
            width=340,
            height=36,
            font=ctk.CTkFont(size=12),
            corner_radius=0,
            border_width=2,
            border_color="#CCCCCC",
            fg_color="#F8F8F8",
            text_color="#000000"
        )
        self.login_username.pack()
        password_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_container.pack(pady=(0, 12), fill="x")
        ctk.CTkLabel(
            password_container,
            text="🔑 PASSWORD",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w", padx=5, pady=(0, 4))
        self.login_password = ctk.CTkEntry(
            password_container,
            placeholder_text="Enter your password",
            show="*",
            width=340,
            height=36,
            font=ctk.CTkFont(size=12),
            corner_radius=0,
            border_width=2,
            border_color="#CCCCCC",
            fg_color="#F8F8F8",
            text_color="#000000"
        )
        self.login_password.pack()
        # Login button
        login_btn = ctk.CTkButton(
            self.login_card,
            text="🔓 SECURE LOGIN",
            width=280,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=0,
            fg_color="#000000",
            hover_color="#333333",
            text_color="#FFFFFF",
            command=self.handle_login
        )
        login_btn.pack(pady=(10, 10))
        # Divider section
        divider_frame = ctk.CTkFrame(self.login_card, fg_color="transparent")
        divider_frame.pack(fill="x", padx=45, pady=8)
        ctk.CTkFrame(divider_frame, height=1, fg_color="#E0E0E0", corner_radius=0).pack(fill="x")
        ctk.CTkLabel(
            divider_frame,
            text="OR",
            font=ctk.CTkFont(size=8, weight="bold"),
            text_color="#999999",
            fg_color="#FFFFFF"
        ).place(relx=0.5, rely=0, anchor="center")
        # Create account section
        create_section = ctk.CTkFrame(self.login_card, fg_color="transparent")
        create_section.pack(pady=6)
        ctk.CTkLabel(
            create_section,
            text="Don't have an account?",
            font=ctk.CTkFont(size=10),
            text_color="#666666"
        ).pack(pady=(0, 6))
        create_account_btn = ctk.CTkButton(
            create_section,
            text="⚪ CREATE ACCOUNT",
            width=240,
            height=36,
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=0,
            fg_color="transparent",
            hover_color="#F5F5F5",
            text_color="#000000",
            border_width=2,
            border_color="#000000",
            command=self.show_signup_page
        )
        create_account_btn.pack(pady=(0, 20))
        # Bind Enter key to login
        self.parent.bind('<Return>', lambda e: self.handle_login())

    def handle_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()
        if not username or not password:
            if self.main_app:
                self.main_app.show_notification("Please enter both username and password", type="error")
            return
        user_info = self.db_manager.authenticate_user(username, password)
        if user_info:
            if self.main_app:
                self.main_app.show_notification(f"Welcome back, {username}!", type="success")
            self.show_home_page(user_info)
        else:
            if self.main_app:
                self.main_app.show_notification("Invalid username or password", type="error")
 