import customtkinter as ctk
from database import DatabaseManager
from security import SecurityManager, InputValidator
from login import LoginPage
from signup import SignupPage
from home import HomePage
import tkinter.simpledialog as simpledialog
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from datetime import datetime
from profile import ProfilePage
from PIL import Image, ImageTk
import cv2
import numpy as np
import base64
from PIL import Image
import io
import insightface
import time
import customtkinter as ctk
from tkinter import Canvas
import math
from file_viewer import FileViewer
import sys
import threading

def get_model_dir():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path,"models", "buffalo_l")

class PasswordPromptDialog(ctk.CTkToplevel):
    def __init__(self, master, title, confirm=False):
        super().__init__(master)
        self.title(title)
        self.geometry("340x200" if not confirm else "340x260")
        self.configure(bg="#000000")
        self.resizable(False, False)
        self.password = None
        self.confirm_password = None
        self.result = None
        self.build_ui(confirm)
        self.grab_set()
        self.wait_window()

    def build_ui(self, confirm):
        ctk.CTkLabel(self, text=self.title(), font=("Segoe UI", 16, "bold"), text_color="#FFF").pack(pady=(18,10))
        ctk.CTkLabel(self, text="Password", text_color="#FFF").pack(anchor="w", padx=40, pady=(2,0))
        self.pw_entry = ctk.CTkEntry(self, width=220, fg_color="#FFF", text_color="#000", show="*")
        self.pw_entry.pack(pady=(0,8))

        if confirm:
            ctk.CTkLabel(self, text="Confirm Password", text_color="#FFF").pack(anchor="w", padx=40, pady=(2,0))
            self.confirm_entry = ctk.CTkEntry(self, width=220, fg_color="#FFF", text_color="#000", show="*")
            self.confirm_entry.pack(pady=(0,8))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="OK", fg_color="#FFF", text_color="#000", width=90, command=self.on_ok).pack(side="left", padx=8)
        ctk.CTkButton(btn_frame, text="Cancel", fg_color="#FFF", text_color="#000", width=90, command=self.destroy).pack(side="left", padx=8)

    def on_ok(self):
        pw = self.pw_entry.get()
        if hasattr(self, 'confirm_entry'):
            confirm_pw = self.confirm_entry.get()
            if pw != confirm_pw:
                from tkinter import messagebox
                messagebox.showerror("Password Mismatch", "Passwords do not match. Please try again.")
                return
            self.result = pw
        else:
            self.result = pw
        self.destroy()

