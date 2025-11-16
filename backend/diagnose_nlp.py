#!/usr/bin/env python3
"""
Diagnostic script to identify NLP matching issues
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from nlp_processor import ResumeMatcherNLP
import json

def diagnose_nlp_issues():
    """Diagnose NLP processing issues with sample data"""
    
    print("🔍 Diagnosing NLP Matching Issues")
    print("=" * 50)
    
    # Initialize NLP processor
    try:
        nlp = ResumeMatcherNLP()
        print("✅ NLP processor initialized")
    except Exception as e:
        print(f"❌ Failed to initialize NLP processor: {e}")
        return
    
    # Sample job description
    job_text = """
    Senior Python Developer - Remote
    
    We are looking for an experienced Python developer with 5+ years of experience.
    
    Requirements:
    - Strong proficiency in Python, Django, and Flask
    - Experience with PostgreSQL and MongoDB databases
    - Knowledge of AWS cloud services
    - Familiarity with Docker and Kubernetes
    - Experience with REST APIs and microservices
    - Bachelor's degree in Computer Science
    - Strong problem-solving and communication skills
    
    Nice to have:
    - React.js or Angular experience
    - Machine learning knowledge
    - DevOps experience with Jenkins
    """
    
    # Sample resume
    resume_text = """
    John Doe
    Senior Software Engineer
    
    Professional Experience:
    - 6 years of software development experience
    - Expert in Python programming and web development
    - Proficient with Django framework and Flask
    - Worked with PostgreSQL, MySQL, and MongoDB databases
    - Deployed applications on AWS (EC2, S3, RDS)
    - Experience with Docker containerization
    - Built REST APIs and microservice architectures
    - Used Git for version control
    
    Education:
    Bachelor of Science in Computer Science
    
    Skills:
    Python, Django, Flask, PostgreSQL, MongoDB, AWS, Docker, REST APIs, Git
    JavaScript, React.js, HTML, CSS, Problem solving, Team collaboration
    """
    
    print("\n📝 Processing Documents...")
    
    # Test text preprocessing
    print("\n🔧 Testing Text Preprocessing:")
    job_processed = nlp.preprocess_text(job_text)
    resume_processed = nlp.preprocess_text(resume_text)
    print(f"Original job text length: {len(job_text)}")
    print(f"Processed job text length: {len(job_processed)}")
    print(f"Sample processed job text: {job_processed[:200]}...")
    
    # Test skill extraction
    print("\n🎯 Testing Skill Extraction:")
    job_skills = nlp.extract_skills(job_text)
    resume_skills = nlp.extract_skills(resume_text)
    print(f"Job skills found: {len(job_skills)}")
    print(f"Job skills: {job_skills}")
    print(f"Resume skills found: {len(resume_skills)}")
    print(f"Resume skills: {resume_skills}")
    
    # Check skill overlap
    common_skills = set(job_skills) & set(resume_skills)
    print(f"Common skills: {list(common_skills)}")
    print(f"Skills match ratio: {len(common_skills) / len(job_skills) if job_skills else 0:.2f}")
    
    # Process documents for similarity
    print("\n📊 Processing for Similarity Analysis:")
    nlp.process_job_description("test_job", job_text)
    nlp.process_resume("test_resume", resume_text)
    
    # Test corpus fitting
    if len(nlp.all_texts) >= 2:
        nlp.fit_corpus_vectorizers()
        print("✅ Corpus vectorizers fitted")
    else:
        print("⚠️ Not enough texts to fit corpus vectorizers")
    
    # Calculate similarity
    print("\n🎯 Testing Similarity Calculation:")
    try:
        similarity = nlp.calculate_similarity("test_job", "test_resume")
        print(f"Overall similarity: {similarity:.3f} ({similarity*100:.1f}%)")
        
        # Get detailed match analysis
        match_details = nlp.get_match_details("test_job", "test_resume")
        
        print("\n📋 Component Scores:")
        components = match_details.get('component_scores', {})
        for component, score in components.items():
            print(f"  {component}: {score:.3f}")
        
        print("\n🔍 Skills Analysis:")
        skills_analysis = match_details.get('skills_analysis', {})
        print(f"  Matched skills: {len(skills_analysis.get('matched_skills', []))}")
        print(f"  Missing skills: {len(skills_analysis.get('missing_skills', []))}")
        print(f"  High priority matched: {skills_analysis.get('high_priority_matched', [])}")
        print(f"  High priority missing: {skills_analysis.get('high_priority_missing', [])}")
        
    except Exception as e:
        print(f"❌ Error calculating similarity: {e}")
        import traceback
        traceback.print_exc()
    
    # Test individual similarity components
    print("\n🧪 Testing Individual Components:")
    try:
        tfidf_sim = nlp.calculate_semantic_similarity("test_job", "test_resume")
        skill_sim = nlp.calculate_skill_similarity("test_job", "test_resume")
        keyword_sim = nlp.calculate_keyword_similarity("test_job", "test_resume")
        context_sim = nlp.calculate_context_similarity("test_job", "test_resume")
        
        print(f"  TF-IDF Similarity: {tfidf_sim:.3f}")
        print(f"  Skill Similarity: {skill_sim:.3f}")
        print(f"  Keyword Similarity: {keyword_sim:.3f}")
        print(f"  Context Similarity: {context_sim:.3f}")
        
    except Exception as e:
        print(f"❌ Error in component testing: {e}")
        import traceback
        traceback.print_exc()
    
    # Identify potential issues
    print("\n🚨 Potential Issues Identified:")
    issues = []
    
    if len(job_skills) < 5:
        issues.append("⚠️ Low skill extraction from job description")
    if len(resume_skills) < 5:
        issues.append("⚠️ Low skill extraction from resume")
    if len(common_skills) == 0:
        issues.append("❌ No common skills found between job and resume")
    if similarity < 0.3:
        issues.append("❌ Very low similarity score despite obvious matches")
    
    if not issues:
        print("✅ No major issues detected")
    else:
        for issue in issues:
            print(issue)
    
    print("\n💡 Recommendations:")
    print("1. Check if skill patterns are too restrictive")
    print("2. Verify text preprocessing isn't removing important terms")
    print("3. Test with different TF-IDF parameters")
    print("4. Check if spaCy model is working correctly")

if __name__ == "__main__":
    diagnose_nlp_issues()