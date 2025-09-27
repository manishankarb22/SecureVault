import pymongo
from datetime import datetime
from typing import Tuple
from security import SecurityManager
from config import config

class DatabaseManager:
    def __init__(self):
        # Connect to the same MongoDB database for both users and files
        # Database: secure_vault_complete
        # Users collection: users
        # Files collection: files
        self.demo_mode = config.demo_mode or True  # Default to demo mode if no config
        try:
            self.client = pymongo.MongoClient(config.mongodb_uri, serverSelectionTimeoutMS=config.mongodb_timeout)
            self.client.server_info()
            self.db = self.client[config.mongodb_database]
            self.users_collection = self.db['users']
            # Ensure unique indexes for username and email
            self.users_collection.create_index('username', unique=True)
            self.users_collection.create_index('email', unique=True)
            self.demo_mode = False
        except:
            print("Running in demo mode")

    def create_user(self, username: str, email: str, password_hash: str, face_b64: str = None, face_emb_b64: str = None) -> Tuple[bool, str]:
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
            if face_b64:
                user_data['face_image'] = face_b64
            if face_emb_b64:
                user_data['face_embedding'] = face_emb_b64
            self.users_collection.insert_one(user_data)
            return True, "Account created successfully!"
        except pymongo.errors.DuplicateKeyError:
            return False, "Username or email already exists"
        except Exception as e:
            return False, f"Failed to create account: {str(e)}"

    def authenticate_user(self, username: str, password: str):
        if self.demo_mode:
            return {'username': username, 'email': f'{username}@example.com'}
        user = self.users_collection.find_one({'username': username, 'is_active': True})
        if user and SecurityManager.verify_password(password, user['password_hash']):
            return {'username': user['username'], 'email': user['email']}
        return None

    def store_file(self, username, filename, file_bytes, salt_b64, user_email):
        if self.demo_mode:
            print(f"[DEMO MODE] File '{filename}' not stored in MongoDB.")
            return True
        file_doc = {
            'username': username,
            'user_email': user_email,
            'filename': filename,
            'data': file_bytes,  # Encrypted data
            'upload_date': datetime.utcnow(),
            'size_bytes': len(file_bytes),
            'salt': salt_b64
        }
        self.db['files'].insert_one(file_doc)
        print(f"[MongoDB] File '{filename}' stored for user '{username}' in 'secure_vault_complete.files'.")
        return True

    def get_user_files(self, username):
        import os, base64
        if self.demo_mode:
            # Return multiple example files for better demo
            files = [
                {'filename': 'example.txt', 'upload_date': datetime.utcnow(), 'size_bytes': 1234, 'salt': base64.urlsafe_b64encode(os.urandom(16)).decode()},
                {'filename': 'document.pdf', 'upload_date': datetime.utcnow(), 'size_bytes': 5678, 'salt': base64.urlsafe_b64encode(os.urandom(16)).decode()},
                {'filename': 'image.jpg', 'upload_date': datetime.utcnow(), 'size_bytes': 9876, 'salt': base64.urlsafe_b64encode(os.urandom(16)).decode()}
            ]
            print(f"[DEBUG] get_user_files (demo) for {username}: {[f['filename'] for f in files]}")
            return files
        files = list(self.db['files'].find({'username': username}))
        print(f"[DEBUG] get_user_files for {username}: {[f['filename'] for f in files]}")
        return files

    # NEW METHOD: Delete file functionality
    def delete_file(self, username, filename):
        if self.demo_mode:
            print(f"[DEMO MODE] File '{filename}' deletion simulated for user '{username}'.")
            return True

        try:
            result = self.db['files'].delete_one({'username': username, 'filename': filename})
            if result.deleted_count > 0:
                print(f"[MongoDB] File '{filename}' deleted for user '{username}'.")
                return True
            else:
                print(f"[MongoDB] File '{filename}' not found for user '{username}'.")
                return False
        except Exception as e:
            print(f"[MongoDB] Error deleting file '{filename}': {str(e)}")
            return False

    def user_storage_stats(self, username):
        if self.demo_mode:
            return {
                'file_count': 3,
                'total_bytes': 1234 + 5678 + 9876,
                'by_ext': {
                    'txt': {'count': 1, 'bytes': 1234},
                    'pdf': {'count': 1, 'bytes': 5678},
                    'jpg': {'count': 1, 'bytes': 9876}
                },
                'largest': {'filename': 'image.jpg', 'size_bytes': 9876}
            }
        files = list(self.db['files'].find({'username': username}))
        file_count = len(files)
        total_bytes = sum(f.get('size_bytes', 0) for f in files)
        by_ext = {}
        largest = None
        for f in files:
            ext = f['filename'].split('.')[-1].lower() if '.' in f['filename'] else 'other'
            by_ext.setdefault(ext, {'count': 0, 'bytes': 0})
            by_ext[ext]['count'] += 1
            by_ext[ext]['bytes'] += f.get('size_bytes', 0)
            if not largest or f.get('size_bytes', 0) > largest.get('size_bytes', 0):
                largest = {'filename': f['filename'], 'size_bytes': f.get('size_bytes', 0)}
        return {
            'file_count': file_count,
            'total_bytes': total_bytes,
            'by_ext': by_ext,
            'largest': largest
        }

    def get_user_profile(self, username):
        if self.demo_mode:
            return {'username': username, 'email': f'{username}@example.com', 'avatar': None}
        user = self.users_collection.find_one({'username': username})
        if user:
            user.pop('_id', None)
        return user

    def is_username_taken(self, username: str) -> bool:
        if self.demo_mode:
            return username.lower() == 'demo'
        return self.users_collection.find_one({'username': username}) is not None

    def is_email_taken(self, email: str) -> bool:
        if self.demo_mode:
            return email.lower() == 'demo@example.com'
        return self.users_collection.find_one({'email': email.lower()}) is not None

    def get_user_by_username(self, username: str):
        if self.demo_mode:
            return {'username': username, 'email': f'{username}@example.com'}
        user = self.users_collection.find_one({'username': username})
        if user:
            user.pop('_id', None)
        return user

    def get_user_face_embedding(self, username: str):
        if self.demo_mode:
            return None
        user = self.users_collection.find_one({'username': username})
        if user and 'face_embedding' in user:
            return user['face_embedding']
        return None
 