class BiometricScanDialog(ctk.CTkToplevel):
    def __init__(self, master, face_model, on_capture=None):
        super().__init__(master)
        self.title("Biometric Scanner")
        self.geometry("600x500")
        self.resizable(False, False)
        self.configure(fg_color="#0A0A0A")
        self.on_capture = on_capture
        self.cap = None
        self.is_capturing = True
        self.animation_frame = 0
        self.scan_line_pos = 0
        self.current_face_box = None
        self.face_stable_duration = 3.0
        self.face_img = None
        self.captured_face = None
        self.model = face_model  # Use pre-initialized model
        self._build_ui()
        self._start_capture()

    def _build_ui(self):
        header_frame = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=0, height=60)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        ctk.CTkLabel(header_frame, text="🔬 BIOMETRIC FACIAL RECOGNITION SYSTEM", font=ctk.CTkFont(size=14, weight="bold"), text_color="#00BCD4").place(relx=0.5, rely=0.3, anchor="center")
        ctk.CTkLabel(header_frame, text="Advanced Neural Pattern Detection Active", font=ctk.CTkFont(size=10), text_color="#666666").place(relx=0.5, rely=0.7, anchor="center")

        scanner_frame = ctk.CTkFrame(self, fg_color="#0F0F0F", corner_radius=10, border_width=2, border_color="#00BCD4")
        scanner_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.canvas = Canvas(scanner_frame, width=500, height=350, bg="#000000", highlightthickness=0)
        self.canvas.pack(pady=15)

        status_frame = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=8, height=80)
        status_frame.pack(fill="x", padx=20, pady=(0, 10))
        status_frame.pack_propagate(False)
        self.capture_status_label = ctk.CTkLabel(status_frame, text="SCANNING FOR BIOMETRIC SIGNATURE...", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00BCD4")
        self.capture_status_label.place(relx=0.5, rely=0.3, anchor="center")
        self.progress_label = ctk.CTkLabel(status_frame, text="Detection Progress: 0%", font=ctk.CTkFont(size=10), text_color="#666666")
        self.progress_label.place(relx=0.5, rely=0.7, anchor="center")

        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.pack(pady=5)
        close_btn = ctk.CTkButton(control_frame, text="ABORT SCAN", width=120, height=35, font=ctk.CTkFont(size=11, weight="bold"), fg_color="#DC3545", hover_color="#C82333", text_color="#FFFFFF", corner_radius=8, command=self._stop_capture)
        close_btn.pack()
        self.protocol("WM_DELETE_WINDOW", self._stop_capture)

    def _start_capture(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.capture_status_label.configure(text="Could not access camera.", text_color="#DC3545")
            return

        self.start_time = time.time()
        self.is_capturing = True
        self.after(10, self._capture_loop)
        self.after(10, self._animation_loop)

    def _capture_loop(self):
        if not self.is_capturing or not self.cap or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if not ret:
            self._stop_capture()
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = self.model.get(frame_rgb)
        elapsed = time.time() - self.start_time

        if faces:
            self.current_face_box = faces[0].bbox.astype(int)
            if elapsed >= self.face_stable_duration:
                self.captured_face = frame_rgb
                self._stop_capture(success=True)
                return

            status_text = f"Face detected! Capturing in {max(0, int(self.face_stable_duration-elapsed))}s"
            progress_text = f"Neural Pattern Analysis: {min(100, int((elapsed/self.face_stable_duration)*100))}%"
            self.capture_status_label.configure(text=status_text, text_color="#00BCD4")
            self.progress_label.configure(text=progress_text)
        else:
            self.current_face_box = None
            self.start_time = time.time()
            self.capture_status_label.configure(text="SCANNING FOR BIOMETRIC SIGNATURE...", text_color="#00BCD4")
            self.progress_label.configure(text="Detection Progress: 0%")

        self._update_video_display(frame_rgb)
        self.after(30, self._capture_loop)

    def _animation_loop(self):
        if not self.is_capturing or not self.canvas or not self.winfo_exists():
            return
        self.animation_frame += 1
        self.scan_line_pos = (self.scan_line_pos + 3) % 350
        self._draw_scanner_overlay()
        self.after(50, self._animation_loop)

    def _update_video_display(self, frame):
        frame_resized = cv2.resize(frame, (500, 350))
        pil_image = Image.fromarray(frame_resized)
        photo = ImageTk.PhotoImage(pil_image)
        if self.canvas and self.canvas.winfo_exists():
            try:
                self.canvas.delete("video")
                self.canvas.create_image(250, 175, image=photo, tags="video")
                self.canvas.image = photo
            except Exception:
                pass

    def _draw_scanner_overlay(self):
        if not self.canvas or not self.canvas.winfo_exists():
            return
        try:
            self.canvas.delete("overlay")
            self.canvas.create_line(50, self.scan_line_pos, 450, self.scan_line_pos, fill="#00BCD4", width=2, tags="overlay")
            if self.current_face_box is not None:
                scale_x = 500 / 400
                scale_y = 350 / 300
                box = self.current_face_box
                x1 = int(box[0] * scale_x)
                y1 = int(box[1] * scale_y)
                x2 = int(box[2] * scale_x)
                y2 = int(box[3] * scale_y)
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="#00FF41", width=2, tags="overlay")
        except Exception:
            pass

    def _stop_capture(self, success=False):
        self.is_capturing = False
        if self.cap:
            self.cap.release()
            self.cap = None
        if hasattr(self, 'canvas') and self.canvas and self.canvas.winfo_exists():
            try:
                self.canvas.delete("all")
            except Exception:
                pass
        self.destroy()
        if success and self.on_capture:
            self.on_capture(self.captured_face)

class FaceCaptureDialog(ctk.CTkToplevel):
    def __init__(self, master, face_model, on_capture=None):
        super().__init__(master)
        self.title("Biometric Scanner")
        self.geometry("600x500")
        self.resizable(False, False)
        self.configure(fg_color="#0A0A0A")
        self.on_capture = on_capture
        self.cap = None
        self.is_capturing = True
        self.animation_frame = 0
        self.scan_line_pos = 0
        self.current_face_box = None
        self.face_stable_duration = 2.0
        self.face_img = None
        self.captured_face = None
        self.captured_face_embedding = None
        self.model = face_model  # Use pre-initialized model
        self._build_ui()
        self._start_capture()

    def _build_ui(self):
        header_frame = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=0, height=60)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        ctk.CTkLabel(header_frame, text="🔬 BIOMETRIC FACIAL RECOGNITION SYSTEM", font=ctk.CTkFont(size=14, weight="bold"), text_color="#00BCD4").place(relx=0.5, rely=0.3, anchor="center")
        ctk.CTkLabel(header_frame, text="Advanced Neural Pattern Detection Active", font=ctk.CTkFont(size=10), text_color="#666666").place(relx=0.5, rely=0.7, anchor="center")

        scanner_frame = ctk.CTkFrame(self, fg_color="#0F0F0F", corner_radius=10, border_width=2, border_color="#00BCD4")
        scanner_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.canvas = Canvas(scanner_frame, width=500, height=350, bg="#000000", highlightthickness=0)
        self.canvas.pack(pady=15)

        status_frame = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=8, height=80)
        status_frame.pack(fill="x", padx=20, pady=(0, 10))
        status_frame.pack_propagate(False)
        self.capture_status_label = ctk.CTkLabel(status_frame, text="SCANNING FOR BIOMETRIC SIGNATURE...", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00BCD4")
        self.capture_status_label.place(relx=0.5, rely=0.3, anchor="center")
        self.progress_label = ctk.CTkLabel(status_frame, text="Detection Progress: 0%", font=ctk.CTkFont(size=10), text_color="#666666")
        self.progress_label.place(relx=0.5, rely=0.7, anchor="center")

        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.pack(pady=5)
        close_btn = ctk.CTkButton(control_frame, text="ABORT SCAN", width=120, height=35, font=ctk.CTkFont(size=11, weight="bold"), fg_color="#DC3545", hover_color="#C82333", text_color="#FFFFFF", corner_radius=8, command=self._stop_capture)
        close_btn.pack()
        self.protocol("WM_DELETE_WINDOW", self._stop_capture)

    def _start_capture(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.capture_status_label.configure(text="Could not access camera.", text_color="#DC3545")
            return

        self.start_time = time.time()
        self.is_capturing = True
        self.after(10, self._capture_loop)
        self.after(10, self._animation_loop)

    def _capture_loop(self):
        if not self.is_capturing or not self.cap or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if not ret:
            self._stop_capture()
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = self.model.get(frame_rgb)
        elapsed = time.time() - self.start_time

        if faces:
            self.current_face_box = faces[0].bbox.astype(int)
            if elapsed >= self.face_stable_duration:
                self.captured_face = frame_rgb
                # Extract embedding
                emb = faces[0].embedding.astype(np.float32) if hasattr(faces[0], 'embedding') else None
                if emb is not None:
                    self.captured_face_embedding = base64.b64encode(emb.tobytes()).decode('utf-8')
                self._stop_capture(success=True)
                return

            status_text = f"Face detected! Capturing in {max(0, int(self.face_stable_duration-elapsed))}s"
            progress_text = f"Neural Pattern Analysis: {min(100, int((elapsed/self.face_stable_duration)*100))}%"
            self.capture_status_label.configure(text=status_text, text_color="#00BCD4")
            self.progress_label.configure(text=progress_text)
        else:
            self.current_face_box = None
            self.start_time = time.time()
            self.capture_status_label.configure(text="SCANNING FOR BIOMETRIC SIGNATURE...", text_color="#00BCD4")
            self.progress_label.configure(text="Detection Progress: 0%")

        self._update_video_display(frame_rgb)
        self.after(30, self._capture_loop)

    def _animation_loop(self):
        if not self.is_capturing or not self.canvas or not self.winfo_exists():
            return
        self.animation_frame += 1
        self.scan_line_pos = (self.scan_line_pos + 3) % 350
        self._draw_scanner_overlay()
        self.after(50, self._animation_loop)

    def _update_video_display(self, frame):
        frame_resized = cv2.resize(frame, (500, 350))
        pil_image = Image.fromarray(frame_resized)
        photo = ImageTk.PhotoImage(pil_image)
        if self.canvas and self.canvas.winfo_exists():
            try:
                self.canvas.delete("video")
                self.canvas.create_image(250, 175, image=photo, tags="video")
                self.canvas.image = photo
            except Exception:
                pass

    def _draw_scanner_overlay(self):
        if not self.canvas or not self.canvas.winfo_exists():
            return
        try:
            self.canvas.delete("overlay")
            self.canvas.create_line(50, self.scan_line_pos, 450, self.scan_line_pos, fill="#00BCD4", width=2, tags="overlay")
            if self.current_face_box is not None:
                scale_x = 500 / 400
                scale_y = 350 / 300
                box = self.current_face_box
                x1 = int(box[0] * scale_x)
                y1 = int(box[1] * scale_y)
                x2 = int(box[2] * scale_x)
                y2 = int(box[3] * scale_y)
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="#00FF41", width=2, tags="overlay")
        except Exception:
            pass

    def _stop_capture(self, success=False):
        self.is_capturing = False
        if self.cap:
            self.cap.release()
            self.cap = None
        if hasattr(self, 'canvas') and self.canvas and self.canvas.winfo_exists():
            try:
                self.canvas.delete("all")
            except Exception:
                pass
        self.destroy()
        if success and self.on_capture:
            self.on_capture(self.captured_face, self.captured_face_embedding)

class MainApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.title("🔐 Secure Vault")
        self.root.geometry("1200x800")
        self.root.configure(fg_color="#000000")

        self.db_manager = DatabaseManager()
        self.security_manager = SecurityManager()
        self.validator = InputValidator()

        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="#000000")
        self.main_frame.pack(fill="both", expand=True)

        self.current_user = None
        self.user_key = None
        
        # **KEY CHANGE: Initialize face model once during app startup**
        self.face_model = None
        self._initialize_face_model()

        self.show_login()

        self.fade_overlay = ctk.CTkFrame(self.root, fg_color="#000000")
        self.fade_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.fade_opacity = 1.0
        self.fade_in_app_opening()

    def _initialize_face_model(self):
        """Initialize the face recognition model once during startup"""
        try:
            model_dir = get_model_dir()
            model_root = os.path.dirname(model_dir)
            
            print(f"[INFO] Initializing face model...")
            print(f"[INFO] Model directory: {model_dir}")
            print(f"[INFO] Model root: {model_root}")
            
            # Check if model files exist
            expected_files = ['1k3d68.onnx', '2d106det.onnx', 'det_10g.onnx', 'genderage.onnx', 'w600k_r50.onnx']
            
            if os.path.exists(model_dir):
                existing_files = os.listdir(model_dir)
                missing = [f for f in expected_files if f not in existing_files]
                
                if missing:
                    print(f"[WARNING] Missing model files: {missing}")
                    print(f"[INFO] InsightFace will download missing models automatically...")
                else:
                    print(f"[INFO] All required model files are present: {existing_files}")
            else:
                print(f"[INFO] Model directory doesn't exist. Will be created during model download.")
            
            # Initialize model (this will download models if needed)
            self.face_model = insightface.app.FaceAnalysis(name='buffalo_l')
            self.face_model.prepare(ctx_id=0, det_size=(640, 640))
            print(f"[INFO] Face model initialized successfully!")
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize face model: {e}")
            self.face_model = None

    def fade_in_app_opening(self):
        if self.fade_opacity > 0:
            color = f"#{int(0):02x}{int(0):02x}{int(0):02x}{int(self.fade_opacity*255):02x}"
            try:
                self.fade_overlay.configure(fg_color=color)
            except Exception:
                pass
            self.fade_opacity -= 0.07
            self.root.after(30, self.fade_in_app_opening)
        else:
            self.fade_overlay.destroy()

    def show_login(self):
        self._show_login()

    def _show_login(self):
        LoginPage(self.main_frame, self.show_signup, self.show_home, main_app=self)

    def show_signup(self):
        self._show_signup()

    def _show_signup(self):
        SignupPage(self.main_frame, self.show_login, self.show_home, main_app=self)

    def show_home(self, user_info=None):
        self._show_home(user_info)

    def _show_home(self, user_info=None):
        if user_info:
            self.current_user = user_info
        files = self.db_manager.get_user_files(self.current_user['username'])
        print(f"[DEBUG] Files fetched for {self.current_user['username']}: {[f['filename'] for f in files]}")
        HomePage(
            self.main_frame,
            user_info=self.current_user,
            db_manager=self.db_manager,
            show_home_callback=self.show_home,
            main_app_instance=self
        )

    def show_profile(self):
        self._show_profile()

    def _show_profile(self):
        user_profile = self.db_manager.get_user_profile(self.current_user['username'])
        ProfilePage(self.main_frame, self.db_manager, user_profile, self.show_home, main_app=self)

    def download_file(self, file_doc):
        pw_dialog = PasswordPromptDialog(self.root, "Enter the password to decrypt this file:", confirm=False)
        password = pw_dialog.result

        if not password:
            print("[DEBUG] No password entered for decryption.")
            return

        # **FACE VERIFICATION WITH PRE-INITIALIZED MODEL**
        if not self.verify_face():
            return

        salt = file_doc.get('salt')
        print(f"[DEBUG] Decrypting file: {file_doc.get('filename')} with salt: {salt}")

        if not salt:
            self.show_notification("No salt found for this file. Cannot decrypt.", type="error")
            print("[DEBUG] No salt found in file_doc.")
            return

        if isinstance(salt, str):
            salt = base64.urlsafe_b64decode(salt)

        key = self.derive_key(password, salt)
        print(f"[DEBUG] Derived key for decryption: {key}")
        fernet = Fernet(key)

        try:
            print("[DEBUG] Starting decryption...")
            if self.db_manager.demo_mode:
                decrypted_data = f"This is demo content for {file_doc['filename']}".encode()
                print("[DEBUG] Demo mode: Using dummy decrypted data.")
            else:
                decrypted_data = fernet.decrypt(file_doc['data'])
            print("[DEBUG] Decryption complete.")
        except Exception as e:
            print(f"[DEBUG] Decryption error: {e}")
            self.show_notification(f"Could not decrypt file: {e}\nMake sure you entered the correct password.", type="error")
            return

        FileViewer(self.root, decrypted_data, file_doc['filename'])
        self.show_notification(f"File decrypted and opened in viewer.", type="success")

    def verify_face(self):
        """Verify face using pre-initialized model"""
        if not self.face_model:
            self.show_notification("Face recognition model not initialized. Cannot verify face.", type="error")
            return False

        # 1. Fetch registered face embedding from DB
        face_emb_b64 = self.db_manager.get_user_face_embedding(self.current_user['username'])
        if not face_emb_b64:
            self.show_notification("No registered face embedding found for this user.", type="error")
            return False

        reg_emb = np.frombuffer(base64.b64decode(face_emb_b64), dtype=np.float32)

        # 2. Capture live face using pre-initialized model
        live_face_np, live_emb_b64 = self.capture_live_face_and_embedding()
        if live_face_np is None or live_emb_b64 is None:
            self.show_notification("Live face capture cancelled or failed.", type="error")
            return False

        # 3. Extract embedding from live face
        live_emb = np.frombuffer(base64.b64decode(live_emb_b64), dtype=np.float32)
        similarity = np.dot(reg_emb, live_emb) / (np.linalg.norm(reg_emb) * np.linalg.norm(live_emb))

        if similarity > 0.5:
            return True
        else:
            self.show_notification("Face verification failed. Access denied.", type="error")
            return False

    def capture_live_face(self):
        """Capture live face using pre-initialized model"""
        if not self.face_model:
            self.show_notification("Face recognition model not initialized.", type="error")
            return None

        captured = []
        def on_capture(face_img):
            captured.append(face_img)

        dialog = BiometricScanDialog(self.root, self.face_model, on_capture=on_capture)
        self.root.wait_window(dialog)

        if captured and captured[0] is not None:
            return captured[0]

        self.show_notification("No face detected for verification. Please try again.", type="error")
        return None

    def capture_live_face_and_embedding(self):
        """Capture live face and embedding using pre-initialized model"""
        if not self.face_model:
            self.show_notification("Face recognition model not initialized.", type="error")
            return None, None

        captured = []
        def on_capture(face_img, face_emb):
            captured.append((face_img, face_emb))

        dialog = FaceCaptureDialog(self.root, self.face_model, on_capture=on_capture)
        self.root.wait_window(dialog)

        if captured and captured[0][0] is not None and captured[0][1] is not None:
            return captured[0]

        self.show_notification("No face detected for verification. Please try again.", type="error")
        return None, None

    def derive_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def upload_file(self, username, parent):
        from tkinter.filedialog import askopenfilename

        file_path = askopenfilename(
            title="Select file to encrypt",
            filetypes=[
                ("All Files", "*.*"),
                ("Text Files", "*.txt"),
                ("PDF Files", "*.pdf"),
                ("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
                ("Document Files", "*.doc;*.docx"),
                ("Archive Files", "*.zip;*.rar"),
                ("Audio Files", "*.mp3;*.wav;*.flac"),
                ("Video Files", "*.mp4;*.avi;*.mkv")
            ]
        )

        if not file_path:
            return

        filename = os.path.basename(file_path)
        try:
            with open(file_path, 'rb') as f:
                file_bytes = f.read()
        except Exception as e:
            self.show_notification(f"Could not read file: {str(e)}", type="error")
            return

        max_size = 50 * 1024 * 1024  # 50MB
        if len(file_bytes) > max_size:
            self.show_notification("File size exceeds 50MB limit. Please choose a smaller file.", type="warning")
            return

        pw_dialog = PasswordPromptDialog(self.root, "Enter a password to encrypt this file:", confirm=True)
        password = pw_dialog.result

        if not password:
            return

        salt = os.urandom(16)
        key = self.derive_key(password, salt)
        fernet = Fernet(key)

        try:
            encrypted_bytes = fernet.encrypt(file_bytes)
        except Exception as e:
            self.show_notification(f"Could not encrypt file: {str(e)}", type="error")
            return

        salt_b64 = base64.urlsafe_b64encode(salt).decode()
        user_email = self.current_user.get('email', '') if self.current_user else ''
        print(f"[DEBUG] Uploading file: {filename} for user: {username} (email: {user_email})")

        try:
            self.db_manager.store_file(username, filename, encrypted_bytes, salt_b64, user_email)
            self.show_notification(f"✅ {filename} uploaded and encrypted successfully!", type="success")
            self.show_home(self.current_user)
        except Exception as e:
            self.show_notification(f"Could not store file: {str(e)}", type="error")

    def delete_file(self, file_doc):
        from tkinter import messagebox

        if not file_doc or not file_doc.get('filename'):
            messagebox.showerror("Error", "Invalid file data.")
            return

        filename = file_doc['filename']
        result = messagebox.askyesno(
            "Delete File",
            f"Are you sure you want to permanently delete '{filename}'?\n\nThis action cannot be undone."
        )

        if result:
            try:
                success = self.db_manager.delete_file(self.current_user['username'], filename)
                if success:
                    messagebox.showinfo("File Deleted", f"'{filename}' has been deleted successfully.")
                    self.show_home(self.current_user)
                else:
                    messagebox.showerror("Error", f"Could not delete '{filename}'. File may not exist.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file: {str(e)}")

    def show_notification(self, message, type="info"):
        if hasattr(self, 'notification_bar') and self.notification_bar:
            self.notification_bar.destroy()
            self.notification_bar = None

        colors = {
            "info": ("#2196F3", "ℹ️"),
            "success": ("#43A047", "✅"),
            "error": ("#E53935", "❌"),
            "warning": ("#FFC107", "⚠️"),
        }

        bg_color, icon = colors.get(type, ("#2196F3", "ℹ️"))
        self.notification_bar = ctk.CTkFrame(self.root, fg_color=bg_color, corner_radius=0, height=48)
        self.notification_bar.place(relx=0, rely=0, relwidth=1, y=-48)

        icon_label = ctk.CTkLabel(self.notification_bar, text=icon, font=("Segoe UI", 20, "bold"), text_color="#FFF", width=40)
        icon_label.pack(side="left", padx=(18, 0), pady=0)

        msg_label = ctk.CTkLabel(self.notification_bar, text=message, font=("Segoe UI", 15, "bold"), text_color="#FFF")
        msg_label.pack(side="left", padx=(10, 18), pady=0)

        def slide_down(y=-48):
            if self.notification_bar is not None:
                if y < 0:
                    self.notification_bar.place_configure(y=y)
                    self.root.after(10, lambda: slide_down(y+6))
                else:
                    self.notification_bar.place_configure(y=0)
                    self.root.after(2000, slide_up)

        def slide_up(y=0):
            if self.notification_bar is not None:
                if y > -48:
                    self.notification_bar.place_configure(y=y)
                    self.root.after(10, lambda: slide_up(y-6))
                else:
                    self.notification_bar.destroy()
                    self.notification_bar = None

        slide_down()

    def run(self):
        self.root.mainloop()

def main():
    app = MainApp()
    app.run()

if __name__ == "__main__":
    main()
