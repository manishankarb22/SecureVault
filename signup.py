import customtkinter as ctk
from tkinter import messagebox, Canvas
from database import DatabaseManager
from security import SecurityManager, InputValidator
import cv2
import numpy as np
import insightface
import base64
from PIL import Image, ImageTk
import io
import threading
import time
import math
import sys
import os

def get_model_dir():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "models", "buffalo_l")

class SignupPage:
    def __init__(self, parent, show_login_page, show_home_page, main_app=None):
        self.parent = parent
        self.show_login_page = show_login_page
        self.show_home_page = show_home_page
        self.db_manager = DatabaseManager()
        self.validator = InputValidator()
        self.signup_fields = {}
        self.validation_labels = {}
        self.main_app = main_app
        self.captured_face_bytes = None
        
        # Face capture variables
        self.cap = None
        self.face_model = None
        self.capture_thread = None
        self.is_capturing = False
        self.canvas = None
        self.face_detected_time = 0
        self.face_stable_duration = 2.0
        self.capture_window = None
        
        # Animation variables
        self.animation_frame = 0
        self.scan_line_pos = 0
        self.node_pulse = 0
        self.wireframe_vertices = []
        self.detection_progress = 0
        self.animation_thread = None
        self.is_animating = False
        
        self.build_ui()

    def build_ui(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        signup_card = ctk.CTkFrame(
            self.parent,
            width=450,
            height=700,
            corner_radius=20,
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
            width=100,
            height=26,
            font=ctk.CTkFont(size=9, weight="bold"),
            corner_radius=13,
            fg_color="transparent",
            text_color="#666666",
            hover_color="#F0F0F0",
            border_width=1,
            border_color="#CCCCCC",
            command=self.show_login_page
        )
        back_btn.place(x=10, y=10)

        # Header
        header_frame = ctk.CTkFrame(signup_card, fg_color="transparent")
        header_frame.pack(pady=(35, 10))

        icon_frame = ctk.CTkFrame(
            header_frame,
            width=40,
            height=40,
            corner_radius=20,
            fg_color="#000000"
        )
        icon_frame.pack()

        ctk.CTkLabel(
            icon_frame,
            text="👤",
            font=ctk.CTkFont(size=18),
            text_color="#FFFFFF"
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            header_frame,
            text="CREATE ACCOUNT",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#000000"
        ).pack(pady=(8, 2))

        ctk.CTkLabel(
            header_frame,
            text="Join the secure platform",
            font=ctk.CTkFont(size=9),
            text_color="#666666"
        ).pack()

        # Form container
        form_container = ctk.CTkFrame(
            signup_card,
            width=380,
            height=280,
            corner_radius=10,
            fg_color="#F8F9FA",
            border_width=1,
            border_color="#E0E0E0"
        )
        form_container.pack(pady=8, padx=20)
        form_container.pack_propagate(False)

        self.create_compact_signup_fields(form_container, entry_width=340)

        # Face capture status
        self.face_status_label = ctk.CTkLabel(
            signup_card,
            text="Face not captured",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#DC3545"
        )
        self.face_status_label.pack(pady=(5, 0))

        # Capture Face button
        self.capture_btn = ctk.CTkButton(
            signup_card,
            text="🔬 Start Biometric Scan",
            width=250,
            height=36,
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=15,
            fg_color="#00BCD4",
            hover_color="#26C6DA",
            text_color="#FFFFFF",
            command=self.toggle_face_capture
        )
        self.capture_btn.pack(pady=(5, 10))

        # Terms
        terms_frame = ctk.CTkFrame(
            signup_card,
            corner_radius=8,
            fg_color="#F0F0F0",
            border_width=1,
            border_color="#CCCCCC"
        )
        terms_frame.pack(fill="x", padx=20, pady=(6, 4))

        ctk.CTkLabel(
            terms_frame,
            text="By creating account, you agree to Terms & Privacy Policy.",
            font=ctk.CTkFont(size=7, weight="bold"),
            text_color="#666666",
            justify="center"
        ).pack(pady=4)

        # Create account button
        create_btn_frame = ctk.CTkFrame(signup_card, fg_color="transparent")
        create_btn_frame.pack(pady=(4, 10))

        create_btn = ctk.CTkButton(
            create_btn_frame,
            text="⚪ CREATE ACCOUNT",
            width=250,
            height=36,
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=15,
            fg_color="#000000",
            hover_color="#333333",
            text_color="#FFFFFF",
            command=self.handle_signup
        )
        create_btn.pack()

    def create_compact_signup_fields(self, parent, entry_width=340):
        scroll_frame = ctk.CTkScrollableFrame(
            parent,
            width=entry_width+20,
            height=250,
            corner_radius=8,
            fg_color="transparent"
        )
        scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        fields = [
            ("username", "👤 Username", "Choose username"),
            ("email", "📧 Email", "your.email@domain.com"),
            ("password", "🔐 Password", "Strong password"),
            ("confirm", "🔒 Confirm", "Confirm password")
        ]

        for field_name, label, placeholder in fields:
            field_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            field_container.pack(pady=5, padx=8, fill="x")

            ctk.CTkLabel(
                field_container,
                text=label,
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color="#000000",
                anchor="w"
            ).pack(anchor="w", padx=4, pady=(0, 2))

            entry = ctk.CTkEntry(
                field_container,
                placeholder_text=placeholder,
                width=entry_width,
                height=26,
                font=ctk.CTkFont(size=9),
                corner_radius=10,
                border_width=2,
                border_color="#CCCCCC",
                fg_color="#FFFFFF",
                text_color="#000000"
            )

            if "Password" in label or "Confirm" in label:
                entry.configure(show="*")

            entry.pack()
            self.signup_fields[field_name] = entry

            validation = ctk.CTkLabel(
                field_container,
                text="",
                font=ctk.CTkFont(size=7),
                anchor="w"
            )
            validation.pack(anchor="w", padx=4, pady=(1, 0))
            self.validation_labels[field_name] = validation

            entry.bind('<KeyRelease>', lambda e, name=field_name: self.validate_field(name))

    def validate_field(self, field_name):
        if field_name not in self.signup_fields:
            return

        value = self.signup_fields[field_name].get()
        validation_label = self.validation_labels[field_name]

        if field_name == 'username':
            if value:
                is_valid, message = self.validator.validate_username(value)
                if is_valid:
                    # Check uniqueness
                    if self.db_manager.is_username_taken(value):
                        validation_label.configure(text="✗ Username already taken", text_color="#DC3545")
                    else:
                        validation_label.configure(text="✓ Username available", text_color="#28A745")
                else:
                    validation_label.configure(text=f"✗ {message}", text_color="#DC3545")
            else:
                validation_label.configure(text="")

        elif field_name == 'email':
            if value:
                is_valid, message = self.validator.validate_email(value)
                if is_valid:
                    # Check uniqueness
                    if self.db_manager.is_email_taken(value):
                        validation_label.configure(text="✗ Email already registered", text_color="#DC3545")
                    else:
                        validation_label.configure(text="✓ Email available", text_color="#28A745")
                else:
                    validation_label.configure(text=f"✗ {message}", text_color="#DC3545")
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

    def toggle_face_capture(self):
        if not self.is_capturing:
            self.start_face_capture()
        else:
            self.stop_face_capture()

    def start_face_capture(self):
        """Start the face capture process with animated UI"""
        if self.main_app:
            self.main_app.show_notification("Initializing biometric scanner...", type="info")

        # Initialize InsightFace model
        try:
            model_dir = get_model_dir()
            print("MODEL DIR (should be .../models/buffalo_l):", model_dir)
            print("MODEL DIR EXISTS:", os.path.exists(model_dir))
            print("MODEL DIR CONTENTS:", os.listdir(model_dir) if os.path.exists(model_dir) else "N/A")
            model_root = os.path.dirname(model_dir)
            expected_files = [
                '1k3d68.onnx', '2d106det.onnx', 'det_10g.onnx', 'genderage.onnx', 'w600k_r50.onnx'
            ]
            missing = [f for f in expected_files if f not in os.listdir(model_dir)]
            if missing:
                print(f"[WARNING] Missing model files: {missing}. Face detection will not work!")
            else:
                print("[INFO] All required model files are present.")
            # Temporarily use default cache for model download
            self.face_model = insightface.app.FaceAnalysis(name='buffalo_l')
            self.face_model.prepare(ctx_id=0, det_size=(640, 640))
        except Exception as e:
            if self.main_app:
                self.main_app.show_notification(f"Failed to load biometric model: {str(e)}", type="error")
            return

        # Open webcam
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            if self.main_app:
                self.main_app.show_notification("Could not access camera.", type="error")
            return

        # Create animated capture window
        self.create_animated_capture_window()
        
        # Start capture and animation threads
        self.is_capturing = True
        self.is_animating = True
        
        self.capture_thread = threading.Thread(target=self.capture_loop, daemon=True)
        self.animation_thread = threading.Thread(target=self.animation_loop, daemon=True)
        
        self.capture_thread.start()
        self.animation_thread.start()

        # Update button
        self.capture_btn.configure(
            text="🛑 Stop Scanner",
            fg_color="#DC3545",
            hover_color="#C82333"
        )

        if self.main_app:
            self.main_app.show_notification("Biometric scanner active. Position your face in the detection zone.", type="info")

    def create_animated_capture_window(self):
        """Create animated capture window with sci-fi interface"""
        self.capture_window = ctk.CTkToplevel(self.parent)
        self.capture_window.title("Biometric Scanner")
        self.capture_window.geometry("600x500")
        self.capture_window.resizable(False, False)
        self.capture_window.configure(fg_color="#0A0A0A")
        
        # Center the window
        self.capture_window.transient(self.parent.master)
        self.capture_window.grab_set()
        
        # Header with sci-fi styling
        header_frame = ctk.CTkFrame(
            self.capture_window,
            fg_color="#1A1A1A",
            corner_radius=0,
            height=60
        )
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)

        ctk.CTkLabel(
            header_frame,
            text="🔬 BIOMETRIC FACIAL RECOGNITION SYSTEM",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00BCD4"
        ).place(relx=0.5, rely=0.3, anchor="center")

        ctk.CTkLabel(
            header_frame,
            text="Advanced Neural Pattern Detection Active",
            font=ctk.CTkFont(size=10),
            text_color="#666666"
        ).place(relx=0.5, rely=0.7, anchor="center")

        # Main scanner area
        scanner_frame = ctk.CTkFrame(
            self.capture_window,
            fg_color="#0F0F0F",
            corner_radius=10,
            border_width=2,
            border_color="#00BCD4"
        )
        scanner_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Canvas for video and animations
        self.canvas = Canvas(
            scanner_frame,
            width=500,
            height=350,
            bg="#000000",
            highlightthickness=0
        )
        self.canvas.pack(pady=15)

        # Status display
        status_frame = ctk.CTkFrame(
            self.capture_window,
            fg_color="#1A1A1A",
            corner_radius=8,
            height=80
        )
        status_frame.pack(fill="x", padx=20, pady=(0, 10))
        status_frame.pack_propagate(False)

        self.capture_status_label = ctk.CTkLabel(
            status_frame,
            text="SCANNING FOR BIOMETRIC SIGNATURE...",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#00BCD4"
        )
        self.capture_status_label.place(relx=0.5, rely=0.3, anchor="center")

        self.progress_label = ctk.CTkLabel(
            status_frame,
            text="Detection Progress: 0%",
            font=ctk.CTkFont(size=10),
            text_color="#666666"
        )
        self.progress_label.place(relx=0.5, rely=0.7, anchor="center")

        # Control buttons
        control_frame = ctk.CTkFrame(self.capture_window, fg_color="transparent")
        control_frame.pack(pady=5)

        close_btn = ctk.CTkButton(
            control_frame,
            text="ABORT SCAN",
            width=120,
            height=35,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#DC3545",
            hover_color="#C82333",
            text_color="#FFFFFF",
            corner_radius=8,
            command=self.stop_face_capture
        )
        close_btn.pack()

        # Handle window close
        self.capture_window.protocol("WM_DELETE_WINDOW", self.stop_face_capture)

        # Initialize wireframe vertices
        self.initialize_wireframe()

    def initialize_wireframe(self):
        """Initialize wireframe face vertices"""
        center_x, center_y = 250, 175
        
        # Define face outline points (oval shape)
        face_points = []
        for i in range(16):
            angle = i * (2 * math.pi / 16)
            x = center_x + 80 * math.cos(angle)
            y = center_y + 100 * math.sin(angle)
            face_points.append((x, y))
        
        # Add feature points
        eye_left = (center_x - 30, center_y - 20)
        eye_right = (center_x + 30, center_y - 20)
        nose = (center_x, center_y + 10)
        mouth_left = (center_x - 20, center_y + 40)
        mouth_right = (center_x + 20, center_y + 40)
        
        self.wireframe_vertices = {
            'face': face_points,
            'features': [eye_left, eye_right, nose, mouth_left, mouth_right],
            'detection_nodes': []
        }

    def animation_loop(self):
        """Main animation loop for UI effects"""
        while self.is_animating and self.capture_window and self.capture_window.winfo_exists():
            try:
                # Update animation counters
                self.animation_frame += 1
                self.scan_line_pos = (self.scan_line_pos + 3) % 350
                self.node_pulse = math.sin(self.animation_frame * 0.1) * 0.5 + 0.5
                
                # Update UI on main thread
                if self.canvas and self.capture_window.winfo_exists():
                    self.canvas.after(0, self.draw_scanner_overlay)
                
                time.sleep(0.05)  # 20 FPS animation
                
            except Exception:
                break

    def draw_scanner_overlay(self):
        """Draw animated scanner overlay on canvas"""
        if not self.canvas or not self.capture_window or not self.capture_window.winfo_exists():
            return

        try:
            # Draw corner brackets
            self.draw_corner_brackets()
            
            # Draw scanning line
            scan_alpha = int(255 * (1 - abs(self.scan_line_pos - 175) / 175))
            scan_color = f"#{0:02x}{max(0, scan_alpha):02x}{max(0, scan_alpha):02x}"
            
            if self.canvas.winfo_exists():
                self.canvas.create_line(
                    50, self.scan_line_pos,
                    450, self.scan_line_pos,
                    fill="#00BCD4",
                    width=2,
                    tags="overlay"
                )

            # Draw grid pattern
            self.draw_grid_pattern()
            
            # Draw wireframe if face detected
            if hasattr(self, 'current_face_box') and self.current_face_box is not None:
                self.draw_face_wireframe()
                
        except Exception:
            pass

    def draw_corner_brackets(self):
        """Draw animated corner brackets"""
        bracket_size = 30
        bracket_width = 3
        
        # Animate bracket extension
        extension = int(bracket_size * (0.7 + 0.3 * math.sin(self.animation_frame * 0.05)))
        
        positions = [
            (50, 50),      # Top-left
            (450, 50),     # Top-right
            (50, 300),     # Bottom-left
            (450, 300)     # Bottom-right
        ]
        
        for i, (x, y) in enumerate(positions):
            color = "#00BCD4" if i % 2 == 0 else "#4CAF50"
            
            if i == 0:  # Top-left
                if self.canvas.winfo_exists():
                    self.canvas.create_line(x, y, x + extension, y, fill=color, width=bracket_width, tags="overlay")
                if self.canvas.winfo_exists():
                    self.canvas.create_line(x, y, x, y + extension, fill=color, width=bracket_width, tags="overlay")
            elif i == 1:  # Top-right
                if self.canvas.winfo_exists():
                    self.canvas.create_line(x, y, x - extension, y, fill=color, width=bracket_width, tags="overlay")
                if self.canvas.winfo_exists():
                    self.canvas.create_line(x, y, x, y + extension, fill=color, width=bracket_width, tags="overlay")
            elif i == 2:  # Bottom-left
                if self.canvas.winfo_exists():
                    self.canvas.create_line(x, y, x + extension, y, fill=color, width=bracket_width, tags="overlay")
                if self.canvas.winfo_exists():
                    self.canvas.create_line(x, y, x, y - extension, fill=color, width=bracket_width, tags="overlay")
            elif i == 3:  # Bottom-right
                if self.canvas.winfo_exists():
                    self.canvas.create_line(x, y, x - extension, y, fill=color, width=bracket_width, tags="overlay")
                if self.canvas.winfo_exists():
                    self.canvas.create_line(x, y, x, y - extension, fill=color, width=bracket_width, tags="overlay")

    def draw_grid_pattern(self):
        """Draw animated grid pattern"""
        grid_spacing = 25
        grid_alpha = int(50 + 30 * math.sin(self.animation_frame * 0.03))
        
        for x in range(75, 425, grid_spacing):
            if self.canvas.winfo_exists():
                self.canvas.create_line(
                    x, 75, x, 275,
                    fill=f"#{grid_alpha:02x}{grid_alpha:02x}{grid_alpha:02x}",
                    width=1,
                    tags="overlay"
                )
        
        for y in range(75, 275, grid_spacing):
            if self.canvas.winfo_exists():
                self.canvas.create_line(
                    75, y, 425, y,
                    fill=f"#{grid_alpha:02x}{grid_alpha:02x}{grid_alpha:02x}",
                    width=1,
                    tags="overlay"
                )

    def draw_face_wireframe(self):
        """Draw animated wireframe over detected face"""
        if not hasattr(self, 'current_face_box') or self.current_face_box is None:
            return
            
        box = self.current_face_box
        
        # Scale box to canvas coordinates (500x350 canvas from 400x300 frame)
        scale_x = 500 / 400
        scale_y = 350 / 300
        
        x1 = int(box[0] * scale_x)
        y1 = int(box[1] * scale_y)
        x2 = int(box[2] * scale_x)
        y2 = int(box[3] * scale_y)
        
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        width = x2 - x1
        height = y2 - y1
        
        # Draw main face outline
        face_points = []
        num_points = 12
        for i in range(num_points):
            angle = i * (2 * math.pi / num_points) + self.animation_frame * 0.02
            x = center_x + (width * 0.4) * math.cos(angle)
            y = center_y + (height * 0.45) * math.sin(angle)
            face_points.extend([x, y])
        
        if len(face_points) >= 4:
            if self.canvas.winfo_exists():
                self.canvas.create_polygon(
                    face_points,
                    outline="#00FF41",
                    fill="",
                    width=2,
                    tags="overlay"
                )
        
        # Draw detection nodes
        node_positions = [
            (center_x - width//4, center_y - height//4),  # Left eye
            (center_x + width//4, center_y - height//4),  # Right eye
            (center_x, center_y),                         # Nose
            (center_x - width//6, center_y + height//4),  # Mouth left
            (center_x + width//6, center_y + height//4),  # Mouth right
        ]
        
        for i, (nx, ny) in enumerate(node_positions):
            pulse_size = int(4 + 3 * math.sin(self.animation_frame * 0.1 + i * 0.5))
            
            if self.canvas.winfo_exists():
                self.canvas.create_oval(
                    nx - pulse_size, ny - pulse_size,
                    nx + pulse_size, ny + pulse_size,
                    outline="#FF6B35",
                    fill="#FF6B35",
                    width=2,
                    tags="overlay"
                )
        
        # Draw connecting lines
        for i in range(len(node_positions)):
            for j in range(i + 1, len(node_positions)):
                x1, y1 = node_positions[i]
                x2, y2 = node_positions[j]
                
                line_alpha = int(100 + 50 * math.sin(self.animation_frame * 0.05 + i + j))
                
                if self.canvas.winfo_exists():
                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill=f"#{line_alpha:02x}{line_alpha:02x}FF",
                        width=1,
                        tags="overlay"
                    )

    def capture_loop(self):
        """Main capture loop with face detection and animation"""
        face_detected_start = None
        self.current_face_box = None
        
        while self.is_capturing and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            # Resize frame for processing
            frame_resized = cv2.resize(frame, (400, 300))
            
            # Detect faces
            faces = self.face_model.get(frame_resized)
            
            current_time = time.time()
            
            if faces:
                face = faces[0]
                self.current_face_box = face.bbox.astype(int)
                
                if face_detected_start is None:
                    face_detected_start = current_time
                
                time_elapsed = current_time - face_detected_start
                remaining_time = max(0, self.face_stable_duration - time_elapsed)
                self.detection_progress = min(100, int((time_elapsed / self.face_stable_duration) * 100))
                
                if remaining_time > 0:
                    status_text = f"BIOMETRIC SIGNATURE DETECTED - ANALYZING..."
                    progress_text = f"Neural Pattern Analysis: {self.detection_progress}%"
                    self.update_capture_status(status_text, progress_text)
                else:
                    # Capture the face
                    self.perform_face_capture(frame_resized, face)
                    break
                    
            else:
                self.current_face_box = None
                face_detected_start = None
                self.detection_progress = 0
                self.update_capture_status("SCANNING FOR BIOMETRIC SIGNATURE...", "Detection Progress: 0%")

            # Convert and display frame
            self.update_video_display(frame_resized)
            
            time.sleep(0.05)

        self.stop_face_capture()

    def update_video_display(self, frame):
        """Update video display with frame"""
        if self.canvas and self.capture_window and self.capture_window.winfo_exists():
            try:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Resize to fit canvas
                frame_resized = cv2.resize(frame_rgb, (500, 350))
                # Convert to PIL Image
                pil_image = Image.fromarray(frame_resized)
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(pil_image)
                
                def update_display():
                    if self.canvas and self.capture_window and self.capture_window.winfo_exists():
                        try:
                            self.canvas.delete("video")
                            self.canvas.create_image(250, 175, image=photo, tags="video")
                            self.canvas.image = photo
                            self.canvas.delete("overlay")
                            self.draw_scanner_overlay()
                        except Exception:
                            pass
                self.canvas.after(0, update_display)
                
            except Exception:
                pass

    def update_capture_status(self, status_text, progress_text=""):
        """Update capture status labels"""
        def update():
            if (self.capture_status_label and self.capture_window and 
                self.capture_window.winfo_exists()):
                self.capture_status_label.configure(text=status_text)
                
            if (self.progress_label and self.capture_window and 
                self.capture_window.winfo_exists() and progress_text):
                self.progress_label.configure(text=progress_text)
        
        if self.capture_window and self.capture_window.winfo_exists():
            self.capture_window.after(0, update)

    def perform_face_capture(self, frame, face):
        """Capture the detected face with success animation"""
        try:
            # Try to use crop_face if available, else fallback to bbox crop
            if hasattr(face, 'crop_face') and callable(face.crop_face):
                aligned_face = face.crop_face(frame)
            else:
                box = face.bbox.astype(int)
                aligned_face = frame[box[1]:box[3], box[0]:box[2]]
            pil_img = Image.fromarray(cv2.cvtColor(aligned_face, cv2.COLOR_BGR2RGB))
            buf = io.BytesIO()
            pil_img.save(buf, format='PNG')
            self.captured_face_bytes = buf.getvalue()
            # Extract embedding using InsightFace
            model_dir = get_model_dir()
            print("MODEL DIR (should be .../models/buffalo_l):", model_dir)
            print("MODEL DIR EXISTS:", os.path.exists(model_dir))
            print("MODEL DIR CONTENTS:", os.listdir(model_dir) if os.path.exists(model_dir) else "N/A")
            model_root = os.path.dirname(model_dir)
            expected_files = [
                '1k3d68.onnx', '2d106det.onnx', 'det_10g.onnx', 'genderage.onnx', 'w600k_r50.onnx'
            ]
            missing = [f for f in expected_files if f not in os.listdir(model_dir)]
            if missing:
                print(f"[WARNING] Missing model files: {missing}. Face detection will not work!")
            else:
                print("[INFO] All required model files are present.")
            # Temporarily use default cache for model download
            model = insightface.app.FaceAnalysis(name='buffalo_l')
            model.prepare(ctx_id=0, det_size=(640, 640))
            print("[DEBUG] Aligned face shape:", aligned_face.shape)
            faces = model.get(aligned_face)
            print("[DEBUG] Faces detected in aligned_face:", len(faces))
            if not faces or not hasattr(faces[0], 'embedding'):
                print("[DEBUG] No face in aligned_face, trying original frame.")
                faces = model.get(frame)
                print("[DEBUG] Faces detected in original frame:", len(faces))
            if faces and hasattr(faces[0], 'embedding'):
                emb = faces[0].embedding.astype(np.float32)
                self.captured_face_embedding = base64.b64encode(emb.tobytes()).decode('utf-8')
                print("[DEBUG] Face embedding captured.")
                self.parent.after(0, self.face_capture_success)
            else:
                self.captured_face_embedding = None
                print("[DEBUG] Face embedding extraction failed.")
                if self.main_app:
                    self.main_app.show_notification("Biometric scan failed. Please try again.", type="error")
        except Exception as e:
            error_msg = str(e)
            self.parent.after(0, lambda error_msg=error_msg: self.face_capture_error(error_msg))

    def face_capture_success(self):
        """Handle successful face capture"""
        self.face_status_label.configure(
            text="✓ Biometric signature captured successfully!",
            text_color="#28A745"
        )
        
        if self.main_app:
            self.main_app.show_notification("Biometric signature captured and verified!", type="success")
        
        # Show success animation briefly before closing
        if self.capture_window and self.capture_window.winfo_exists():
            self.update_capture_status("✓ BIOMETRIC CAPTURE COMPLETE", "Neural Pattern Verified: 100%")
            self.capture_window.after(2000, self.stop_face_capture)

    def face_capture_error(self, error_msg):
        """Handle face capture error"""
        if self.main_app:
            self.main_app.show_notification(f"Biometric capture failed: {error_msg}", type="error")
        
        self.stop_face_capture()

    def stop_face_capture(self):
        """Stop face capture and cleanup"""
        self.is_capturing = False
        self.is_animating = False
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        if self.capture_window and self.capture_window.winfo_exists():
            self.capture_window.destroy()
            self.capture_window = None
        
        self.canvas = None
        self.current_face_box = None
        
        # Reset button
        self.capture_btn.configure(
            text="🔬 Start Biometric Scan",
            fg_color="#00BCD4",
            hover_color="#26C6DA"
        )

    def handle_signup(self):
        username = self.signup_fields["username"].get().strip()
        email = self.signup_fields["email"].get().strip()
        password = self.signup_fields["password"].get()
        confirm = self.signup_fields["confirm"].get()

        if not all([username, email, password, confirm]):
            if self.main_app:
                self.main_app.show_notification("Please fill in all fields", type="error")
            return

        if not self.captured_face_bytes or not getattr(self, 'captured_face_embedding', None):
            if self.main_app:
                self.main_app.show_notification("Please complete biometric scan before signing up.", type="warning")
            return

        # Uniqueness checks
        if self.db_manager.is_username_taken(username):
            if self.main_app:
                self.main_app.show_notification("Username already taken. Please choose another.", type="error")
            return
        if self.db_manager.is_email_taken(email):
            if self.main_app:
                self.main_app.show_notification("Email already registered. Please use another.", type="error")
            return

        # Validation checks
        username_valid, username_msg = self.validator.validate_username(username)
        if not username_valid:
            if self.main_app:
                self.main_app.show_notification(username_msg, type="error")
            return

        email_valid, email_msg = self.validator.validate_email(email)
        if not email_valid:
            if self.main_app:
                self.main_app.show_notification(email_msg, type="error")
            return

        password_valid, password_msg = self.validator.validate_password(password)
        if not password_valid:
            if self.main_app:
                self.main_app.show_notification(password_msg, type="error")
            return

        if password != confirm:
            if self.main_app:
                self.main_app.show_notification("Passwords do not match", type="error")
            return

        # Create user
        password_hash = SecurityManager.hash_password(password)
        face_b64 = base64.b64encode(self.captured_face_bytes).decode('utf-8')
        face_emb_b64 = self.captured_face_embedding
        success, message = self.db_manager.create_user(username, email, password_hash, face_b64, face_emb_b64)
        if success:
            if self.main_app:
                self.main_app.show_notification(f"Account created successfully! Welcome to Secure Vault, {username}! Your biometric profile has been registered.", type="success")
            user_info = {'username': username, 'email': email}
            self.show_home_page(user_info)
        else:
            if self.main_app:
                self.main_app.show_notification(message, type="error")
 