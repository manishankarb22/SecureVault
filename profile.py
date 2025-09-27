import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import io, base64, os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from security import SecurityManager
from cryptography.fernet import Fernet

# Microsoft Fluent Design - Black and White Theme Colors
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

# Set modern theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ProfilePage:
    def __init__(self, parent, db, user, refresh_home, main_app=None):
        self.parent, self.db, self.user, self.refresh_home = parent, db, user, refresh_home
        self.main_app = main_app
        
        # Animation properties
        self.hover_animations = {}
        self.card_animations = {}
        
        self.build_ui()
    
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
        elif style == "success":
            fg_color = MS_SUCCESS
            hover_color = MS_PRIMARY_HOVER
            text_color = MS_WHITE
        elif style == "warning":
            fg_color = MS_WARNING
            hover_color = MS_PRIMARY_HOVER
            text_color = MS_WHITE
        elif style == "error":
            fg_color = MS_ERROR
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
            corner_radius=4,
            border_width=1,
            border_color=MS_BORDER,
            width=width,
            height=height
        )
        
        return button
    
    def create_fluent_card(self, parent, fg_color=MS_WHITE, corner_radius=8, border_width=1):
        """Create Microsoft Fluent Design card with subtle shadow effect"""
        card = ctk.CTkFrame(
            parent,
            fg_color=fg_color,
            corner_radius=corner_radius,
            border_width=border_width,
            border_color=MS_BORDER
        )
        return card

    def build_ui(self):
        # Clear existing widgets
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Main container with Microsoft background
        main_container = ctk.CTkFrame(self.parent, fg_color=MS_SURFACE, corner_radius=0)
        main_container.pack(fill="both", expand=True)
        
        # Create modern navigation bar
        self.create_fluent_navigation_bar(main_container)
        
        # Content frame with Microsoft spacing
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=24, pady=(16, 24))
        
        # Create modern dual panel layout
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure((0,1), weight=1)
        
        # Left panel - User Profile Card
        self.build_fluent_user_card(content_frame)
        
        # Right panel - Storage Overview
        self.build_fluent_storage_panel(content_frame)
    
    def create_fluent_navigation_bar(self, parent):
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
        
        # Modern logo with subtle animation
        logo_frame = ctk.CTkFrame(
            left_nav,
            width=40,
            height=40,
            corner_radius=8,
            fg_color=MS_PRIMARY
        )
        logo_frame.pack(side="left", padx=(0, 16))
        logo_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            logo_frame,
            text="👤",
            font=ctk.CTkFont(size=18),
            text_color=MS_WHITE
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Modern title with Microsoft typography
        title_frame = ctk.CTkFrame(left_nav, fg_color="transparent")
        title_frame.pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text="Profile Settings",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=MS_TEXT_PRIMARY
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Manage your account and preferences",
            font=ctk.CTkFont(size=11),
            text_color=MS_TEXT_TERTIARY
        ).pack(anchor="w")
        
        # Right side - Navigation buttons
        right_nav = ctk.CTkFrame(nav_frame, fg_color="transparent")
        right_nav.pack(side="right", fill="y", padx=24, pady=12)
        
        home_btn = self.create_fluent_button(
            right_nav,
            "🏠 Home",
            command=self.refresh_home,
            style="primary",
            width=100,
            height=36
        )
        home_btn.pack(side="right")

    def build_fluent_user_card(self, parent):
        """Modern Microsoft-style user profile card"""
        # Left panel container (scrollable)
        left_panel_scroll = ctk.CTkScrollableFrame(parent, fg_color=MS_SURFACE, corner_radius=12)
        left_panel_scroll.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        left_panel = left_panel_scroll
        
        # Header section
        header = ctk.CTkFrame(left_panel, fg_color=MS_SURFACE, corner_radius=8)
        header.pack(fill="x", padx=20, pady=(20, 0))
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=16, pady=16)
        
        # Profile header with icon
        icon_frame = ctk.CTkFrame(header_content, width=48, height=48, corner_radius=12, fg_color=MS_PRIMARY)
        icon_frame.pack(side="left", padx=(0, 16))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text="👤",
            font=ctk.CTkFont(size=22),
            text_color=MS_WHITE
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Title section
        title_section = ctk.CTkFrame(header_content, fg_color="transparent")
        title_section.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            title_section,
            text="User Profile",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=MS_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_section,
            text="Manage your personal information and settings",
            font=ctk.CTkFont(size=12),
            text_color=MS_TEXT_SECONDARY,
            anchor="w"
        ).pack(anchor="w", pady=(4, 0))
        
        # Main content area
        content_area = ctk.CTkFrame(left_panel, fg_color="transparent")
        content_area.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Avatar section with modern styling
        avatar_section = self.create_fluent_card(content_area, fg_color=MS_SURFACE_SECONDARY, corner_radius=12)
        avatar_section.pack(fill="x", pady=(0, 16))
        
        avatar_content = ctk.CTkFrame(avatar_section, fg_color="transparent")
        avatar_content.pack(pady=20)
        
        # Avatar display
        avatar_img = self.load_avatar()
        avatar_label = ctk.CTkLabel(avatar_content, image=avatar_img, text="")
        avatar_label.pack(pady=(0, 12))
        
        # User info with modern typography
        stats = self.db.user_storage_stats(self.user['username'])
        
        display_name = f"{self.user.get('first_name', '')} {self.user.get('last_name', '')}".strip()
        if not display_name:
            display_name = self.user['username']
        
        ctk.CTkLabel(
            avatar_content,
            text=display_name,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=MS_TEXT_PRIMARY
        ).pack()
        
        ctk.CTkLabel(
            avatar_content,
            text=f"@{self.user['username']}",
            font=ctk.CTkFont(size=12),
            text_color=MS_TEXT_SECONDARY
        ).pack(pady=(2, 0))
        
        ctk.CTkLabel(
            avatar_content,
            text=self.user['email'],
            font=ctk.CTkFont(size=11),
            text_color=MS_TEXT_TERTIARY
        ).pack(pady=(4, 0))
        
        # Quick stats card
        stats_card = self.create_fluent_card(content_area, fg_color=MS_SURFACE_SECONDARY, corner_radius=8)
        stats_card.pack(fill="x", pady=(0, 16))
        
        stats_content = ctk.CTkFrame(stats_card, fg_color="transparent")
        stats_content.pack(fill="x", padx=16, pady=12)
        
        ctk.CTkLabel(
            stats_content,
            text="Account Statistics",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=MS_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        # Stats grid
        stats_grid = ctk.CTkFrame(stats_content, fg_color="transparent")
        stats_grid.pack(fill="x")
        
        # Files count
        files_frame = ctk.CTkFrame(stats_grid, fg_color="transparent")
        files_frame.pack(side="left", expand=True, fill="x")
        
        ctk.CTkLabel(
            files_frame,
            text="📁",
            font=ctk.CTkFont(size=16),
            text_color=MS_PRIMARY
        ).pack()
        
        ctk.CTkLabel(
            files_frame,
            text=str(stats['file_count']),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=MS_TEXT_PRIMARY
        ).pack()
        
        ctk.CTkLabel(
            files_frame,
            text="Files",
            font=ctk.CTkFont(size=10),
            text_color=MS_TEXT_TERTIARY
        ).pack()
        
        # Storage usage
        storage_frame = ctk.CTkFrame(stats_grid, fg_color="transparent")
        storage_frame.pack(side="right", expand=True, fill="x")
        
        ctk.CTkLabel(
            storage_frame,
            text="💾",
            font=ctk.CTkFont(size=16),
            text_color=MS_PRIMARY
        ).pack()
        
        ctk.CTkLabel(
            storage_frame,
            text=f"{stats['total_bytes']/1_048_576:.1f} MB",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=MS_TEXT_PRIMARY
        ).pack()
        
        ctk.CTkLabel(
            storage_frame,
            text="Used",
            font=ctk.CTkFont(size=10),
            text_color=MS_TEXT_TERTIARY
        ).pack()
        
        # FIXED Action buttons with modern styling - Account Actions Section
        actions_card = self.create_fluent_card(content_area, corner_radius=8)
        actions_card.pack(fill="x")
        
        actions_content = ctk.CTkFrame(actions_card, fg_color="transparent")
        actions_content.pack(fill="x", padx=16, pady=16)
        
        # Account Actions Header
        ctk.CTkLabel(
            actions_content,
            text="Account Actions",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=MS_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w", pady=(0, 12))
        
        # Action buttons
        buttons = [
            ("📸 Change Avatar", self.change_avatar, "secondary"),
            ("✏️ Edit Profile", self.open_edit_profile_page, "primary"),
            ("🔒 Change Password", self.open_change_password_page, "warning"),
            ("🚪 Logout", self.logout, "error")
        ]
        
        for text, command, style in buttons:
            btn = self.create_fluent_button(
                actions_content,
                text,
                command=command,
                style=style,
                width=200,
                height=36
            )
            btn.pack(fill="x", pady=2)

    def build_fluent_storage_panel(self, parent):
        """Modern Microsoft-style storage overview panel"""
        # Right panel container
        right_panel = self.create_fluent_card(parent, corner_radius=12)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        
        stats = self.db.user_storage_stats(self.user['username'])
        
        # Header section
        header = ctk.CTkFrame(right_panel, fg_color=MS_SURFACE, corner_radius=8)
        header.pack(fill="x", padx=20, pady=(20, 0))
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=16, pady=16)
        
        # Storage header with icon
        icon_frame = ctk.CTkFrame(header_content, width=48, height=48, corner_radius=12, fg_color=MS_SUCCESS)
        icon_frame.pack(side="left", padx=(0, 16))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text="💾",
            font=ctk.CTkFont(size=22),
            text_color=MS_WHITE
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Title section
        title_section = ctk.CTkFrame(header_content, fg_color="transparent")
        title_section.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            title_section,
            text="Storage Overview",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=MS_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_section,
            text="Monitor your file storage and usage",
            font=ctk.CTkFont(size=12),
            text_color=MS_TEXT_SECONDARY,
            anchor="w"
        ).pack(anchor="w", pady=(4, 0))
        
        # Main content area
        content_area = ctk.CTkFrame(right_panel, fg_color="transparent")
        content_area.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Storage usage card
        usage_card = self.create_fluent_card(content_area, fg_color=MS_SURFACE_SECONDARY, corner_radius=12)
        usage_card.pack(fill="x", pady=(0, 16))
        
        usage_content = ctk.CTkFrame(usage_card, fg_color="transparent")
        usage_content.pack(fill="x", padx=20, pady=20)
        
        used_gb = stats['total_bytes'] / 1_073_741_824
        
        ctk.CTkLabel(
            usage_content,
            text="Storage Usage",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=MS_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w", pady=(0, 12))
        
        # Progress bar with modern styling
        progress_frame = ctk.CTkFrame(usage_content, fg_color="transparent")
        progress_frame.pack(fill="x", pady=(0, 12))
        
        # Determine color based on usage
        if used_gb < 3:
            progress_color = MS_SUCCESS
        elif used_gb < 4.5:
            progress_color = MS_WARNING
        else:
            progress_color = MS_ERROR
        
        progress_bar = ctk.CTkProgressBar(
            progress_frame,
            width=280,
            height=16,
            progress_color=progress_color,
            fg_color=MS_SURFACE_TERTIARY,
            corner_radius=8
        )
        progress_bar.set(min(used_gb/5, 1))
        progress_bar.pack()
        
        # Usage text
        ctk.CTkLabel(
            usage_content,
            text=f"{used_gb:.2f} GB of 5.00 GB used ({(used_gb/5)*100:.1f}%)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=MS_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")
        
        # File types breakdown
        if stats['by_ext']:
            breakdown_card = self.create_fluent_card(content_area, corner_radius=8)
            breakdown_card.pack(fill="both", expand=True)
            
            breakdown_content = ctk.CTkFrame(breakdown_card, fg_color="transparent")
            breakdown_content.pack(fill="both", expand=True, padx=16, pady=16)
            
            ctk.CTkLabel(
                breakdown_content,
                text="File Types Breakdown",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=MS_TEXT_PRIMARY,
                anchor="w"
            ).pack(anchor="w", pady=(0, 12))
            
            # Scrollable file types list
            types_frame = ctk.CTkScrollableFrame(
                breakdown_content,
                height=200,
                fg_color=MS_SURFACE,
                corner_radius=6,
                border_width=1,
                border_color=MS_BORDER
            )
            types_frame.pack(fill="both", expand=True)
            
            for ext, d in sorted(stats['by_ext'].items(), key=lambda x: x[1]['bytes'], reverse=True):
                mb = d['bytes'] / 1_048_576
                percentage = (d['bytes'] / stats['total_bytes']) * 100 if stats['total_bytes'] > 0 else 0
                
                # File type row
                row_card = self.create_fluent_card(types_frame, fg_color=MS_SURFACE_SECONDARY, corner_radius=6, border_width=0)
                row_card.pack(fill="x", padx=4, pady=2)
                
                row_content = ctk.CTkFrame(row_card, fg_color="transparent")
                row_content.pack(fill="x", padx=12, pady=8)
                
                # File type info
                info_frame = ctk.CTkFrame(row_content, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True)
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"{ext.upper()}",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=MS_TEXT_PRIMARY,
                    anchor="w"
                ).pack(anchor="w")
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"{d['count']} files • {mb:.1f} MB",
                    font=ctk.CTkFont(size=9),
                    text_color=MS_TEXT_SECONDARY,
                    anchor="w"
                ).pack(anchor="w")
                
                # Percentage
                ctk.CTkLabel(
                    row_content,
                    text=f"{percentage:.1f}%",
                    font=ctk.CTkFont(size=10, weight="bold"),
                    text_color=MS_TEXT_PRIMARY
                ).pack(side="right")

    def load_avatar(self, data=None):
        """Load and decrypt the encrypted avatar from MongoDB users collection"""
        avatar_enc = self.user.get('avatar_encrypted')
        if avatar_enc:
            try:
                key = base64.urlsafe_b64encode(self.user['username'].ljust(32, '0').encode()[:32])
                fernet = Fernet(key)
                encrypted_bytes = base64.b64decode(avatar_enc)
                img_bytes = fernet.decrypt(encrypted_bytes)
                img = Image.open(io.BytesIO(img_bytes)).resize((80, 80))
                return ctk.CTkImage(img, size=(80, 80))
            except Exception:
                pass
        
        # Fallback to default avatar
        img = Image.new("RGB", (80, 80), color=MS_SURFACE_TERTIARY)
        return ctk.CTkImage(img, size=(80, 80))

    def crop_center_square(self, img):
        """Crop image to center square"""
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim
        return img.crop((left, top, right, bottom))

    def change_avatar(self):
        """Change user avatar with modern file dialog"""
        path = filedialog.askopenfilename(
            title="Choose Avatar",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
        )
        if not path:
            return

        try:
            with open(path, "rb") as f:
                img_bytes = f.read()
            
            img = Image.open(io.BytesIO(img_bytes))
            img = self.crop_center_square(img)
            
            output = io.BytesIO()
            img.save(output, format="PNG")
            cropped_bytes = output.getvalue()
            
            # Encrypt avatar
            key = base64.urlsafe_b64encode(self.user['username'].ljust(32, '0').encode()[:32])
            fernet = Fernet(key)
            encrypted_img = fernet.encrypt(cropped_bytes)
            b64_encrypted = base64.b64encode(encrypted_img).decode()
            
            # Store encrypted avatar
            self.db.users_collection.update_one(
                {'username': self.user['username']}, 
                {'$set': {'avatar_encrypted': b64_encrypted}}
            )
            
            if self.main_app:
                self.main_app.show_notification(
                    "Profile picture updated and encrypted successfully!",
                    type="success"
                )
            
            self.refresh_home(self.db.get_user_profile(self.user['username']))
            
        except Exception as e:
            if self.main_app:
                self.main_app.show_notification(
                    f"Failed to update avatar: {e}",
                    type="error"
                )

    def logout(self):
        """Logout user"""
        if self.main_app:
            self.main_app.show_notification(
                "You have been logged out successfully!",
                type="info"
            )
        self.refresh_home()

    def open_edit_profile_page(self):
        """Open edit profile page"""
        EditProfilePage(self.parent, self.db, self.user, self.refresh_home, main_app=self.main_app)

    def open_change_password_page(self):
        """Open change password page"""
        ChangePasswordPage(self.parent, self.db, self.user, self.refresh_home, main_app=self.main_app)


