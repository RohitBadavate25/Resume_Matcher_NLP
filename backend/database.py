import sqlite3
import json
from datetime import datetime
import uuid
import os

class Database:
    def __init__(self, db_path='resume_matcher.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create job_descriptions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_descriptions (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                company TEXT,
                description TEXT NOT NULL,
                requirements TEXT,
                recruiter_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create resumes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumes (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                candidate_name TEXT,
                candidate_email TEXT,
                content TEXT NOT NULL,
                file_path TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create matches table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                resume_id TEXT NOT NULL,
                similarity_score REAL,
                common_skills TEXT,
                missing_skills TEXT,
                match_details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES job_descriptions (id),
                FOREIGN KEY (resume_id) REFERENCES resumes (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    # Job Description methods
    def create_job_description(self, title, company, description, requirements, recruiter_name):
        """Create a new job description"""
        job_id = str(uuid.uuid4())
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO job_descriptions (id, title, company, description, requirements, recruiter_name)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (job_id, title, company, description, requirements, recruiter_name))
        
        conn.commit()
        conn.close()
        return job_id
    
    def get_job_descriptions(self):
        """Get all job descriptions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM job_descriptions ORDER BY created_at DESC')
        rows = cursor.fetchall()
        
        job_descriptions = []
        for row in rows:
            job_descriptions.append({
                'id': row[0],
                'title': row[1],
                'company': row[2],
                'description': row[3],
                'requirements': row[4],
                'recruiter_name': row[5],
                'created_at': row[6]
            })
        
        conn.close()
        return job_descriptions
    
    def get_job_description(self, job_id):
        """Get a specific job description"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM job_descriptions WHERE id = ?', (job_id,))
        row = cursor.fetchone()
        
        if row:
            job_desc = {
                'id': row[0],
                'title': row[1],
                'company': row[2],
                'description': row[3],
                'requirements': row[4],
                'recruiter_name': row[5],
                'created_at': row[6]
            }
        else:
            job_desc = None
        
        conn.close()
        return job_desc
    
    # Resume methods
    def create_resume(self, filename, candidate_name, candidate_email, content, file_path):
        """Create a new resume record"""
        resume_id = str(uuid.uuid4())
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO resumes (id, filename, candidate_name, candidate_email, content, file_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (resume_id, filename, candidate_name, candidate_email, content, file_path))
        
        conn.commit()
        conn.close()
        return resume_id
    
    def get_resumes(self):
        """Get all resumes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM resumes ORDER BY uploaded_at DESC')
        rows = cursor.fetchall()
        
        resumes = []
        for row in rows:
            resumes.append({
                'id': row[0],
                'filename': row[1],
                'candidate_name': row[2],
                'candidate_email': row[3],
                'content': row[4],
                'file_path': row[5],
                'uploaded_at': row[6]
            })
        
        conn.close()
        return resumes
    
    def get_resume(self, resume_id):
        """Get a specific resume"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM resumes WHERE id = ?', (resume_id,))
        row = cursor.fetchone()
        
        if row:
            resume = {
                'id': row[0],
                'filename': row[1],
                'candidate_name': row[2],
                'candidate_email': row[3],
                'content': row[4],
                'file_path': row[5],
                'uploaded_at': row[6]
            }
        else:
            resume = None
        
        conn.close()
        return resume
    
    # Match methods
    def create_match(self, job_id, resume_id, similarity_score, common_skills, missing_skills, match_details):
        """Create a new match record"""
        match_id = str(uuid.uuid4())
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO matches (id, job_id, resume_id, similarity_score, common_skills, missing_skills, match_details)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (match_id, job_id, resume_id, similarity_score, 
              json.dumps(common_skills), json.dumps(missing_skills), json.dumps(match_details)))
        
        conn.commit()
        conn.close()
        return match_id
    
    def get_matches_for_job(self, job_id):
        """Get all matches for a specific job"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.*, r.filename, r.candidate_name, r.candidate_email
            FROM matches m
            JOIN resumes r ON m.resume_id = r.id
            WHERE m.job_id = ?
            ORDER BY m.similarity_score DESC
        ''', (job_id,))
        
        rows = cursor.fetchall()
        matches = []
        for row in rows:
            matches.append({
                'id': row[0],
                'job_id': row[1],
                'resume_id': row[2],
                'similarity_score': row[3],
                'common_skills': json.loads(row[4]) if row[4] else [],
                'missing_skills': json.loads(row[5]) if row[5] else [],
                'match_details': json.loads(row[6]) if row[6] else {},
                'created_at': row[7],
                'filename': row[8],
                'candidate_name': row[9],
                'candidate_email': row[10]
            })
        
        conn.close()
        return matches
    
    def get_all_matches(self):
        """Get all matches"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.*, j.title as job_title, r.filename, r.candidate_name
            FROM matches m
            JOIN job_descriptions j ON m.job_id = j.id
            JOIN resumes r ON m.resume_id = r.id
            ORDER BY m.created_at DESC
        ''')
        
        rows = cursor.fetchall()
        matches = []
        for row in rows:
            matches.append({
                'id': row[0],
                'job_id': row[1],
                'resume_id': row[2],
                'similarity_score': row[3],
                'common_skills': json.loads(row[4]) if row[4] else [],
                'missing_skills': json.loads(row[5]) if row[5] else [],
                'match_details': json.loads(row[6]) if row[6] else {},
                'created_at': row[7],
                'job_title': row[8],
                'filename': row[9],
                'candidate_name': row[10]
            })
        
        conn.close()
        return matches
