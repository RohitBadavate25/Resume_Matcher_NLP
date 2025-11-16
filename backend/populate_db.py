#!/usr/bin/env python3

from database import Database
import uuid

def populate_sample_data():
    """Add sample job descriptions and resumes to the database"""
    db = Database()
    
    print("🔄 Adding sample data to database...")
    
    # Sample job descriptions
    job_descriptions = [
        {
            "title": "Senior Software Engineer",
            "company": "TechCorp Inc.",
            "description": "We are looking for a Senior Software Engineer with expertise in Python, Django, and React. The candidate should have experience with cloud platforms, microservices architecture, and agile development methodologies. Strong problem-solving skills and ability to work in a collaborative team environment are essential.",
            "requirements": "5+ years of experience in software development, Python, Django, React, AWS, Docker, Git",
            "recruiter_name": "John Smith"
        },
        {
            "title": "Data Scientist",
            "company": "DataTech Solutions",
            "description": "Join our data science team to work on machine learning projects and data analytics. We need someone skilled in Python, pandas, scikit-learn, and statistical analysis. Experience with big data technologies and cloud platforms is a plus.",
            "requirements": "PhD or Master's in Data Science, Python, Machine Learning, SQL, Statistics, TensorFlow or PyTorch",
            "recruiter_name": "Sarah Johnson"
        },
        {
            "title": "Frontend Developer",
            "company": "WebDesign Pro",
            "description": "We're seeking a talented Frontend Developer to create amazing user interfaces. You should be proficient in JavaScript, React, HTML5, CSS3, and have an eye for design. Experience with modern build tools and responsive design is required.",
            "requirements": "3+ years frontend experience, React, JavaScript, HTML5, CSS3, Webpack, Git",
            "recruiter_name": "Mike Davis"
        },
        {
            "title": "DevOps Engineer",
            "company": "CloudOps Ltd",
            "description": "Looking for a DevOps Engineer to manage our cloud infrastructure and CI/CD pipelines. Must have experience with AWS, Docker, Kubernetes, and automation tools. Strong scripting skills in Python or Bash are required.",
            "requirements": "AWS, Docker, Kubernetes, CI/CD, Python, Terraform, Jenkins",
            "recruiter_name": "Emily Wilson"
        },
        {
            "title": "Product Manager",
            "company": "InnovateCorp",
            "description": "Seeking an experienced Product Manager to lead product strategy and development. Should have strong analytical skills, experience with agile methodologies, and ability to work cross-functionally with engineering and design teams.",
            "requirements": "5+ years product management, Agile, Analytics, User Research, Roadmap Planning",
            "recruiter_name": "David Brown"
        }
    ]
    
    # Sample resumes
    resumes = [
        {
            "filename": "john_doe_resume.pdf",
            "candidate_name": "John Doe",
            "candidate_email": "john.doe@email.com",
            "content": "Experienced Software Engineer with 6 years in full-stack development. Proficient in Python, Django, React, and JavaScript. Strong experience with AWS cloud services, Docker containerization, and microservices architecture. Led development teams in agile environments and delivered scalable web applications. Skills: Python, Django, React, JavaScript, AWS, Docker, Git, PostgreSQL, Redis, Elasticsearch."
        },
        {
            "filename": "jane_smith_resume.pdf",
            "candidate_name": "Jane Smith",
            "candidate_email": "jane.smith@email.com",
            "content": "Data Scientist with PhD in Statistics and 4 years of industry experience. Expert in machine learning, statistical modeling, and data visualization. Proficient in Python, pandas, scikit-learn, TensorFlow, and SQL. Experience with big data processing using Spark and cloud platforms like AWS. Published researcher with strong analytical and communication skills. Skills: Python, Machine Learning, Statistics, TensorFlow, SQL, Spark, AWS, Data Visualization."
        },
        {
            "filename": "alex_johnson_resume.pdf",
            "candidate_name": "Alex Johnson",
            "candidate_email": "alex.johnson@email.com",
            "content": "Frontend Developer with 4 years of experience creating responsive web applications. Expert in React, JavaScript, HTML5, CSS3, and modern frontend build tools. Strong design sense and experience with user interface development. Familiar with backend technologies and API integration. Skills: React, JavaScript, HTML5, CSS3, Webpack, Sass, Git, RESTful APIs, Responsive Design."
        },
        {
            "filename": "maria_garcia_resume.pdf",
            "candidate_name": "Maria Garcia",
            "candidate_email": "maria.garcia@email.com",
            "content": "DevOps Engineer with 5 years experience in cloud infrastructure and automation. Specialized in AWS services, container orchestration with Kubernetes, and CI/CD pipeline development. Strong scripting skills in Python and Bash. Experience with infrastructure as code using Terraform and monitoring solutions. Skills: AWS, Kubernetes, Docker, CI/CD, Python, Terraform, Jenkins, Monitoring, Linux."
        },
        {
            "filename": "robert_chen_resume.pdf",
            "candidate_name": "Robert Chen",
            "candidate_email": "robert.chen@email.com",
            "content": "Product Manager with 7 years experience leading cross-functional teams and driving product strategy. Expert in agile methodologies, user research, and data-driven decision making. Strong background in technology with previous software engineering experience. Led successful product launches and managed product roadmaps. Skills: Product Strategy, Agile, User Research, Analytics, Roadmap Planning, Team Leadership, Technical Background."
        }
    ]
    
    # Add job descriptions
    for job_data in job_descriptions:
        job_id = db.create_job_description(
            title=job_data["title"],
            company=job_data["company"],
            description=job_data["description"],
            requirements=job_data["requirements"],
            recruiter_name=job_data["recruiter_name"]
        )
        print(f"✅ Added job: {job_data['title']} at {job_data['company']}")
    
    # Add resumes
    for resume_data in resumes:
        resume_id = db.create_resume(
            filename=resume_data["filename"],
            candidate_name=resume_data["candidate_name"],
            candidate_email=resume_data["candidate_email"],
            content=resume_data["content"],
            file_path=f"uploads/{resume_data['filename']}"
        )
        print(f"✅ Added resume: {resume_data['candidate_name']} ({resume_data['filename']})")
    
    print("\n🎉 Sample data added successfully!")
    print(f"📝 Added {len(job_descriptions)} job descriptions")
    print(f"📄 Added {len(resumes)} resumes")
    print("\n💡 You can now test the application - the 'failed to fetch resumes' error should be resolved!")

if __name__ == "__main__":
    populate_sample_data()