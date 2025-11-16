#!/usr/bin/env python3
"""
Quick setup script for the Enhanced Resume Matcher
Handles installation with better error handling for Python 3.13+
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package with better error handling"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to install {package}: {e}")
        return False

def install_requirements():
    """Install packages one by one with fallbacks"""
    
    # Core packages (required)
    core_packages = [
        "Flask>=2.3.3",
        "Flask-CORS>=4.0.0", 
        "numpy",  # Let pip choose compatible version
        "scikit-learn",
        "nltk>=3.8.1",
        "PyPDF2>=3.0.1",
        "python-docx>=0.8.11",
        "Werkzeug>=2.3.7"
    ]
    
    # Enhanced packages (optional)
    enhanced_packages = [
        "sentence-transformers",  # For BERT functionality
        "pandas",
        "matplotlib", 
        "seaborn",
        "scipy"
    ]
    
    print("🚀 Installing Resume Matcher Enhanced Dependencies")
    print("=" * 60)
    
    # Install core packages
    print("📦 Installing core packages...")
    failed_core = []
    for package in core_packages:
        print(f"Installing {package}...")
        if not install_package(package):
            failed_core.append(package)
    
    if failed_core:
        print(f"❌ Failed to install core packages: {failed_core}")
        print("The basic system may not work properly.")
    else:
        print("✅ Core packages installed successfully!")
    
    # Install enhanced packages
    print("\\n🤖 Installing enhanced packages...")
    failed_enhanced = []
    for package in enhanced_packages:
        print(f"Installing {package}...")
        if not install_package(package):
            failed_enhanced.append(package)
    
    if failed_enhanced:
        print(f"⚠️ Failed to install enhanced packages: {failed_enhanced}")
        print("The system will work but some advanced features may be unavailable.")
    else:
        print("✅ All enhanced packages installed successfully!")
    
    # Download NLTK data
    print("\\n📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True) 
        nltk.download('wordnet', quiet=True)
        print("✅ NLTK data downloaded successfully!")
    except Exception as e:
        print(f"⚠️ NLTK data download failed: {e}")
    
    print("\\n🎉 Setup completed!")
    print("\\nTo test the enhanced system, run:")
    print("  python test_improvements.py")
    print("\\nTo start the server:")
    print("  python app.py")

if __name__ == "__main__":
    install_requirements()