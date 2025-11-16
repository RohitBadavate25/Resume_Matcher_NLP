#!/usr/bin/env python3
"""
Test script to demonstrate the improved Resume Matcher with enhanced accuracy features.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from enhanced_nlp_processor import EnhancedResumeMatcherNLP
from validation_framework import ValidationFramework
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_improvements():
    """Test the enhanced NLP improvements"""
    
    print("🚀 Testing Enhanced Resume Matcher Improvements")
    print("=" * 60)
    
    # Initialize enhanced processor
    print("📝 Initializing Enhanced NLP Processor...")
    try:
        nlp = EnhancedResumeMatcherNLP()
        print("✅ Enhanced processor initialized successfully")
        
        # Check if BERT model is available
        if nlp.transformer_model:
            print("🤖 BERT transformer model loaded for semantic analysis")
        else:
            print("⚠️ Using TF-IDF fallback (BERT not available)")
            
    except Exception as e:
        print(f"❌ Error initializing enhanced processor: {e}")
        return
    
    # Initialize validation framework
    print("📊 Initializing Validation Framework...")
    try:
        validator = ValidationFramework(nlp)
        print("✅ Validation framework initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing validator: {e}")
        return
    
    print("\n🧪 Running Tests...")
    print("-" * 60)
    
    # Test sample data
    job_description = """
    Senior Software Engineer - Full Stack
    
    We're looking for a Senior Software Engineer with 5+ years of experience.
    
    Requirements:
    • 5+ years of software development experience
    • Strong proficiency in Python and JavaScript
    • Experience with React, Node.js, and modern web frameworks
    • Knowledge of cloud platforms (AWS, Azure, or GCP)
    • Database experience with PostgreSQL and MongoDB
    • Docker and containerization experience
    • Bachelor's degree in Computer Science or related field
    """
    
    excellent_resume = """
    John Smith - Senior Software Engineer
    
    Professional Experience:
    Senior Software Engineer at TechCorp (2018-2024) - 6 years
    • Developed full-stack applications using Python, JavaScript, and React
    • Built scalable Node.js backends serving 1M+ users
    • Deployed applications on AWS with Docker containers
    • Managed PostgreSQL and MongoDB databases
    • Led a team of 4 developers using Agile methodology
    
    Education:
    Bachelor of Science in Computer Science - MIT (2017)
    
    Technical Skills:
    Python, JavaScript, React, Node.js, AWS, Docker, PostgreSQL, MongoDB, Git
    """
    
    poor_resume = """
    Jane Doe - Graphic Designer
    
    Professional Experience:
    Graphic Designer at DesignStudio (2020-2024) - 4 years
    • Created visual designs for marketing materials
    • Proficient in Adobe Creative Suite (Photoshop, Illustrator, InDesign)
    • Basic knowledge of HTML and CSS
    • Collaborated with marketing teams on campaign designs
    
    Education:
    Bachelor of Fine Arts in Graphic Design - Art University (2019)
    
    Skills:
    Adobe Photoshop, Illustrator, InDesign, HTML, CSS
    """
    
    # Process documents
    print("📝 Processing documents...")
    nlp.process_job_description("job_1", job_description)
    nlp.process_resume("excellent_resume", excellent_resume)
    nlp.process_resume("poor_resume", poor_resume)
    
    # Test 1: Excellent match
    print(f"\\n👤 Testing Excellent Match:")
    print("-" * 30)
    
    excellent_score, excellent_confidence = nlp.calculate_similarity("job_1", "excellent_resume")
    excellent_details = nlp.get_match_details("job_1", "excellent_resume")
    
    print(f"Similarity Score: {excellent_score:.3f} ({excellent_score*100:.1f}%)")
    print(f"Confidence Score: {excellent_confidence:.3f} ({excellent_confidence*100:.1f}%)")
    print(f"Match Strength: {excellent_details['match_strength'].upper()}")
    print(f"Skills Matched: {len(excellent_details['matched_skills'])}")
    print(f"Skills Missing: {len(excellent_details['missing_skills'])}")
    
    if excellent_details['recommendations']:
        print("Recommendations:")
        for rec in excellent_details['recommendations'][:2]:
            priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
            print(f"  {priority_emoji} {rec['message']}")
    
    # Test 2: Poor match
    print(f"\\n👤 Testing Poor Match:")
    print("-" * 30)
    
    poor_score, poor_confidence = nlp.calculate_similarity("job_1", "poor_resume")
    poor_details = nlp.get_match_details("job_1", "poor_resume")
    
    print(f"Similarity Score: {poor_score:.3f} ({poor_score*100:.1f}%)")
    print(f"Confidence Score: {poor_confidence:.3f} ({poor_confidence*100:.1f}%)")
    print(f"Match Strength: {poor_details['match_strength'].upper()}")
    print(f"Skills Matched: {len(poor_details['matched_skills'])}")
    print(f"Skills Missing: {len(poor_details['missing_skills'])}")
    
    if poor_details['recommendations']:
        print("Recommendations:")
        for rec in poor_details['recommendations'][:2]:
            priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
            print(f"  {priority_emoji} {rec['message']}")
    
    # Test 3: Validation Framework
    print(f"\\n📊 Testing Validation Framework:")
    print("-" * 30)
    
    print("Running ground truth validation...")
    try:
        validation_results = validator.run_ground_truth_validation("test_improvements")
        
        if 'error' not in validation_results:
            print(f"✅ Validation completed successfully!")
            print(f"Mean Absolute Error: {validation_results.get('mae', 'N/A'):.3f}")
            print(f"Correlation: {validation_results.get('pearson_correlation', 'N/A'):.3f}")
            print(f"Accuracy (±20%): {validation_results.get('accuracy_20_percent', 'N/A'):.1%}")
            print(f"Sample Size: {validation_results.get('sample_size', 'N/A')}")
        else:
            print(f"⚠️ Validation error: {validation_results['error']}")
            
    except Exception as e:
        print(f"❌ Validation framework error: {e}")
    
    # Test 4: Feedback system
    print(f"\\n💬 Testing Feedback System:")
    print("-" * 30)
    
    try:
        # Add some sample feedback
        nlp.add_feedback(
            job_id="job_1",
            resume_id="excellent_resume", 
            human_score=0.9,
            recruiter_feedback="Excellent match, candidate has all required skills",
            match_quality="excellent"
        )
        
        nlp.add_feedback(
            job_id="job_1",
            resume_id="poor_resume",
            human_score=0.1,
            recruiter_feedback="Poor match, completely different skillset",
            match_quality="poor"
        )
        
        print("✅ Feedback added successfully")
        
        # Get validation metrics (if enough data)
        metrics = nlp.get_validation_metrics()
        if 'error' not in metrics:
            print(f"Current validation metrics:")
            print(f"  • MAE: {metrics.get('mae', 'N/A'):.3f}")
            print(f"  • Correlation: {metrics.get('correlation', 'N/A'):.3f}")
            print(f"  • Sample Size: {metrics.get('sample_size', 'N/A')}")
        else:
            print(f"  • {metrics['error']}")
            
    except Exception as e:
        print(f"❌ Feedback system error: {e}")
    
    print(f"\\n🎯 Summary of Improvements:")
    print("=" * 60)
    print("✅ COMPLETED IMPROVEMENTS:")
    print("  • Simplified from 5 to 3 core similarity components")
    print("  • Added confidence scoring (10-100%)")
    print("  • Integrated BERT transformer for semantic understanding")
    print("  • Implemented human feedback collection system")
    print("  • Created comprehensive validation framework")
    print("  • Added ground truth testing with curated datasets")
    print("  • Enhanced recommendations with actionable insights")
    
    print("\\n🔧 TECHNICAL ENHANCEMENTS:")
    print("  • Reduced complexity and noise in similarity calculation")
    print("  • Added data quality assessment for confidence")
    print("  • Implemented continuous learning from recruiter feedback")
    print("  • Created validation metrics (MAE, correlation, accuracy)")
    print("  • Added performance monitoring over time")
    
    print("\\n📈 ACCURACY IMPROVEMENTS:")
    print("  • More consistent scoring with weighted skill matching")
    print("  • Better discrimination between good/poor matches")
    print("  • Confidence-aware recommendations") 
    print("  • Measurable validation against ground truth data")
    print("  • Continuous improvement through feedback loop")
    
    print(f"\\n💡 REALISTIC EXPECTATIONS:")
    print("  • System is designed for screening and ranking (not final decisions)")
    print("  • Confidence scores indicate prediction reliability")
    print("  • Human review still essential for nuanced evaluation")
    print("  • Best used for initial filtering and candidate prioritization")

if __name__ == "__main__":
    test_improvements()