# Modern Microsoft Fluent Design Edit Profile Page
class EditProfilePage:
    def __init__(self, parent, db, user, refresh_home, main_app=None):
        self.parent = parent
        self.db = db
        self.user = user
        self.refresh_home = refresh_home
        self.main_app = main_app
        self.create_ui()
    
    def create_fluent_button(self, parent, text, command=None, style="primary", width=None, height=32):
        """Create Microsoft Fluent Design button"""
        if style == "primary":
            fg_color = MS_PRIMARY
            hover_color = MS_PRIMARY_HOVER
            text_color = MS_WHITE
        elif style == "success":
            fg_color = MS_SUCCESS
            hover_color = MS_PRIMARY_HOVER
            text_color = MS_WHITE
        elif style == "error":
            fg_color = MS_ERROR
            hover_color = MS_PRIMARY_HOVER
            text_color = MS_WHITE
        else:
            fg_color = MS_SURFACE_SECONDARY
            hover_color = MS_SURFACE_TERTIARY
            text_color = MS_TEXT_PRIMARY
        
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=text_color,
            font=ctk.CTkFont(size=13, weight="normal"),
            corner_radius=4,
            border_width=1,
            border_color=MS_BORDER,
            width=width,
            height=height
        )
        return button
    
    def create_fluent_card(self, parent, fg_color=MS_WHITE, corner_radius=8, border_width=1):
        """Create Microsoft Fluent Design card"""
        card = ctk.CTkFrame(
            parent,
            fg_color=fg_color,
            corner_radius=corner_radius,
            border_width=border_width,
            border_color=MS_BORDER
        )
        return card

    def create_ui(self):
        # Clear all existing widgets
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Main container
        main_container = ctk.CTkFrame(self.parent, fg_color=MS_SURFACE, corner_radius=0)
        main_container.pack(fill="both", expand=True)
        
        # Navigation bar
        self.create_navigation_bar(main_container)
        
        # Content area
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=24, pady=24)
        
        # Main card
        main_card = self.create_fluent_card(content_frame, corner_radius=12)
        main_card.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header_section(main_card)
        
        # Form section
        self.create_form_section(main_card)
    
    def create_navigation_bar(self, parent):
        """Create navigation bar"""
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
        
        # Left side navigation
        left_nav = ctk.CTkFrame(nav_frame, fg_color="transparent")
        left_nav.pack(side="left", fill="y", padx=24, pady=12)
        
        # Home button
        home_btn = self.create_fluent_button(
            left_nav,
            "🏠 Home",
            command=self.go_home,
            style="primary",
            width=100,
            height=36
        )
        home_btn.pack(side="left", padx=(0, 12))
        
        # Profile button
        profile_btn = self.create_fluent_button(
            left_nav,
            "👤 Profile",
            command=self.go_back_to_profile,
            style="secondary",
            width=100,
            height=36
        )
        profile_btn.pack(side="left")
        
        # Title
        title_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        title_frame.pack(expand=True)
        
        ctk.CTkLabel(
            title_frame,
            text="✏️ Edit Profile",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=MS_TEXT_PRIMARY
        ).pack(pady=12)
    
    def create_header_section(self, parent):
        """Create header section"""
        header = ctk.CTkFrame(parent, fg_color=MS_SURFACE, corner_radius=8)
        header.pack(fill="x", padx=20, pady=(20, 0))
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=16, pady=16)
        
        # Icon
        icon_frame = ctk.CTkFrame(header_content, width=48, height=48, corner_radius=12, fg_color=MS_PRIMARY)
        icon_frame.pack(side="left", padx=(0, 16))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text="✏️",
            font=ctk.CTkFont(size=22),
            text_color=MS_WHITE
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Title section
        title_section = ctk.CTkFrame(header_content, fg_color="transparent")
        title_section.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            title_section,
            text="Edit Your Profile",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=MS_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_section,
            text="Update your personal information and preferences",
            font=ctk.CTkFont(size=12),
            text_color=MS_TEXT_SECONDARY,
            anchor="w"
        ).pack(anchor="w", pady=(4, 0))
    
    def create_form_section(self, parent):
        """Create form section"""
        # Content area
        content_area = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            scrollbar_button_color=MS_SURFACE_TERTIARY,
            scrollbar_button_hover_color=MS_SURFACE_SECONDARY
        )
        content_area.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form card
        form_card = self.create_fluent_card(content_area, fg_color=MS_SURFACE_SECONDARY, corner_radius=12)
        form_card.pack(fill="x", pady=(0, 20))
        
        form_content = ctk.CTkFrame(form_card, fg_color="transparent")
        form_content.pack(fill="x", padx=24, pady=24)
        
        # Form fields
        self.create_input_field(form_content, "First Name:", "first_name", self.user.get('first_name', ''))
        self.create_input_field(form_content, "Last Name:", "last_name", self.user.get('last_name', ''))
        self.create_input_field(form_content, "Email Address:", "email", self.user.get('email', ''))
        
        # Bio field
        bio_label = ctk.CTkLabel(
            form_content,
            text="Bio (Optional):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=MS_TEXT_PRIMARY,
            anchor="w"
        )
        bio_label.pack(fill="x", pady=(16, 8))
        
        self.bio_textbox = ctk.CTkTextbox(
            form_content,
            height=80,
            fg_color=MS_WHITE,
            text_color=MS_TEXT_PRIMARY,
            border_color=MS_BORDER,
            border_width=1,
            corner_radius=6,
            font=ctk.CTkFont(size=12)
        )
        self.bio_textbox.pack(fill="x", pady=(0, 20))
        
        if self.user.get('bio'):
            self.bio_textbox.insert("1.0", self.user['bio'])
        
        # Buttons section
        buttons_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(16, 0))
        
        # Save button
        save_btn = self.create_fluent_button(
            buttons_frame,
            "💾 Save Changes",
            command=self.save_changes,
            style="success",
            width=160,
            height=40
        )
        save_btn.pack(side="left", padx=(0, 12))
        
        # Cancel button
        cancel_btn = self.create_fluent_button(
            buttons_frame,
            "❌ Cancel",
            command=self.go_back_to_profile,
            style="error",
            width=120,
            height=40
        )
        cancel_btn.pack(side="left")

    def create_input_field(self, parent, label_text, field_name, default_value):
        """Create input field with modern styling"""
        # Label
        label = ctk.CTkLabel(
            parent,
            text=label_text,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=MS_TEXT_PRIMARY,
            anchor="w"
        )
        label.pack(fill="x", pady=(16, 8))
        
        # Entry field
        entry = ctk.CTkEntry(
            parent,
            height=40,
            fg_color=MS_WHITE,
            text_color=MS_TEXT_PRIMARY,
            border_color=MS_BORDER,
            border_width=1,
            corner_radius=6,
            font=ctk.CTkFont(size=12),
            placeholder_text=f"Enter your {label_text.lower().replace(':', '')}"
        )
        entry.pack(fill="x", pady=(0, 8))
        
        if default_value:
            entry.insert(0, default_value)
        
        setattr(self, field_name + "_entry", entry)

    def save_changes(self):
        """Save profile changes"""
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        bio = self.bio_textbox.get("1.0", "end-1c").strip()

        if email and "@" not in email:
            if self.main_app:
                self.main_app.show_notification("Please enter a valid email address!", type="error")
            return

        updates = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'bio': bio
        }

        try:
            result = self.db.users_collection.update_one(
                {'username': self.user['username']},
                {'$set': updates}
            )

            if self.main_app:
                self.main_app.show_notification("Profile updated successfully!", type="success")

            updated_user = self.db.get_user_profile(self.user['username'])
            ProfilePage(self.parent, self.db, updated_user, self.refresh_home, main_app=self.main_app)

        except Exception as e:
            if self.main_app:
                self.main_app.show_notification(f"Failed to update profile: {str(e)}", type="error")

    def go_back_to_profile(self):
        """Go back to profile page"""
        ProfilePage(self.parent, self.db, self.user, self.refresh_home, main_app=self.main_app)

    def go_home(self):
        """Go to home page"""
        self.refresh_home(self.user)


