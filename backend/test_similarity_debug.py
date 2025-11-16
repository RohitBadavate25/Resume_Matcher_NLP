#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nlp_processor import ResumeMatcherNLP
from database import Database

def test_similarity():
    try:
        print("Testing similarity calculation...")
        
        # Initialize components
        nlp = ResumeMatcherNLP()
        db = Database()
        
        # Get some test data
        jobs = db.get_job_descriptions()
        resumes = db.get_resumes()
        
        if not jobs or not resumes:
            print("No jobs or resumes found!")
            return
            
        job = jobs[0]
        resume = resumes[0]
        
        print(f"Job ID: {job['id']}")
        print(f"Resume ID: {resume['id']}")
        
        # Process the data
        job_content = f"{job['description']} {job['requirements']}"
        nlp.process_job_description(job['id'], job_content)
        nlp.process_resume(resume['id'], resume['content'])
        
        # Fit vectorizers
        if len(nlp.all_texts) >= 2:
            nlp.fit_corpus_vectorizers()
            
        # Calculate similarity
        print("Calculating similarity...")
        similarity = nlp.calculate_similarity(job['id'], resume['id'])
        print(f"Similarity score: {similarity}")
        
        # Get match details
        match_details = nlp.get_match_details(job['id'], resume['id'])
        print(f"Match details: {match_details}")
        
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_similarity()