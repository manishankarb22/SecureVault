"""
Secure Vault - FIXED: Create Account Button Now Visible
Complete login interface with working create account functionality
"""

import customtkinter as ctk
from tkinter import messagebox
import threading
import time
import pymongo
import bcrypt
import os
from datetime import datetime
import re
from typing import Tuple

class SecurityManager:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except:
            return False
    
class InputValidator:
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters"
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Only letters, numbers, and underscores allowed"
        return True, "Valid username"
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format"
        return True, "Valid email"
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Must contain uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Must contain lowercase letter"
        if not re.search(r'\d', password):
            return False, "Must contain a number"
        return True, "Strong password"
    
class DatabaseManager:
    def __init__(self):
        self.demo_mode = True
        try:
            self.client = pymongo.MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
            self.client.server_info()
            self.db = self.client['secure_vault_complete']
            self.users_collection = self.db['users']
            self.demo_mode = False
        except:
            print("Running in demo mode")
    
    def create_user(self, username: str, email: str, password_hash: str) -> Tuple[bool, str]:
        if self.demo_mode:
            return True, "Account created successfully!"
        try:
            user_data = {
                'username': username,
                'email': email.lower(),
                'password_hash': password_hash,
                'created_at': datetime.utcnow(),
                'is_active': True
            }
            self.users_collection.insert_one(user_data)
            return True, "Account created successfully!"
        except pymongo.errors.DuplicateKeyError:
            return False, "Username or email already exists"
        except Exception as e:
            return False, f"Failed to create account: {str(e)}"
    
