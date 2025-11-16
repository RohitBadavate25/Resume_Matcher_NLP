import requests
import json

def post_quality_job_description():
    """Post a quality job description for testing"""
    
    job_data = {
        "title": "Senior MERN Stack Developer",
        "company": "TechCorp Solutions",
        "recruiter_name": "HR Team",
        "description": """
        We are seeking a highly skilled Senior MERN Stack Developer to join our dynamic development team.
        The ideal candidate will have extensive experience with MongoDB, Express.js, React.js, and Node.js.
        
        Key Responsibilities:
        • Design and develop full-stack web applications using the MERN stack
        • Build responsive and interactive user interfaces with React.js
        • Develop robust backend APIs using Node.js and Express.js
        • Work with MongoDB databases and implement data modeling
        • Collaborate with cross-functional teams including designers and product managers
        • Implement authentication and authorization systems
        • Optimize applications for maximum speed and scalability
        • Write clean, maintainable, and well-documented code
        • Participate in code reviews and maintain coding standards
        
        Technical Requirements:
        • 3+ years of experience with JavaScript and modern ES6+ features
        • Strong proficiency in React.js including hooks, context, and state management
        • Experience with Node.js and Express.js for backend development
        • Proficiency in MongoDB and database design principles
        • Knowledge of RESTful API design and implementation
        • Experience with version control systems (Git)
        • Familiarity with cloud platforms (AWS, Azure, or GCP)
        • Understanding of authentication methods (JWT, OAuth)
        • Experience with testing frameworks (Jest, Mocha, Cypress)
        • Knowledge of containerization technologies (Docker)
        
        Nice to Have:
        • Experience with TypeScript
        • Knowledge of GraphQL
        • Familiarity with CI/CD pipelines
        • Experience with microservices architecture
        • Understanding of DevOps practices
        • Knowledge of Redis for caching
        • Experience with socket programming for real-time applications
        """,
        "requirements": """
        Education: Bachelor's degree in Computer Science or related field
        Experience: Minimum 3 years in full-stack web development
        Skills: MERN stack, JavaScript, HTML5, CSS3, Git, Agile methodologies
        """
    }
    
    print("📝 Posting quality job description...")
    response = requests.post('http://127.0.0.1:5000/api/job-description', json=job_data)
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Job posted successfully!")
        print(f"Job ID: {result['job_id']}")
        return result['job_id']
    else:
        print(f"❌ Failed to post job: {response.status_code}")
        print(response.text)
        return None

def test_with_quality_job():
    """Test matching with the quality job description"""
    
    job_id = post_quality_job_description()
    if not job_id:
        return
    
    print(f"\n🎯 Testing matching with quality job description...")
    
    # Test matching
    match_response = requests.post('http://127.0.0.1:5000/api/match', 
                                 json={'job_id': job_id})
    
    if match_response.status_code == 200:
        match_data = match_response.json()
        print(f"✅ Matching successful!")
        print(f"📊 Total candidates: {match_data.get('total_candidates', 0)}")
        
        matches = match_data.get('matches', [])
        print(f"\n🏆 Results with Quality Job Description:")
        print("=" * 60)
        
        for i, match in enumerate(matches, 1):
            name = match.get('candidate_name', 'Unknown')
            similarity = match.get('match_percentage', 0)
            strength = match.get('match_category', 'Unknown')
            
            print(f"\n{i}. {name}")
            print(f"   Match: {similarity}% ({strength.upper()})")
            
            # Show component breakdown
            components = match.get('component_scores', {})
            if components:
                print(f"   Components:")
                print(f"     • TF-IDF: {components.get('tfidf_similarity', 0):.3f}")
                print(f"     • Skills: {components.get('skill_similarity', 0):.3f}")
                print(f"     • Semantic: {components.get('semantic_similarity', 0):.3f}")
                print(f"     • Keywords: {components.get('keyword_similarity', 0):.3f}")
            
            # Show skills analysis
            skills = match.get('skills_analysis', {})
            if skills:
                matched_skills = skills.get('matched_skills', [])
                missing_skills = skills.get('missing_skills', [])
                
                if matched_skills:
                    print(f"   ✅ Matched Skills: {', '.join(matched_skills[:5])}")
                if missing_skills:
                    print(f"   ❌ Missing Skills: {', '.join(missing_skills[:3])}")
        
        # Check improvement
        best_match = max([m.get('match_percentage', 0) for m in matches])
        print(f"\n📈 Results Summary:")
        print(f"   Best Match: {best_match}%")
        
        if best_match > 20:
            print("   ✅ SUCCESS: Quality job description produces better matches!")
        else:
            print("   ⚠️  Still low matches - may need better resume content")
            
    else:
        print(f"❌ Matching failed: {match_response.status_code}")
        print(match_response.text)

if __name__ == "__main__":
    test_with_quality_job()