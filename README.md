# 🔐 SecureVault - Biometric File Security System

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB" />
  <img src="https://img.shields.io/badge/Face-Recognition-FF6B6B?style=for-the-badge&logo=security&logoColor=white" alt="Face Recognition" />
  <img src="https://img.shields.io/badge/Encryption-AES-4CAF50?style=for-the-badge&logo=shield&logoColor=white" alt="Encryption" />
  <img src="https://img.shields.io/badge/CustomTkinter-UI-2196F3?style=for-the-badge&logo=gui&logoColor=white" alt="CustomTkinter" />
</div>

A cutting-edge secure file vault application that combines **biometric face authentication**, **military-grade encryption**, and **modern UI design** for ultimate file security. Built with Python and featuring an Iron Man-inspired black & orange theme.

## ✨ Features

### 🛡️ **Security Features**
- **🔐 Biometric Authentication**: InsightFace-powered face recognition for secure access
- **🔒 File Encryption**: Fernet symmetric encryption for all stored files
- **🔑 Password Security**: bcrypt hashing with configurable salt rounds
- **👤 User Isolation**: Each user's files are completely isolated and encrypted
- **🚫 Zero Plaintext**: No sensitive data stored in plaintext anywhere

### 🎨 **User Interface**
- **🌃 Modern Dark Theme**: Iron Man-inspired black background with orange accents
- **📱 Responsive Design**: Smooth animations and modern UI components
- **📊 Dashboard Analytics**: File storage statistics and usage insights
- **🔔 Smart Notifications**: Animated notification bars for user feedback
- **🖼️ Avatar Management**: Encrypted profile pictures with cropping functionality

### 📁 **File Management**
- **📤 Secure Upload**: Drag-and-drop file encryption and storage
- **📥 Biometric Access**: Face scan required for file decryption
- **🔍 Smart Search**: Real-time file search and filtering
- **📊 Storage Analytics**: File type analysis and storage statistics
- **🗑️ Secure Deletion**: Complete file removal with secure cleanup

