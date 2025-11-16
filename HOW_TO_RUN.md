# Resume Matcher - How to Run

## 🚀 Quick Start Guide

Follow these steps to run the Resume Matcher application:

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

## 📁 Project Structure
```
Resume_Matcher/
├── backend/          # Flask API server
├── frontend/         # React application
├── setup.bat         # Windows setup script
└── start_dev.bat     # Development startup script
```

## 🛠️ Setup Instructions

### Option 1: Automated Setup (Recommended)
1. **Open PowerShell as Administrator**
2. **Navigate to project directory:**
   ```powershell
   cd "C:\Users\rohit\OneDrive\Projects\Resume_Matcher"
   ```
3. **Run setup script:**
   ```powershell
   .\setup.bat
   ```
4. **Start development servers:**
   ```powershell
   .\start_dev.bat
   ```

### Option 2: Manual Setup

#### Backend Setup
1. **Navigate to backend directory:**
   ```powershell
   cd "C:\Users\rohit\OneDrive\Projects\Resume_Matcher\backend"
   ```

2. **Create virtual environment:**
   ```powershell
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. **Install Python dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Install spaCy model:**
   ```powershell
   python -m spacy download en_core_web_sm
   ```

6. **Start Flask server:**
   ```powershell
   python app.py
   ```
   Server will run on: http://127.0.0.1:5000

#### Frontend Setup
1. **Open new PowerShell terminal**
2. **Navigate to frontend directory:**
   ```powershell
   cd "C:\Users\rohit\OneDrive\Projects\Resume_Matcher\frontend"
   ```

3. **Install Node.js dependencies:**
   ```powershell
   npm install
   ```

4. **Start React development server:**
   ```powershell
   npm start
   ```
   Application will open at: http://localhost:3000

## 🎯 Accessing the Application

### URLs:
- **Frontend (React):** http://localhost:3000
- **Backend API:** http://127.0.0.1:5000
- **API Documentation:** http://127.0.0.1:5000/api/docs (if available)

### User Roles:
1. **Recruiters:** Post job descriptions and view candidate matches
2. **Candidates:** Upload resumes and view job matches

## 🔧 Development Commands

### Backend Commands:
```powershell
# Navigate to backend
cd "C:\Users\rohit\OneDrive\Projects\Resume_Matcher\backend"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run Flask app
python app.py

# Run tests
python test_real_world.py
python test_final_validation.py

# Debug NLP issues
python diagnose_nlp.py
```

### Frontend Commands:
```powershell
# Navigate to frontend
cd "C:\Users\rohit\OneDrive\Projects\Resume_Matcher\frontend"

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## 🐛 Troubleshooting

### Common Issues:

1. **Python Virtual Environment Issues:**
   ```powershell
   # If activation fails, try:
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Port Already in Use:**
   ```powershell
   # Kill process on port 5000 (Flask)
   netstat -ano | findstr :5000
   taskkill /PID <PID_NUMBER> /F
   
   # Kill process on port 3000 (React)
   netstat -ano | findstr :3000
   taskkill /PID <PID_NUMBER> /F
   ```

3. **Missing Dependencies:**
   ```powershell
   # Backend
   pip install flask flask-cors PyPDF2 python-docx scikit-learn nltk spacy

   # Frontend
   npm install react react-dom react-router-dom axios
   ```

4. **Database Issues:**
   - Database file: `backend/resume_matcher.db`
   - Delete and restart if corrupted

## 📊 Testing the Application

### Test with Quality Data:
```powershell
cd "C:\Users\rohit\OneDrive\Projects\Resume_Matcher\backend"
python test_quality_job.py
```

### Check NLP Performance:
```powershell
python test_real_world.py
```

## 🎉 Success Indicators

✅ **Backend Running Successfully:**
- Console shows: "Running on http://127.0.0.1:5000"
- No error messages
- Database initialized with existing data

✅ **Frontend Running Successfully:**
- Browser opens automatically to http://localhost:3000
- Home page loads with navigation buttons
- No console errors in browser

✅ **Full System Working:**
- Can navigate between Recruiter and Candidate dashboards
- Can upload resumes and post job descriptions
- Matching functionality returns results > 0%

## 🔄 Development Workflow

1. **Make backend changes** → Flask auto-reloads
2. **Make frontend changes** → React hot-reloads
3. **Test API changes** → Use test scripts or browser network tab
4. **Check logs** → Monitor terminal outputs for errors

## 📝 Notes

- Flask runs in debug mode for development
- React development server has hot reload enabled
- Database persists between runs
- Uploaded files stored in `backend/uploads/`
- NLP models downloaded automatically on first run

---

**Ready to start? Run the setup commands above and your Resume Matcher will be live!** 🚀