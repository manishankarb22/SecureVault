import customtkinter as ctk
from tkinter import messagebox, filedialog
import tkinter.simpledialog as simpledialog
import os
import threading
import time
import math

# Black and White Theme Colors
MS_PRIMARY = "#000000"
MS_PRIMARY_HOVER = "#555555"
MS_SECONDARY = "#222222"
MS_SURFACE = "#FFFFFF"
MS_SURFACE_SECONDARY = "#EEEEEE"
MS_SURFACE_TERTIARY = "#DDDDDD"
MS_ACCENT = "#000000"
MS_TEXT_PRIMARY = "#000000"
MS_TEXT_SECONDARY = "#555555"
MS_TEXT_TERTIARY = "#777777"
MS_SUCCESS = "#000000"
MS_WARNING = "#000000"
MS_ERROR = "#000000"
MS_WHITE = "#FFFFFF"
MS_BORDER = "#CCCCCC"
MS_SHADOW = "#00000040"

class HomePage:
    def __init__(self, parent, user_info=None, db_manager=None, show_home_callback=None, main_app_instance=None):
        self.parent = parent
        self.user_info = user_info or {}
        self.db_manager = db_manager
        self.show_home_callback = show_home_callback
        self.main_app = main_app_instance
        self.current_files = []
        self.search_var = ctk.StringVar()
        
        # Animation properties
        self.hover_animations = {}
        self.card_animations = {}
        
        self.active_tooltip = None
        self.build_ui()
    
    def animate_hover(self, widget, hover_in=True, target_color=None):
        """Microsoft-style smooth hover animation"""
        if not target_color:
            target_color = MS_PRIMARY_HOVER if hover_in else MS_PRIMARY
        
        animation_id = id(widget)
        if animation_id in self.hover_animations:
            self.parent.after_cancel(self.hover_animations[animation_id])
        
        def animate_step(step=0):
            if step <= 10:
                progress = step / 10
                if hover_in:
                    # Smooth scale and color transition
                    widget.configure(fg_color=target_color)
                else:
                    widget.configure(fg_color=MS_PRIMARY)
                
                self.hover_animations[animation_id] = self.parent.after(16, lambda: animate_step(step + 1))
        
        animate_step()
    
    def create_fluent_button(self, parent, text, command=None, style="primary", width=None, height=32):
        """Create Microsoft Fluent Design button with animations"""
        if style == "primary":
            fg_color = MS_PRIMARY
            hover_color = MS_PRIMARY_HOVER
            text_color = MS_WHITE
        elif style == "secondary":
            fg_color = MS_SURFACE_SECONDARY
            hover_color = MS_SURFACE_TERTIARY
            text_color = MS_TEXT_PRIMARY
        elif style == "accent":
            fg_color = MS_ACCENT
            hover_color = MS_PRIMARY_HOVER
            text_color = MS_WHITE
        else:
            fg_color = MS_SURFACE
            hover_color = MS_SURFACE_SECONDARY
            text_color = MS_TEXT_PRIMARY
        
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=text_color,
            font=ctk.CTkFont(size=13, weight="normal"),
            corner_radius=4,  # Microsoft's subtle corner radius
            border_width=1,
            border_color=MS_BORDER,
            width=width,
            height=height
        )
        
        # Add hover animation
        def on_enter(event):
            self.animate_button_hover(button, True)
        
        def on_leave(event):
            self.animate_button_hover(button, False)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
    
    def animate_button_hover(self, button, hover_in):
        """Smooth button hover animation"""
        def animate_step(step=0):
            if step <= 8:
                progress = step / 8
                scale = 1.02 if hover_in else 1.0
                # Simulate scale effect by adjusting padding
                current_scale = 1.0 + (scale - 1.0) * progress if hover_in else scale + (1.0 - scale) * progress
                self.parent.after(16, lambda: animate_step(step + 1))
        
        animate_step()
    
    def create_fluent_card(self, parent, fg_color=MS_WHITE, corner_radius=8, border_width=1):
        """Create Microsoft Fluent Design card with subtle shadow effect"""
        card = ctk.CTkFrame(
            parent,
            fg_color=fg_color,
            corner_radius=corner_radius,
            border_width=border_width,
            border_color=MS_BORDER
        )
        
        # Add subtle entrance animation
        self.animate_card_entrance(card)
        
        return card
    
    def animate_card_entrance(self, card):
        """Smooth card entrance animation"""
        def animate_step(step=0):
            if step <= 12:
                progress = step / 12
                opacity = int(progress * 255)
                # Simulate fade-in by adjusting colors
                if step == 12:
                    card.configure(fg_color=MS_WHITE)
                
                self.parent.after(25, lambda: animate_step(step + 1))
        
        animate_step()
    
    def build_ui(self):
        # Clear existing widgets
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        username = self.user_info.get('username', 'User')
        user_email = self.user_info.get('email', 'No email provided')
        
        # Main container with Microsoft background
        main_container = ctk.CTkFrame(self.parent, fg_color=MS_SURFACE, corner_radius=0)
        main_container.pack(fill="both", expand=True)
        
        # Create modern navigation bar
        self.create_fluent_navigation_bar(main_container, username, user_email)
        
        # Content frame with Microsoft spacing
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=24, pady=(16, 24))
        
        # Create modern dual panel layout
        self.create_fluent_dual_panel(content_frame)
        
        # Smooth entrance animation
        self.animate_page_entrance(content_frame)
    
    def animate_page_entrance(self, content_frame):
        """Microsoft-style page entrance animation"""
        # Create overlay for fade-in effect
        overlay = ctk.CTkFrame(content_frame, fg_color=MS_SURFACE)
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        def fade_step(step=0):
            if step <= 15:
                progress = step / 15
                opacity = int((1 - progress) * 255)
                if step == 15:
                    overlay.destroy()
                else:
                    # Simulate fade by adjusting color opacity
                    self.parent.after(30, lambda: fade_step(step + 1))
        
        self.parent.after(100, fade_step)  # Slight delay for smoother effect
    
    def create_fluent_navigation_bar(self, parent, username, user_email):
        """Modern Microsoft-style navigation bar"""
        nav_frame = ctk.CTkFrame(
            parent,
            fg_color=MS_WHITE,
            corner_radius=0,
            height=64,
            border_width=1,
            border_color=MS_BORDER
        )
        nav_frame.pack(fill="x", side="top")
        nav_frame.pack_propagate(False)
        
        # Left side - Modern logo and title
        left_nav = ctk.CTkFrame(nav_frame, fg_color="transparent")
        left_nav.pack(side="left", fill="y", padx=24, pady=12)
        
        # Modern logo with perfect centering and modern lock icon
        logo_frame = ctk.CTkFrame(
            left_nav,
            width=52,
            height=52,
            corner_radius=16,
            fg_color=MS_PRIMARY
        )
        logo_frame.pack(side="left", padx=(0, 16))
        logo_frame.pack_propagate(False)
        ctk.CTkLabel(
            logo_frame,
            text="🔒",
            font=ctk.CTkFont(size=32),
            text_color=MS_WHITE
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Modern title with Microsoft typography
        title_frame = ctk.CTkFrame(left_nav, fg_color="transparent")
        title_frame.pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text="Secure Vault",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=MS_TEXT_PRIMARY
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="File Encryption Platform",
            font=ctk.CTkFont(size=11),
            text_color=MS_TEXT_TERTIARY
        ).pack(anchor="w")
        
        # Right side - User info and modern buttons
        right_nav = ctk.CTkFrame(nav_frame, fg_color="transparent")
        right_nav.pack(side="right", fill="y", padx=24, pady=12)
        
        # Modern user info card
        user_card = self.create_fluent_card(right_nav, fg_color=MS_SURFACE_SECONDARY, corner_radius=6)
        user_card.pack(side="right", padx=(16, 0))
        
        user_content = ctk.CTkFrame(user_card, fg_color="transparent")
        user_content.pack(padx=12, pady=8)
        
        ctk.CTkLabel(
            user_content,
            text=f"Welcome, {username}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=MS_TEXT_PRIMARY
        ).pack(anchor="e")
        
        ctk.CTkLabel(
            user_content,
            text=user_email,
            font=ctk.CTkFont(size=10),
            text_color=MS_TEXT_SECONDARY
        ).pack(anchor="e")
        
        # Modern navigation buttons
        nav_buttons = ctk.CTkFrame(right_nav, fg_color="transparent")
        nav_buttons.pack(side="right", padx=(0, 16))
        
        home_btn = self.create_fluent_button(
            nav_buttons,
            "🏠 Home",
            command=self.show_home_callback,
            style="secondary",
            width=90
        )
        home_btn.pack(side="right", padx=4)
        
        profile_btn = self.create_fluent_button(
            nav_buttons,
            "👤 Profile",
            command=self.main_app.show_profile if self.main_app else None,
            style="secondary",
            width=90
        )
        profile_btn.pack(side="right", padx=4)
        
        logout_btn = self.create_fluent_button(
            nav_buttons,
            "🚪 Logout",
            command=self.main_app.show_login if self.main_app else None,
            style="primary",
            width=90
        )
        logout_btn.pack(side="right", padx=4)
    
    def create_fluent_dual_panel(self, parent):
        """Modern dual panel layout with Microsoft design"""
        dual_container = ctk.CTkFrame(parent, fg_color="transparent")
        dual_container.pack(fill="both", expand=True)
        
        # Left Panel - Encryption
        self.create_encryption_panel_fluent(dual_container)
        
        # Modern separator
        separator = ctk.CTkFrame(dual_container, width=1, fg_color=MS_BORDER)
        separator.pack(side="left", fill="y", padx=16)
        
        # Right Panel - Decryption
        self.create_decryption_panel_fluent(dual_container)
    
    def create_encryption_panel_fluent(self, parent):
        """Microsoft Fluent Design encryption panel"""
        encrypt_frame = self.create_fluent_card(parent, corner_radius=12)
        encrypt_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        # Modern header with Microsoft styling
        header = ctk.CTkFrame(encrypt_frame, fg_color=MS_SURFACE, corner_radius=8)
        header.pack(fill="x", padx=20, pady=(20, 0))
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=16, pady=16)
        
        # Icon with modern styling
        icon_frame = ctk.CTkFrame(header_content, width=48, height=48, corner_radius=12, fg_color=MS_PRIMARY)
        icon_frame.pack(side="left", padx=(0, 16))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text="🔒",
            font=ctk.CTkFont(size=22),
            text_color=MS_WHITE
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Title section
        title_section = ctk.CTkFrame(header_content, fg_color="transparent")
        title_section.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            title_section,
            text="File Encryption",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=MS_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_section,
            text="Protect your files with enterprise-grade encryption",
            font=ctk.CTkFont(size=12),
            text_color=MS_TEXT_SECONDARY,
            anchor="w"
        ).pack(anchor="w", pady=(4, 0))
        
        # Content area with modern styling
        content_area = ctk.CTkFrame(encrypt_frame, fg_color="transparent")
        content_area.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Modern upload area
        upload_card = self.create_fluent_card(content_area, fg_color=MS_SURFACE_SECONDARY, corner_radius=12)
        upload_card.pack(fill="x", pady=(0, 16))
        
        # Drop zone with modern design
        drop_zone = ctk.CTkFrame(upload_card, fg_color="transparent")
        drop_zone.pack(fill="x", padx=24, pady=24)
        
        # Visual elements
        icon_large = ctk.CTkLabel(
            drop_zone,
            text="📁",
            font=ctk.CTkFont(size=48),
            text_color=MS_PRIMARY
        )
        icon_large.pack(pady=(0, 16))
        
        ctk.CTkLabel(
            drop_zone,
            text="Select Files to Encrypt",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=MS_TEXT_PRIMARY
        ).pack(pady=(0, 8))
        
        ctk.CTkLabel(
            drop_zone,
            text="Choose files from your computer to secure with password encryption",
            font=ctk.CTkFont(size=12),
            text_color=MS_TEXT_SECONDARY
        ).pack(pady=(0, 24))
        
        # Modern upload button
        upload_btn = self.create_fluent_button(
            drop_zone,
            "🔗 Select Files to Encrypt",
            command=self.upload_and_encrypt_file,
            style="primary",
            width=240,
            height=40
        )
        upload_btn.pack()
        
        # Instructions with modern card design
        instructions_card = self.create_fluent_card(content_area, corner_radius=8)
        instructions_card.pack(fill="x")
        
        instructions_content = ctk.CTkFrame(instructions_card, fg_color="transparent")
        instructions_content.pack(fill="x", padx=20, pady=16)
        
        ctk.CTkLabel(
            instructions_content,
            text="How It Works",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=MS_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w", pady=(0, 12))
        
        steps = [
            "Select files from your device",
            "Set a secure encryption password", 
            "Files are encrypted and stored safely",
            "Access files anytime with your password"
        ]
        
        for i, step in enumerate(steps, 1):
            step_frame = ctk.CTkFrame(instructions_content, fg_color="transparent")
            step_frame.pack(fill="x", pady=2)
            
            # Step number with modern styling
            number_frame = ctk.CTkFrame(step_frame, width=20, height=20, corner_radius=10, fg_color=MS_PRIMARY)
            number_frame.pack(side="left", padx=(0, 12))
            number_frame.pack_propagate(False)
            
            ctk.CTkLabel(
                number_frame,
                text=str(i),
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=MS_WHITE
            ).place(relx=0.5, rely=0.5, anchor="center")
            
            ctk.CTkLabel(
                step_frame,
                text=step,
                font=ctk.CTkFont(size=11),
                text_color=MS_TEXT_SECONDARY,
                anchor="w"
            ).pack(side="left", fill="x", expand=True)
    
    def create_decryption_panel_fluent(self, parent):
        """Microsoft Fluent Design decryption panel"""
        decrypt_frame = self.create_fluent_card(parent, corner_radius=12)
        decrypt_frame.pack(side="left", fill="both", expand=True, padx=(8, 0))
        
        # Modern header
        header = ctk.CTkFrame(decrypt_frame, fg_color=MS_SURFACE, corner_radius=8)
        header.pack(fill="x", padx=20, pady=(20, 0))
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=16, pady=16)
        
        # Icon
        icon_frame = ctk.CTkFrame(header_content, width=48, height=48, corner_radius=12, fg_color=MS_SUCCESS)
        icon_frame.pack(side="left", padx=(0, 16))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text="🔓",
            font=ctk.CTkFont(size=22),
            text_color=MS_WHITE
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Title section
        title_section = ctk.CTkFrame(header_content, fg_color="transparent")
        title_section.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            title_section,
            text="File Management",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=MS_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_section,
            text="Access and manage your encrypted files",
            font=ctk.CTkFont(size=12),
            text_color=MS_TEXT_SECONDARY,
            anchor="w"
        ).pack(anchor="w", pady=(4, 0))
        
        # Modern search bar
        search_frame = ctk.CTkFrame(decrypt_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(16, 0))
        
        search_container = ctk.CTkFrame(search_frame, fg_color=MS_SURFACE_SECONDARY, corner_radius=8, height=40)
        search_container.pack(fill="x")
        search_container.pack_propagate(False)
        
        search_content = ctk.CTkFrame(search_container, fg_color="transparent")
        search_content.pack(fill="both", expand=True, padx=12, pady=8)
        
        search_entry = ctk.CTkEntry(
            search_content,
            textvariable=self.search_var,
            placeholder_text="Search files...",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            text_color=MS_TEXT_PRIMARY,
            border_width=0,
            height=24
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        search_btn = self.create_fluent_button(
            search_content,
            "🔍",
            command=self.search_files,
            style="secondary",
            width=30,
            height=24
        )
        search_btn.pack(side="right")
        
        # Content area
        content_area = ctk.CTkFrame(decrypt_frame, fg_color="transparent")
        content_area.pack(fill="both", expand=True, padx=20, pady=16)
        
        # Action bar
        action_bar = ctk.CTkFrame(content_area, fg_color="transparent")
        action_bar.pack(fill="x", pady=(0, 16))
        
        refresh_btn = self.create_fluent_button(
            action_bar,
            "🔄 Refresh",
            command=self.refresh_files,
            style="secondary",
            width=100
        )
        refresh_btn.pack(side="right")
        
        # Files list with modern styling
        self.files_frame = ctk.CTkScrollableFrame(
            content_area,
            fg_color=MS_SURFACE,
            corner_radius=8,
            border_width=1,
            border_color=MS_BORDER,
            label_text="Your Encrypted Files",
            label_font=ctk.CTkFont(size=12, weight="bold"),
            label_text_color=MS_TEXT_PRIMARY
        )
        self.files_frame.pack(fill="both", expand=True)
        
        # Load files
        self.refresh_files()
    
    def destroy_active_tooltip(self):
        if self.active_tooltip is not None:
            try:
                self.active_tooltip.destroy()
            except Exception:
                pass
            self.active_tooltip = None

    def create_modern_file_item(self, file_doc):
        """Create modern Microsoft-style file item"""
        file_card = self.create_fluent_card(self.files_frame, corner_radius=8)
        file_card.pack(fill="x", padx=12, pady=2)
        file_card.configure(height=44)
        # Use grid for precise alignment
        content = ctk.CTkFrame(file_card, fg_color="transparent", height=44)
        content.pack(fill="x", padx=8, pady=2)
        content.pack_propagate(False)
        content.grid_columnconfigure(1, weight=1)
        # File icon
        icon_frame = ctk.CTkFrame(content, width=24, height=24, corner_radius=6, fg_color=MS_PRIMARY)
        icon_frame.grid(row=0, column=0, padx=(0, 8), pady=0, sticky="n")
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(
            icon_frame,
            text="📄",
            font=ctk.CTkFont(size=12),
            text_color=MS_WHITE
        ).place(relx=0.5, rely=0.5, anchor="center")
        # File details
        details = ctk.CTkFrame(content, fg_color="transparent", width=240, height=44)
        details.grid(row=0, column=1, sticky="nsw")
        details.pack_propagate(False)
        filename = file_doc.get('filename', 'Unknown File')
        max_len = 32
        display_name = (filename[:max_len] + '...') if len(filename) > max_len else filename
        filename_label = ctk.CTkLabel(
            details,
            text=display_name,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=MS_TEXT_PRIMARY,
            anchor="w",
            width=220
        )
        filename_label.pack(anchor="w")
        # Metadata
        upload_date = file_doc.get('upload_date', 'Unknown')
        file_size = file_doc.get('size_bytes', 0)
        size_kb = round(file_size / 1024, 1) if file_size > 0 else 0
        ctk.CTkLabel(
            details,
            text=f"{size_kb} KB • {str(upload_date)[:19] if upload_date else 'Unknown date'}",
            font=ctk.CTkFont(size=9),
            text_color=MS_TEXT_TERTIARY,
            anchor="w"
        ).pack(anchor="w", pady=(0, 0))
        # Actions
        actions = ctk.CTkFrame(content, fg_color="transparent", width=180, height=44)
        actions.grid(row=0, column=2, padx=(8, 0), pady=0, sticky="nse")
        actions.pack_propagate(False)
        decrypt_btn = self.create_fluent_button(
            actions,
            "🔓 Decrypt",
            command=lambda: self.decrypt_and_view_file(file_doc),
            style="primary",
            width=80,
            height=28
        )
        decrypt_btn.pack(side="left", padx=(0, 8), pady=0)
        delete_btn = self.create_fluent_button(
            actions,
            "Delete",
            command=lambda: self.delete_file(file_doc),
            style="secondary",
            width=80,
            height=28
        )
        delete_btn.pack(side="left", pady=0)
    
    def show_modern_skeleton_loading(self):
        self.destroy_active_tooltip()
        for widget in self.files_frame.winfo_children():
            widget.destroy()
        
        for _ in range(4):
            skeleton = self.create_fluent_card(self.files_frame, fg_color=MS_SURFACE_SECONDARY)
            skeleton.pack(fill="x", padx=12, pady=6)
            
            content = ctk.CTkFrame(skeleton, fg_color="transparent")
            content.pack(fill="x", padx=16, pady=12)
            
            # Skeleton elements with shimmer effect
            icon_skeleton = ctk.CTkFrame(content, width=32, height=32, corner_radius=8, fg_color=MS_SURFACE_TERTIARY)
            icon_skeleton.pack(side="left", padx=(0, 12))
            icon_skeleton.pack_propagate(False)
            
            details_skeleton = ctk.CTkFrame(content, fg_color="transparent")
            details_skeleton.pack(side="left", fill="both", expand=True)
            
            name_bar = ctk.CTkFrame(details_skeleton, width=200, height=14, corner_radius=4, fg_color=MS_SURFACE_TERTIARY)
            name_bar.pack(anchor="w", pady=(0, 4))
            name_bar.pack_propagate(False)
            
            meta_bar = ctk.CTkFrame(details_skeleton, width=140, height=10, corner_radius=4, fg_color=MS_SURFACE_TERTIARY)
            meta_bar.pack(anchor="w")
            meta_bar.pack_propagate(False)
    
    # Keep existing methods but update UI calls
    def search_files(self):
        query = self.search_var.get().strip().lower()
        if not self.db_manager:
            return
        
        username = self.user_info.get('username', 'User')
        files = self.db_manager.get_user_files(username)
        
        if query:
            filtered = [f for f in files if query in f.get('filename', '').lower()]
        else:
            filtered = files
        
        self.current_files = filtered
        self.display_modern_files(filtered)
    
    def upload_and_encrypt_file(self):
        if not self.main_app:
            return
        
        username = self.user_info.get('username', 'User')
        self.main_app.upload_file(username, self.parent)
    
    def refresh_files(self):
        if not self.db_manager:
            return
        
        self.show_modern_skeleton_loading()
        
        def load_files():
            time.sleep(0.8)  # Reduced loading time for better UX
            username = self.user_info.get('username', 'User')
            files = self.db_manager.get_user_files(username)
            self.current_files = files
            self.parent.after(0, lambda: self.display_modern_files(files))
        
        threading.Thread(target=load_files, daemon=True).start()
    
    def display_modern_files(self, files):
        self.destroy_active_tooltip()
        for widget in self.files_frame.winfo_children():
            widget.destroy()
        
        if not files:
            # Modern empty state
            empty_card = self.create_fluent_card(self.files_frame, fg_color=MS_SURFACE_SECONDARY)
            empty_card.pack(fill="x", padx=12, pady=16)
            
            empty_content = ctk.CTkFrame(empty_card, fg_color="transparent")
            empty_content.pack(padx=24, pady=32)
            
            ctk.CTkLabel(
                empty_content,
                text="📁",
                font=ctk.CTkFont(size=36),
                text_color=MS_TEXT_TERTIARY
            ).pack(pady=(0, 12))
            
            ctk.CTkLabel(
                empty_content,
                text="No Encrypted Files Yet",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=MS_TEXT_PRIMARY
            ).pack()
            
            ctk.CTkLabel(
                empty_content,
                text="Upload and encrypt your first file using the encryption panel",
                font=ctk.CTkFont(size=12),
                text_color=MS_TEXT_SECONDARY
            ).pack(pady=(4, 0))
        else:
            for file_doc in files:
                self.create_modern_file_item(file_doc)
    
    def decrypt_and_view_file(self, file_doc):
        if not self.main_app:
            return
        
        self.main_app.download_file(file_doc)
    
    def delete_file(self, file_doc):
        if not self.main_app:
            return
        
        try:
            success = self.db_manager.delete_file(self.user_info['username'], file_doc['filename'])
            if success:
                if self.main_app:
                    self.main_app.show_notification(
                        f"'{file_doc.get('filename', 'File')}' deleted successfully",
                        type="success"
                    )
                self.refresh_files()
            else:
                if self.main_app:
                    self.main_app.show_notification(
                        f"Could not delete '{file_doc.get('filename', 'File')}'",
                        type="error"
                    )
        except Exception as e:
            if self.main_app:
                self.main_app.show_notification(f"Failed to delete file: {str(e)}", type="error")
 