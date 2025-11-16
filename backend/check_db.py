#!/usr/bin/env python3

from database import Database
import sqlite3

def check_database():
    """Check database structure and content"""
    try:
        db = Database()
        print("✅ Database connected successfully")
        
        # Check tables using direct connection
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Tables found: {[table[0] for table in tables]}")
        
        # Check job descriptions count
        cursor.execute("SELECT COUNT(*) FROM job_descriptions")
        job_count = cursor.fetchone()[0]
        print(f"📝 Job descriptions: {job_count}")
        
        # Check resumes count
        cursor.execute("SELECT COUNT(*) FROM resumes")
        resume_count = cursor.fetchone()[0]
        print(f"📄 Resumes: {resume_count}")
        
        conn.close()
        
        # If empty, let's check if we can add some test data
        if job_count == 0 and resume_count == 0:
            print("⚠️  Database is empty. This explains the 'failed to fetch resumes' error.")
            print("💡 The application needs data to function properly.")
            
        return True
        
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
        return False

if __name__ == "__main__":
    check_database()