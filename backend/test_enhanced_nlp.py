#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced NLP matching capabilities
"""

from nlp_processor import ResumeMatcherNLP
import json

def test_enhanced_matching():
    """Test the enhanced NLP matching with sample data"""
    
    # Initialize the enhanced NLP processor
    nlp = ResumeMatcherNLP()
    
    # Sample job description
    job_description = """
    Senior Software Engineer - Full Stack Development
    
    We are looking for an experienced Full Stack Developer with 5+ years of experience 
    to join our dynamic team. The ideal candidate should have strong expertise in:
    
    Requirements:
    - Bachelor's degree in Computer Science or related field
    - 5+ years of software development experience
    - Proficiency in Python, JavaScript, and React
    - Experience with AWS, Docker, and Kubernetes
    - Strong knowledge of SQL and NoSQL databases (PostgreSQL, MongoDB)
    - Experience with CI/CD pipelines and DevOps practices
    - Machine learning experience preferred
    - Excellent problem-solving and communication skills
    - Agile/Scrum methodology experience
    
    Responsibilities:
    - Design and develop scalable web applications
    - Collaborate with cross-functional teams
    - Implement automated testing and deployment
    - Mentor junior developers
    """
    
    # Sample resume 1 - Strong match
    resume_1 = """
    John Smith
    Senior Full Stack Developer
    Email: john.smith@email.com
    
    Professional Experience:
    Senior Software Developer (2019-2024) - 5 years
    - Developed full-stack web applications using Python, JavaScript, and React
    - Implemented microservices architecture using Docker and Kubernetes
    - Managed AWS infrastructure and deployed applications using CI/CD pipelines
    - Worked extensively with PostgreSQL and MongoDB databases
    - Applied machine learning algorithms for data analysis and prediction
    - Led agile development teams and mentored junior developers
    - Strong problem-solving skills and excellent communication abilities
    
    Education:
    Bachelor of Science in Computer Science, University of Technology
    
    Technical Skills:
    - Programming: Python, JavaScript, TypeScript, Java
    - Frontend: React, Angular, HTML5, CSS3
    - Backend: Django, Flask, Node.js, Express
    - Databases: PostgreSQL, MongoDB, Redis
    - Cloud: AWS (EC2, S3, Lambda, RDS)
    - DevOps: Docker, Kubernetes, Jenkins, Git
    - Machine Learning: TensorFlow, scikit-learn, pandas
    """
    
    # Sample resume 2 - Moderate match
    resume_2 = """
    Jane Doe
    Software Developer
    Email: jane.doe@email.com
    
    Professional Experience:
    Software Developer (2021-2024) - 3 years
    - Developed web applications using JavaScript and React
    - Basic experience with Python for data analysis
    - Worked with MySQL databases
    - Some experience with Git version control
    - Participated in agile development processes
    
    Education:
    Bachelor of Science in Information Technology
    
    Technical Skills:
    - Programming: JavaScript, HTML, CSS, some Python
    - Frontend: React, jQuery
    - Databases: MySQL
    - Tools: Git, Visual Studio Code
    """
    
    # Sample resume 3 - Poor match
    resume_3 = """
    Mike Johnson
    Graphic Designer
    Email: mike.johnson@email.com
    
    Professional Experience:
    Graphic Designer (2020-2024) - 4 years
    - Created visual designs for marketing materials
    - Proficient in Adobe Creative Suite
    - Basic HTML and CSS knowledge
    - Worked with clients to understand design requirements
    
    Education:
    Bachelor of Fine Arts in Graphic Design
    
    Technical Skills:
    - Design: Photoshop, Illustrator, InDesign
    - Web: Basic HTML, CSS
    - Other: Microsoft Office Suite
    """
    
    print("🚀 Testing Enhanced NLP Resume Matcher")
    print("=" * 60)
    
    # Process documents
    print("📝 Processing documents...")
    nlp.process_job_description("job_1", job_description)
    nlp.process_resume("resume_1", resume_1)
    nlp.process_resume("resume_2", resume_2)
    nlp.process_resume("resume_3", resume_3)
    
    # Fit corpus vectorizers for better accuracy
    nlp.fit_corpus_vectorizers()
    print("✅ Corpus vectorizers fitted successfully")
    
    print("\n📊 Match Results:")
    print("-" * 60)
    
    # Test each resume against the job
    resumes = [
        ("resume_1", "John Smith - Senior Full Stack Developer"),
        ("resume_2", "Jane Doe - Software Developer"),
        ("resume_3", "Mike Johnson - Graphic Designer")
    ]
    
    for resume_id, resume_name in resumes:
        print(f"\n👤 Candidate: {resume_name}")
        
        # Calculate similarity
        similarity = nlp.calculate_similarity("job_1", resume_id)
        match_details = nlp.get_match_details("job_1", resume_id)
        
        print(f"Overall Similarity: {similarity:.3f} ({similarity*100:.1f}%)")
        print(f"Match Strength: {match_details.get('match_strength', 'unknown').upper()}")
        
        # Component scores
        components = match_details.get('component_scores', {})
        print(f"Component Scores:")
        for component, score in components.items():
            print(f"  • {component.replace('_', ' ').title()}: {score:.3f}")
        
        # Skills analysis
        skills = match_details.get('skills_analysis', {})
        matched_skills = skills.get('matched_skills', [])
        missing_skills = skills.get('missing_skills', [])
        high_priority_matched = skills.get('high_priority_matched', [])
        high_priority_missing = skills.get('high_priority_missing', [])
        
        print(f"Skills Analysis:")
        print(f"  • Total Skills Matched: {len(matched_skills)}")
        print(f"  • High Priority Matched: {len(high_priority_matched)}")
        if high_priority_matched:
            print(f"    - {', '.join(high_priority_matched[:5])}")
        print(f"  • High Priority Missing: {len(high_priority_missing)}")
        if high_priority_missing:
            print(f"    - {', '.join(high_priority_missing[:5])}")
        
        # Experience analysis
        exp_analysis = match_details.get('experience_analysis', {})
        if exp_analysis.get('status') != 'unknown':
            print(f"Experience Match: {exp_analysis.get('status', 'unknown').replace('_', ' ').title()}")
            if exp_analysis.get('job_years') and exp_analysis.get('resume_years'):
                print(f"  • Required: {exp_analysis['job_years']} years")
                print(f"  • Candidate: {exp_analysis['resume_years']} years")
        
        # Recommendations
        recommendations = match_details.get('recommendations', [])
        if recommendations:
            print(f"Recommendations:")
            for rec in recommendations[:3]:  # Show top 3 recommendations
                priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                print(f"  {priority_emoji} {rec['message']}")
        
        print("-" * 60)
    
    print("\n🎯 Summary:")
    print("The enhanced NLP system provides:")
    print("• More accurate similarity scoring using corpus-fitted TF-IDF")
    print("• Comprehensive skill extraction and weighted matching") 
    print("• Experience level analysis and requirements matching")
    print("• Document structure and context analysis")
    print("• Detailed recommendations for improving matches")
    print("• Multi-component scoring for better discrimination")

if __name__ == "__main__":
    test_enhanced_matching()