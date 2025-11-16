import sqlite3
import json

def inspect_database():
    """Inspect what's actually in the database"""
    
    db_path = 'resume_matcher.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("📊 Database Contents Inspection")
    print("=" * 60)
    
    # Check job descriptions
    print("\n📋 Job Descriptions:")
    cursor.execute("SELECT id, title, company, description, requirements FROM job_descriptions")
    jobs = cursor.fetchall()
    
    for i, (job_id, title, company, desc, req) in enumerate(jobs, 1):
        print(f"\n{i}. {title} at {company}")
        print(f"   ID: {job_id}")
        print(f"   Description: '{desc[:100]}{'...' if len(desc) > 100 else ''}'")
        print(f"   Requirements: '{req[:100]}{'...' if len(req) > 100 else ''}'")
        print(f"   Total length: {len(desc)} chars")
    
    # Check resumes
    print(f"\n📄 Resumes:")
    cursor.execute("SELECT id, candidate_name, filename, content FROM resumes")
    resumes = cursor.fetchall()
    
    for i, (resume_id, name, filename, content) in enumerate(resumes, 1):
        print(f"\n{i}. {name}")
        print(f"   ID: {resume_id}")
        print(f"   Filename: {filename}")
        print(f"   Content preview: '{content[:200]}{'...' if len(content) > 200 else ''}'")
        print(f"   Total length: {len(content)} chars")
    
    conn.close()

if __name__ == "__main__":
    inspect_database()