### 🔬 **Technical Excellence**
- **⚡ Modular Architecture**: Clean, maintainable codebase structure
- **🏃 Demo Mode**: Run without MongoDB for testing and demonstrations
- **⚙️ Environment Configuration**: Secure configuration management
- **🔧 Extensible Design**: Easy to add new features and integrations

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   CustomTkinter │◄──►│   SecureVault   │◄──►│    MongoDB      │
│     GUI         │    │   Application   │    │   Database      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│  Face Detection │    │   File System   │    │  User Profiles  │
│  & Recognition  │    │   Encryption    │    │ & Authentication│
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **MongoDB** (Optional - has demo mode) - [Download here](https://www.mongodb.com/try/download/community)
- **Webcam** - Required for face authentication
- **Git** - [Download here](https://git-scm.com/downloads)

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/manishankarb22/SecureVault.git
cd SecureVault
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment (Optional)
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configurations
```

**Environment Configuration (.env):**
```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=secure_vault_complete
MONGODB_TIMEOUT=3000

# Security Configuration
ENCRYPTION_KEY=your-secret-encryption-key-here
JWT_SECRET=your-jwt-secret-key-here
BCRYPT_ROUNDS=12

# Application Settings
DEBUG=False
DEMO_MODE=False

# Face Recognition Settings
FACE_CONFIDENCE_THRESHOLD=0.7
FACE_MODEL_PATH=./models/buffalo_l/
```

#### 5. Setup Database (Optional)

**Option A: Demo Mode (No Database Required)**
- The application runs in demo mode by default
- No MongoDB setup needed for testing

**Option B: Production Setup**
1. Install and start MongoDB
2. Update `.env` file with your MongoDB URI
3. Set `DEMO_MODE=False` in `.env`

### 🏃‍♂️ Running the Application

#### Quick Start (Demo Mode)
```bash
python main.py
```

#### Production Mode
```bash
# Ensure MongoDB is running
# Windows
net start MongoDB

# macOS (with Homebrew)
brew services start mongodb-community

# Linux
sudo systemctl start mongod

# Run the application
python main.py
```

## 📱 Usage Guide

### 🔐 **Getting Started**

1. **First Launch**: Run `python main.py`
2. **Create Account**: Click "Sign Up" and complete biometric enrollment
3. **Face Capture**: Allow camera access for face authentication setup
4. **Login**: Use your credentials + face scan to access your vault

### 📁 **File Management**

1. **Upload Files**: 
   - Drag and drop files or use the upload button
   - Files are automatically encrypted before storage
   
2. **Access Files**:
   - Enter your password
   - Complete face scan authentication
   - Files are decrypted and made available

3. **File Operations**:
   - **Search**: Use the search bar to find files quickly
   - **Delete**: Select files and delete securely
   - **Analytics**: View storage statistics and file breakdowns

### 👤 **Profile Management**

- **Avatar**: Upload and crop encrypted profile pictures
- **Edit Profile**: Update account information
- **Change Password**: Secure password modification
- **Security Settings**: Manage authentication preferences

## 🔧 Project Structure

```
SecureVault/
├── 📄 main.py              # Application entry point & navigation
├── 🔐 security.py          # Encryption & password hashing
├── 🗄️ database.py          # MongoDB operations & file storage
├── 🔑 login.py             # Authentication interface
├── ✍️ signup.py            # Account creation & biometric enrollment
├── 🏠 home.py              # File management dashboard
├── 👤 profile.py           # Profile & settings management
├── 🎥 file_viewer.py       # File preview & viewing
├── ⚙️ config.py            # Configuration management
├── 📋 requirements.txt     # Python dependencies
├── 🚫 .gitignore          # Git ignore rules
├── 🔧 .env.example        # Environment template
└── 📁 models/             # Face recognition models
    └── buffalo_l/         # InsightFace model files
```

## 🛠️ Technical Specifications

### **Security Implementation**

- **Encryption Algorithm**: Fernet (AES 128 in CBC mode with HMAC)
- **Password Hashing**: bcrypt with configurable salt rounds (default: 12)
- **Face Recognition**: InsightFace with cosine similarity matching
- **Database Security**: Encrypted storage of all sensitive data
- **Session Management**: Secure authentication state handling

### **Supported File Types**

- **Documents**: `.txt`, `.pdf`, `.docx`, `.xlsx`, `.pptx`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`
- **Archives**: `.zip`, `.rar`, `.7z`
- **Media**: `.mp4`, `.mp3`, `.wav`
- **Custom**: Configurable via environment variables

### **System Requirements**

- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB for models + user data
- **Camera**: Any USB/built-in webcam for face recognition
- **Network**: Internet connection for initial model download

## 🔍 Advanced Features

### **Biometric Security Flow**

1. **Enrollment**: Face capture → Feature extraction → Encrypted storage
2. **Authentication**: Live capture → Feature matching → Access decision
3. **Anti-Spoofing**: Liveness detection and quality checks
4. **Privacy**: Face data never stored in plaintext

### **File Encryption Process**

1. **Upload**: File → Salt generation → Fernet encryption → MongoDB storage
2. **Access**: Authentication → Key derivation → Decryption → Temporary access
3. **Cleanup**: Automatic temporary file cleanup after use

### **Demo Mode Features**

- **No Database Required**: Runs entirely in memory
- **Sample Data**: Pre-populated with example files
- **Full Functionality**: All features work except persistent storage
- **Development Friendly**: Perfect for testing and development

## 🚨 Troubleshooting

### **Common Issues**

**1. Face Recognition Not Working**
```bash
# Check camera permissions
# Verify webcam is not in use by other applications
# Ensure adequate lighting for face detection
```

**2. MongoDB Connection Issues**
```bash
# Check if MongoDB is running
mongod --version

# Start MongoDB service
# Windows: net start MongoDB
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongod
```

**3. Missing Dependencies**
```bash
# Update pip and reinstall
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**4. Model Download Issues**
```bash
# Clear model cache and re-download
rm -rf models/
python main.py  # Will auto-download models
```

### **Performance Optimization**

- **Large Files**: Use compression before encryption for better performance
- **Multiple Users**: Consider MongoDB indexing for better query performance
- **Memory Usage**: Close unused file previews to free memory
- **Face Recognition**: Ensure good lighting for faster authentication

## 🔐 Security Best Practices

### **For Developers**
- Never commit the `.env` file to version control
- Use strong encryption keys (minimum 32 characters)
- Regularly update dependencies for security patches
- Implement proper error handling to avoid information leakage

### **For Users**
- Use a strong master password (12+ characters)
- Ensure good lighting during face registration
- Regularly backup your encrypted data
- Don't share your account credentials

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### **Development Setup**
```bash
# Clone your fork
git clone https://github.com/your-username/SecureVault.git

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black .
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[InsightFace](https://github.com/deepinsight/insightface)** - Powerful face recognition framework
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - Modern UI framework for Python
- **[MongoDB](https://www.mongodb.com/)** - Flexible document database
- **[Cryptography](https://cryptography.io/)** - Robust encryption library
- **[bcrypt](https://github.com/pyca/bcrypt/)** - Secure password hashing

## 📞 Support

If you encounter any issues or have questions:

1. **Check** the [Issues](https://github.com/manishankarb22/SecureVault/issues) page
2. **Search** existing issues before creating a new one
3. **Provide** detailed information including:
   - Operating system and version
   - Python version
   - Error messages and logs
   - Steps to reproduce the issue

## 🔮 Future Enhancements

- **🌐 Web Interface**: Browser-based access portal
- **📱 Mobile App**: iOS and Android companion apps
- **🔗 Cloud Integration**: Support for cloud storage providers
- **🛡️ Multi-Factor Auth**: Additional security layers
- **👥 Team Features**: Shared vaults and collaboration tools
- **🔄 Auto-Backup**: Automated encrypted backups
- **📊 Advanced Analytics**: Detailed usage and security analytics

---

<div align="center">
  <strong>Built with ❤️ for Security & Privacy</strong>
  <br />
  <a href="https://github.com/manishankarb22">Made by manishankarb22</a>
</div>
#   S e c u r e V a u l t  
 