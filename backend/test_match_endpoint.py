#!/usr/bin/env python3

import sys
import traceback
from nlp_processor import ResumeMatcherNLP
from database import Database

def test_matching():
    """Test the matching functionality that's causing the API to fail"""
    try:
        # Initialize components
        print("Initializing database...")
        db = Database()
        
        print("Initializing NLP processor...")
        nlp_processor = ResumeMatcherNLP()
        
        # Test job and resume IDs from inspection
        job_id = "b18d0ac8-0c5f-4539-8d5a-4a0fda000c03"
        resume_id = "555a1e6b-cd71-4001-802c-2f94d6d632ff"
        
        print(f"Testing match between job {job_id} and resume {resume_id}")
        
        # Test job description retrieval
        print("Getting job description...")
        job_desc = db.get_job_description(job_id)
        if not job_desc:
            print("ERROR: Job description not found!")
            return False
        print(f"✓ Job found: {job_desc.get('title', 'No title')}")
        
        # Test resume retrieval
        print("Getting resume...")
        resume_data = db.get_resume(resume_id)
        if not resume_data:
            print("ERROR: Resume not found!")
            return False
        print(f"✓ Resume found: {resume_data.get('candidate_name', 'No name')}")
        
        # Process job description if needed
        print("Processing job description...")
        if job_id not in nlp_processor.job_data:
            nlp_processor.add_job_description(job_id, job_desc)
        
        # Process resume if needed  
        print("Processing resume...")
        if resume_id not in nlp_processor.resume_data:
            nlp_processor.add_resume(resume_id, resume_data)
        
        # Fit vectorizers if needed
        if not nlp_processor.corpus_fitted:
            print("Fitting vectorizers...")
            nlp_processor.fit_corpus_vectorizers()
        
        # Test similarity calculation
        print("Calculating similarity...")
        similarity_score = nlp_processor.calculate_similarity(job_id, resume_id)
        print(f"✓ Similarity score: {similarity_score}")
        
        # Test match details
        print("Getting match details...")
        match_details = nlp_processor.get_match_details(job_id, resume_id)
        print(f"✓ Match details keys: {list(match_details.keys())}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Resume Matching API Components")
    print("=" * 50)
    success = test_matching()
    print("=" * 50)
    print(f"Test {'PASSED' if success else 'FAILED'}")