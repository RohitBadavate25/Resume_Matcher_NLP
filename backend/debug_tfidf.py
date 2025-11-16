#!/usr/bin/env python3
"""
Enhanced diagnostic script to debug TF-IDF and semantic similarity issues
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from nlp_processor import ResumeMatcherNLP
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def debug_tfidf_issues():
    """Debug TF-IDF vectorization issues"""
    
    print("🔍 Debugging TF-IDF Issues")
    print("=" * 50)
    
    # Sample texts
    job_text = "Senior Python Developer with Django Flask PostgreSQL AWS Docker Kubernetes experience"
    resume_text = "Experienced Python developer skilled in Django Flask PostgreSQL AWS Docker REST APIs"
    
    nlp = ResumeMatcherNLP()
    
    # Test different vectorizer configurations
    configs = [
        {
            'name': 'Original Config',
            'params': {
                'max_features': 8000,
                'stop_words': None,
                'ngram_range': (1, 2),
                'min_df': 1,
                'max_df': 0.8,
            }
        },
        {
            'name': 'Simple Config',
            'params': {
                'max_features': 1000,
                'stop_words': 'english',
                'ngram_range': (1, 1),
                'min_df': 1,
                'max_df': 1.0,
            }
        },
        {
            'name': 'Minimal Config',
            'params': {
                'max_features': None,
                'stop_words': None,
                'ngram_range': (1, 1),
                'min_df': 1,
                'max_df': 1.0,
            }
        }
    ]
    
    for config in configs:
        print(f"\n📊 Testing {config['name']}:")
        
        try:
            vectorizer = TfidfVectorizer(**config['params'])
            
            # Test on preprocessed texts
            job_processed = nlp.preprocess_text(job_text)
            resume_processed = nlp.preprocess_text(resume_text)
            
            print(f"  Job processed: {job_processed}")
            print(f"  Resume processed: {resume_processed}")
            
            texts = [job_processed, resume_processed]
            tfidf_matrix = vectorizer.fit_transform(texts)
            
            print(f"  Matrix shape: {tfidf_matrix.shape}")
            print(f"  Vocabulary size: {len(vectorizer.vocabulary_)}")
            print(f"  Sample vocab: {list(vectorizer.vocabulary_.keys())[:10]}")
            
            if tfidf_matrix.shape[1] > 0:
                from sklearn.metrics.pairwise import cosine_similarity
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                print(f"  Similarity: {similarity:.3f}")
            else:
                print(f"  ❌ No features extracted!")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Test with raw texts
    print(f"\n📝 Testing with Raw Texts:")
    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        texts = [job_text, resume_text]
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        print(f"  Raw texts matrix shape: {tfidf_matrix.shape}")
        if tfidf_matrix.shape[1] > 0:
            from sklearn.metrics.pairwise import cosine_similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            print(f"  Raw texts similarity: {similarity:.3f}")
            
    except Exception as e:
        print(f"  ❌ Raw texts error: {e}")

if __name__ == "__main__":
    debug_tfidf_issues()