# Modern Microsoft Fluent Design Change Password Page
class ChangePasswordPage:
    def __init__(self, parent, db, user, refresh_home, main_app=None):
        self.parent = parent
        self.db = db
        self.user = user
        self.refresh_home = refresh_home
        self.main_app = main_app
        self.create_ui()
    
    def create_fluent_button(self, parent, text, command=None, style="primary", width=None, height=32):
        """Create Microsoft Fluent Design button"""
        if style == "primary":
            fg_color = MS_PRIMARY
            hover_color = MS_PRIMARY_HOVER
            text_color = MS_WHITE
        elif style == "warning":
            fg_color = MS_WARNING
            hover_color = MS_PRIMARY_HOVER
            text_color = MS_WHITE
        elif style == "error":
            fg_color = MS_ERROR
            hover_color = MS_PRIMARY_HOVER
            text_color = MS_WHITE
        else:
            fg_color = MS_SURFACE_SECONDARY
            hover_color = MS_SURFACE_TERTIARY
            text_color = MS_TEXT_PRIMARY
        
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=text_color,
            font=ctk.CTkFont(size=13, weight="normal"),
            corner_radius=4,
            border_width=1,
            border_color=MS_BORDER,
            width=width,
            height=height
        )
        return button
    
    def create_fluent_card(self, parent, fg_color=MS_WHITE, corner_radius=8, border_width=1):
        """Create Microsoft Fluent Design card"""
        card = ctk.CTkFrame(
            parent,
            fg_color=fg_color,
            corner_radius=corner_radius,
            border_width=border_width,
            border_color=MS_BORDER
        )
        return card

    def create_ui(self):
        # Clear all existing widgets
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Main container
        main_container = ctk.CTkFrame(self.parent, fg_color=MS_SURFACE, corner_radius=0)
        main_container.pack(fill="both", expand=True)
        # Navigation bar
        self.create_navigation_bar(main_container)
        # Content area
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=24, pady=24)
        # Main card (scrollable)
        main_card_scroll = ctk.CTkScrollableFrame(content_frame, fg_color=MS_SURFACE, corner_radius=12)
        main_card_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        main_card = main_card_scroll
        # Header section
        self.create_header_section(main_card)
        # Form section
        self.create_form_section(main_card)
    
    def create_navigation_bar(self, parent):
        """Create navigation bar"""
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
        
        # Left side navigation
        left_nav = ctk.CTkFrame(nav_frame, fg_color="transparent")
        left_nav.pack(side="left", fill="y", padx=24, pady=12)
        
        # Home button
        home_btn = self.create_fluent_button(
            left_nav,
            "🏠 Home",
            command=self.go_home,
            style="primary",
            width=100,
            height=36
        )
        home_btn.pack(side="left", padx=(0, 12))
        
        # Profile button
        profile_btn = self.create_fluent_button(
            left_nav,
            "👤 Profile",
            command=self.go_back_to_profile,
            style="secondary",
            width=100,
            height=36
        )
        profile_btn.pack(side="left")
        
        # Title
        title_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        title_frame.pack(expand=True)
        
        ctk.CTkLabel(
            title_frame,
            text="🔒 Change Password",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=MS_TEXT_PRIMARY
        ).pack(pady=12)
    
    def create_header_section(self, parent):
        """Create header section"""
        header = ctk.CTkFrame(parent, fg_color=MS_SURFACE, corner_radius=8)
        header.pack(fill="x", padx=20, pady=(20, 0))
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=16, pady=16)
        
        # Icon
        icon_frame = ctk.CTkFrame(header_content, width=48, height=48, corner_radius=12, fg_color=MS_WARNING)
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
            text="Change Password",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=MS_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_section,
            text="Update your account password for better security",
            font=ctk.CTkFont(size=12),
            text_color=MS_TEXT_SECONDARY,
            anchor="w"
        ).pack(anchor="w", pady=(4, 0))
    
    def create_form_section(self, parent):
        """Create form section"""
        # Content area
        content_area = ctk.CTkFrame(parent, fg_color="transparent")
        content_area.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Security warning
        warning_card = self.create_fluent_card(content_area, fg_color="#FFF9C4", corner_radius=8)
        warning_card.pack(fill="x", pady=(0, 16))
        
        warning_content = ctk.CTkFrame(warning_card, fg_color="transparent")
        warning_content.pack(fill="x", padx=16, pady=12)
        
        ctk.CTkLabel(
            warning_content,
            text="🛡️ Security Tip: Use a strong password with at least 6 characters including letters and numbers",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#8B5A00",
            wraplength=500
        ).pack()
        
        # Form card
        form_card = self.create_fluent_card(content_area, fg_color=MS_SURFACE_SECONDARY, corner_radius=12)
        form_card.pack(fill="x", pady=(0, 20))
        
        form_content = ctk.CTkFrame(form_card, fg_color="transparent")
        form_content.pack(fill="x", padx=24, pady=24)
        
        # Password fields
        self.create_password_field(form_content, "Current Password:", "current_password")
        self.create_password_field(form_content, "New Password:", "new_password")
        self.create_password_field(form_content, "Confirm New Password:", "confirm_password")
        
        # Buttons section
        buttons_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(24, 0))
        
        # Change password button
        change_btn = self.create_fluent_button(
            buttons_frame,
            "🔒 Change Password",
            command=self.change_password,
            style="warning",
            width=180,
            height=40
        )
        change_btn.pack(side="left", padx=(0, 12))
        
        # Cancel button
        cancel_btn = self.create_fluent_button(
            buttons_frame,
            "❌ Cancel",
            command=self.go_back_to_profile,
            style="error",
            width=120,
            height=40
        )
        cancel_btn.pack(side="left")

    def create_password_field(self, parent, label_text, field_name):
        """Create password field with modern styling"""
        # Label
        label = ctk.CTkLabel(
            parent,
            text=label_text,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=MS_TEXT_PRIMARY,
            anchor="w"
        )
        label.pack(fill="x", pady=(16, 8))
        
        # Password entry field
        entry = ctk.CTkEntry(
            parent,
            height=40,
            fg_color=MS_WHITE,
            text_color=MS_TEXT_PRIMARY,
            border_color=MS_BORDER,
            border_width=1,
            corner_radius=6,
            font=ctk.CTkFont(size=12),
            show="*",
            placeholder_text=f"Enter {label_text.lower()}"
        )
        entry.pack(fill="x", pady=(0, 8))
        
        setattr(self, field_name + "_entry", entry)

    def change_password(self):
        """Change user password"""
        current_pw = self.current_password_entry.get()
        new_pw = self.new_password_entry.get()
        confirm_pw = self.confirm_password_entry.get()

        # Validation
        if not current_pw or not new_pw or not confirm_pw:
            if self.main_app:
                self.main_app.show_notification("Please fill in all password fields!", type="error")
            return

        if new_pw != confirm_pw:
            if self.main_app:
                self.main_app.show_notification("New passwords do not match!", type="error")
            return

        if len(new_pw) < 6:
            if self.main_app:
                self.main_app.show_notification("Password must be at least 6 characters long!", type="error")
            return

        # Verify current password
        try:
            user_doc = self.db.users_collection.find_one({'username': self.user['username']})
            if not user_doc or not SecurityManager.verify_password(current_pw, user_doc['password_hash']):
                if self.main_app:
                    self.main_app.show_notification("Current password is incorrect!", type="error")
                return
        except Exception as e:
            if self.main_app:
                self.main_app.show_notification(f"Password verification failed: {str(e)}", type="error")
            return

        # Update password
        try:
            new_hash = SecurityManager.hash_password(new_pw)
            result = self.db.users_collection.update_one(
                {'username': self.user['username']},
                {'$set': {'password_hash': new_hash}}
            )

            if self.main_app:
                self.main_app.show_notification("Password changed successfully!", type="success")

            updated_user = self.db.get_user_profile(self.user['username'])
            ProfilePage(self.parent, self.db, updated_user, self.refresh_home, main_app=self.main_app)

        except Exception as e:
            if self.main_app:
                self.main_app.show_notification(f"Failed to update password: {str(e)}", type="error")

    def go_back_to_profile(self):
        """Go back to profile page"""
        ProfilePage(self.parent, self.db, self.user, self.refresh_home, main_app=self.main_app)

    def go_home(self):
        """Go to home page"""
        self.refresh_home(self.user)
 