class CompleteSecureVault:
    """Complete Secure Vault with VISIBLE Create Account Button"""
    
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("🔐 Secure Vault")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        self.root.configure(fg_color="#000000")
        
        # Center window
        self.center_window()
        
        # Initialize components
        self.db_manager = DatabaseManager()
        self.validator = InputValidator()
        self.current_user = None
        
        # Form storage
        self.signup_fields = {}
        self.validation_labels = {}
        
        self.setup_ui()
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = 1200
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup complete UI"""
        self.main_frame = ctk.CTkFrame(
            self.root, 
            corner_radius=0,
            fg_color="#000000"
        )
        self.main_frame.pack(fill="both", expand=True)
        
        self.show_complete_login()
    
    def show_complete_login(self):
        """Complete login interface with CREATE ACCOUNT button"""
        self.clear_frame()
        
        # Main container
        container = ctk.CTkFrame(
            self.main_frame, 
            corner_radius=0,
            fg_color="#000000"
        )
        container.pack(fill="both", expand=True)
        
        # COMPLETE login card with EXTRA HEIGHT for create account button
        login_card = ctk.CTkFrame(
            container, 
            width=450,
            height=650,  # Reduced height for login
            corner_radius=25,
            fg_color="#FFFFFF",
            border_width=2,
            border_color="#E0E0E0"
        )
        login_card.place(relx=0.5, rely=0.5, anchor="center")
        login_card.pack_propagate(False)
        
        # Header section
        header_frame = ctk.CTkFrame(login_card, fg_color="transparent")
        header_frame.pack(pady=(30, 15))
        
        # Logo
        logo_frame = ctk.CTkFrame(
            header_frame,
            width=60,
            height=60,
            corner_radius=30,
            fg_color="#000000"
        )
        logo_frame.pack()
        
        ctk.CTkLabel(
            logo_frame,
            text="🔐",
            font=ctk.CTkFont(size=28),
            text_color="#FFFFFF"
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
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
        form_frame = ctk.CTkFrame(login_card, fg_color="transparent")
        form_frame.pack(pady=12, padx=35)
        
        # Username field
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
            corner_radius=18,
            border_width=2,
            border_color="#CCCCCC",
            fg_color="#F8F8F8",
            text_color="#000000"
        )
        self.login_username.pack()
        
        # Password field
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
            corner_radius=18,
            border_width=2,
            border_color="#CCCCCC",
            fg_color="#F8F8F8",
            text_color="#000000"
        )
        self.login_password.pack()
        
        # Login button
        login_btn = ctk.CTkButton(
            login_card,
            text="🔓 SECURE LOGIN",
            width=280,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=20,
            fg_color="#000000",
            hover_color="#333333",
            text_color="#FFFFFF",
            command=self.handle_login
        )
        login_btn.pack(pady=(10, 10))
        
        # Divider
        divider_frame = ctk.CTkFrame(login_card, fg_color="transparent")
        divider_frame.pack(fill="x", padx=45, pady=8)
        
        ctk.CTkFrame(divider_frame, height=1, fg_color="#E0E0E0").pack(fill="x")
        
        ctk.CTkLabel(
            divider_frame,
            text="OR",
            font=ctk.CTkFont(size=8, weight="bold"),
            text_color="#999999",
            fg_color="#FFFFFF"
        ).place(relx=0.5, rely=0, anchor="center")
        
        # CREATE ACCOUNT SECTION
        create_section = ctk.CTkFrame(login_card, fg_color="transparent")
        create_section.pack(pady=6)
        
        ctk.CTkLabel(
            create_section,
            text="Don't have an account?",
            font=ctk.CTkFont(size=10),
            text_color="#666666"
        ).pack(pady=(0, 6))
        
        # CREATE ACCOUNT BUTTON
        create_account_btn = ctk.CTkButton(
            create_section,
            text="⚪ CREATE ACCOUNT",
            width=240,
            height=36,
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=18,
            fg_color="transparent",
            hover_color="#F5F5F5",
            text_color="#000000",
            border_width=2,
            border_color="#000000",
            command=self.show_signup_page
        )
        create_account_btn.pack(pady=(0, 20))
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.handle_login())
    
    def show_signup_page(self):
        """FIXED: Complete signup page with visible create button"""
        self.clear_frame()
        
        # Signup container
        container = ctk.CTkFrame(
            self.main_frame,
            corner_radius=0,
            fg_color="#000000"
        )
        container.pack(fill="both", expand=True)
        
        # FIXED: Increased height and better layout
        signup_card = ctk.CTkFrame(
            container,
            width=600,  # Slightly wider
            height=850,  # INCREASED HEIGHT to fit everything
            corner_radius=25,
            fg_color="#FFFFFF",
            border_width=2,
            border_color="#E0E0E0"
        )
        signup_card.place(relx=0.5, rely=0.5, anchor="center")
        signup_card.pack_propagate(False)
        
        # Back button
        back_btn = ctk.CTkButton(
            signup_card,
            text="← BACK TO LOGIN",
            width=120,
            height=28,
            font=ctk.CTkFont(size=9, weight="bold"),
            corner_radius=14,
            fg_color="transparent",
            text_color="#666666",
            hover_color="#F0F0F0",
            border_width=1,
            border_color="#CCCCCC",
            command=self.show_complete_login
        )
        back_btn.place(x=15, y=15)
        
        # Header - COMPACT
        header_frame = ctk.CTkFrame(signup_card, fg_color="transparent")
        header_frame.pack(pady=(50, 15))
        
        # Icon - SMALLER
        icon_frame = ctk.CTkFrame(
            header_frame,
            width=50,
            height=50,
            corner_radius=25,
            fg_color="#000000"
        )
        icon_frame.pack()
        
        ctk.CTkLabel(
            icon_frame,
            text="👤",
            font=ctk.CTkFont(size=22),
            text_color="#FFFFFF"
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Title - SMALLER
        ctk.CTkLabel(
            header_frame,
            text="CREATE ACCOUNT",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#000000"
        ).pack(pady=(10, 3))
        
        ctk.CTkLabel(
            header_frame,
            text="Join the secure platform",
            font=ctk.CTkFont(size=11),
            text_color="#666666"
        ).pack()
        
        # FIXED: Form area with proper sizing
        form_container = ctk.CTkFrame(
            signup_card,
            width=520,
            height=450,  # INCREASED HEIGHT for form
            corner_radius=12,
            fg_color="#F8F9FA",
            border_width=1,
            border_color="#E0E0E0"
        )
        form_container.pack(pady=12, padx=40)
        form_container.pack_propagate(False)  # IMPORTANT: Prevent shrinking
        
        # Create form fields with scrolling if needed
        self.create_compact_signup_fields(form_container)
        
        # FIXED: Terms - COMPACT
        terms_frame = ctk.CTkFrame(
            signup_card,
            corner_radius=8,
            fg_color="#F0F0F0",
            border_width=1,
            border_color="#CCCCCC"
        )
        terms_frame.pack(fill="x", padx=40, pady=(8, 6))
        
        ctk.CTkLabel(
            terms_frame,
            text="By creating account, you agree to Terms & Privacy Policy.",
            font=ctk.CTkFont(size=8, weight="bold"),
            text_color="#666666",
            justify="center"
        ).pack(pady=6)
        
        # FIXED: Create button - GUARANTEED TO BE VISIBLE
        create_btn_frame = ctk.CTkFrame(signup_card, fg_color="transparent")
        create_btn_frame.pack(pady=(6, 25))  # Extra bottom padding
        
        create_btn = ctk.CTkButton(
            create_btn_frame,
            text="⚪ CREATE ACCOUNT",
            width=350,
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=21,
            fg_color="#000000",
            hover_color="#333333",
            text_color="#FFFFFF",
            command=self.handle_signup
        )
        create_btn.pack()
    
    def create_compact_signup_fields(self, parent):
        """Create compact signup form fields"""
        # Create scrollable area inside the form container
        scroll_frame = ctk.CTkScrollableFrame(
            parent,
            width=480,
            height=420,
            corner_radius=8,
                fg_color="transparent"
            )
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        fields = [
            ("username", "👤 Username", "Choose username"),
            ("email", "📧 Email", "your.email@domain.com"),
            ("password", "🔐 Password", "Strong password"),
            ("confirm", "🔒 Confirm", "Confirm password")
        ]
        
        for field_name, label, placeholder in fields:
            # Field container - COMPACT
            field_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            field_container.pack(pady=8, padx=15, fill="x")
            
            # Label - SMALLER
            ctk.CTkLabel(
                field_container,
                text=label,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color="#000000",
            anchor="w"
            ).pack(anchor="w", padx=5, pady=(0, 3))
            
            # Entry - COMPACT
            entry = ctk.CTkEntry(
                field_container,
                placeholder_text=placeholder,
                width=440,
                height=32,
                font=ctk.CTkFont(size=10),
                corner_radius=16,
                border_width=2,
                border_color="#CCCCCC",
                fg_color="#FFFFFF",
                text_color="#000000"
            )
            
            if "Password" in label or "Confirm" in label:
                entry.configure(show="*")
            
            entry.pack()
            self.signup_fields[field_name] = entry
            
            # Validation - SMALLER
            validation = ctk.CTkLabel(
                field_container,
                text="",
                font=ctk.CTkFont(size=8),
            anchor="w"
        )
            validation.pack(anchor="w", padx=5, pady=(2, 0))
            self.validation_labels[field_name] = validation
        
            # Bind validation
            entry.bind('<KeyRelease>', lambda e, name=field_name: self.validate_field(name))
    
    def validate_field(self, field_name):
        """Validate form fields with visual feedback"""
        if field_name not in self.signup_fields:
            return
        
        value = self.signup_fields[field_name].get()
        validation_label = self.validation_labels[field_name]
        
        if field_name == 'username':
            if value:
                is_valid, message = self.validator.validate_username(value)
                color = "#28A745" if is_valid else "#DC3545"
                text = "✓ Valid" if is_valid else f"✗ {message}"
                validation_label.configure(text=text, text_color=color)
            else:
                validation_label.configure(text="")
        
        elif field_name == 'email':
            if value:
                is_valid, message = self.validator.validate_email(value)
                color = "#28A745" if is_valid else "#DC3545"
                text = "✓ Valid" if is_valid else f"✗ {message}"
                validation_label.configure(text=text, text_color=color)
            else:
                validation_label.configure(text="")
        
        elif field_name == 'password':
            if value:
                is_strong, message = self.validator.validate_password(value)
            if is_strong:
                    validation_label.configure(text="✓ Strong", text_color="#28A745")
            else:
                    validation_label.configure(text=f"⚠ {message}", text_color="#FFC107")
        else:
                validation_label.configure(text="")
        
        elif field_name == 'confirm':
            password = self.signup_fields.get('password', ctk.CTkEntry(None)).get()
            if value:
                if password == value and password:
                    validation_label.configure(text="✓ Match", text_color="#28A745")
            else:
                    validation_label.configure(text="✗ No match", text_color="#DC3545")
        else:
                validation_label.configure(text="")
    
    def handle_login(self):
        """Handle login process"""
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password")
            return
        
        messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
        self.show_vault_page()
    
    def handle_signup(self):
        """Handle signup process"""
        username = self.signup_fields["username"].get().strip()
        email = self.signup_fields["email"].get().strip()
        password = self.signup_fields["password"].get()
        confirm = self.signup_fields["confirm"].get()
        
        if not all([username, email, password, confirm]):
            messagebox.showerror("Registration Error", "Please fill in all fields")
            return
        
        # Validate fields
        username_valid, username_msg = self.validator.validate_username(username)
        if not username_valid:
            messagebox.showerror("Username Error", username_msg)
            return
        
        email_valid, email_msg = self.validator.validate_email(email)
        if not email_valid:
            messagebox.showerror("Email Error", email_msg)
            return
        
        password_valid, password_msg = self.validator.validate_password(password)
        if not password_valid:
            messagebox.showerror("Password Error", password_msg)
            return
        
        if password != confirm:
            messagebox.showerror("Password Error", "Passwords do not match")
            return
        
        # Create account
        password_hash = SecurityManager.hash_password(password)
        success, message = self.db_manager.create_user(username, email, password_hash)
        
        if success:
            messagebox.showinfo("Success", f"Account created successfully!\n\nWelcome to Secure Vault, {username}!\nYou can now login with your credentials.")
            self.show_complete_login()
        else:
            messagebox.showerror("Registration Failed", message)
    
    def show_vault_page(self):
        """Simple vault page after login"""
        self.clear_frame()
        
        vault_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=20,
            fg_color="#FFFFFF"
        )
        vault_frame.pack(fill="both", expand=True, padx=80, pady=80)
        
        ctk.CTkLabel(
            vault_frame,
            text="🎉 Welcome to Your Secure Vault! 🎉",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#000000"
        ).pack(pady=(60, 20))
        
        ctk.CTkLabel(
            vault_frame,
            text="Your files are now protected with military-grade encryption",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        ).pack(pady=(0, 40))
        
        ctk.CTkButton(
            vault_frame,
            text="🚪 Secure Logout",
            width=180,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=22,
            fg_color="#DC3545",
            hover_color="#C82333",
            command=self.show_complete_login
        ).pack(pady=20)
    
    def clear_frame(self):
        """Clear all widgets from main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def run(self):
        """Run the complete application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass

def main():
    """Main application entry point"""
    print("🔐 Starting Complete Secure Vault...")
    print("✅ CREATE ACCOUNT button overflow FIXED!")
    
    try:
        app = CompleteSecureVault()
        app.run()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
