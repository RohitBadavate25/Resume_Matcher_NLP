# Setup Instructions for ResumeMatch

This guide will help you set up the ResumeMatch application on your local machine or deploy it to a production environment.

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software
- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Node.js 14 or higher** - [Download Node.js](https://nodejs.org/)
- **npm** (comes with Node.js) or **yarn**
- **Git** - [Download Git](https://git-scm.com/)

### System Requirements
- **RAM**: Minimum 4GB (8GB recommended for better performance)
- **Storage**: At least 2GB free space
- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)

## 🚀 Installation Guide

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Resume_Matcher
```

### Step 2: Backend Setup

#### 2.1 Navigate to Backend Directory
```bash
cd backend
```

#### 2.2 Create Virtual Environment
**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2.3 Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2.4 Download NLTK Data
```bash
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True)"
```

#### 2.5 Install spaCy Model (Optional but Recommended)
```bash
python -m spacy download en_core_web_sm
```
*Note: If this fails, the application will still work but with slightly reduced NLP capabilities.*

#### 2.6 Test Backend Installation
```bash
python app.py
```
You should see output similar to:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Press `Ctrl+C` to stop the server.

### Step 3: Frontend Setup

#### 3.1 Navigate to Frontend Directory
Open a new terminal window/tab and navigate to the frontend directory:
```bash
cd frontend
```

#### 3.2 Install Node.js Dependencies
```bash
npm install
```

#### 3.3 Test Frontend Installation
```bash
npm start
```
Your browser should automatically open to `http://localhost:3000`.

## 🔧 Configuration

### Backend Configuration

#### Environment Variables
Create a `.env` file in the backend directory (optional):
```bash
FLASK_ENV=development
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

#### File Upload Settings
By default, the application supports:
- **File Types**: PDF, DOC, DOCX, TXT
- **Max File Size**: 16MB
- **Upload Directory**: `backend/uploads/`

To modify these settings, edit the configuration section in `backend/app.py`:
```python
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

### Frontend Configuration

#### API Endpoint Configuration
If your backend runs on a different port or domain, update the API base URL in `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

#### Styling Customization
To customize the UI colors and theme, edit `frontend/tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom colors here
      }
    }
  }
}
```

## 🚀 Running the Application

### Development Mode

#### Option 1: Manual Start (Recommended for Development)

**Terminal 1 - Backend:**
```bash
cd backend
# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

#### Option 2: Using the Startup Script

I'll create a startup script for easier development:

**On Windows:**
Create `start_dev.bat`:
```batch
@echo off
echo Starting ResumeMatch Development Environment...

echo.
echo Starting Backend Server...
start cmd /k "cd /d backend && venv\Scripts\activate && python app.py"

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo Starting Frontend Server...
start cmd /k "cd /d frontend && npm start"

echo.
echo Both servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
pause
```

**On macOS/Linux:**
Create `start_dev.sh`:
```bash
#!/bin/bash
echo "Starting ResumeMatch Development Environment..."

echo ""
echo "Starting Backend Server..."
osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/backend && source venv/bin/activate && python app.py"'

echo ""
echo "Waiting for backend to start..."
sleep 5

echo ""
echo "Starting Frontend Server..."
osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/frontend && npm start"'

echo ""
echo "Both servers are starting..."
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
```

Make it executable:
```bash
chmod +x start_dev.sh
```

### Production Mode

For production deployment, you'll need additional configuration:

#### Backend Production Setup
1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Create `gunicorn.conf.py`:
```python
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
timeout = 30
max_requests = 1000
max_requests_jitter = 100
```

3. Run with Gunicorn:
```bash
gunicorn -c gunicorn.conf.py app:app
```

#### Frontend Production Build
1. Build the production version:
```bash
cd frontend
npm run build
```

2. Serve the built files using a web server like nginx or Apache.

## 🔍 Troubleshooting

### Common Issues

#### Backend Issues

**Issue: ModuleNotFoundError for NLTK or spaCy**
```bash
# Solution: Reinstall dependencies
pip install --force-reinstall nltk spacy
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

**Issue: spaCy model not found**
```bash
# Solution: Download the English model
python -m spacy download en_core_web_sm
```

**Issue: Permission denied on file upload**
```bash
# Solution: Check upload directory permissions
mkdir -p backend/uploads
chmod 755 backend/uploads
```

#### Frontend Issues

**Issue: npm install fails**
```bash
# Solution: Clear npm cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Issue: Port 3000 already in use**
```bash
# Solution: Use a different port
PORT=3001 npm start
```

**Issue: API connection refused**
- Ensure backend server is running on port 5000
- Check firewall settings
- Verify CORS configuration in backend

### Performance Issues

**Slow processing times:**
1. Ensure you have adequate RAM (8GB recommended)
2. Close unnecessary applications
3. Consider using lighter NLP models for development

**High memory usage:**
1. Restart the application periodically during heavy testing
2. Limit the number of large files processed simultaneously
3. Monitor system resources

### Development Tips

1. **Hot Reloading**: Both servers support hot reloading during development
2. **Debugging**: Use `console.log()` in frontend and `print()` or `logger` in backend
3. **Testing**: Test with small files first before processing large documents
4. **Browser DevTools**: Use Network tab to monitor API calls

## 📚 Additional Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [NLTK Documentation](https://www.nltk.org/)

### Useful Commands

**Backend Commands:**
```bash
# Install specific package
pip install package_name

# Update requirements.txt
pip freeze > requirements.txt

# Check Python version
python --version

# Test API endpoint
curl http://localhost:5000/api/health
```

**Frontend Commands:**
```bash
# Install specific package
npm install package_name

# Update all packages
npm update

# Check for security vulnerabilities
npm audit

# Build for production
npm run build
```

## 🆘 Getting Help

If you encounter issues not covered in this guide:

1. **Check the logs**: Both servers provide detailed error messages
2. **Verify prerequisites**: Ensure all required software is properly installed
3. **Test components individually**: Test backend and frontend separately
4. **Check network connectivity**: Ensure no firewall blocks local connections
5. **Review the README**: Check the main README.md for additional information

### Support Channels
- Create an issue in the repository with detailed error messages
- Include your operating system, Python version, and Node.js version
- Provide steps to reproduce the problem
- Include relevant log output

---

Happy coding! 🚀
