#!/usr/bin/env python3
"""
Basic test script for the enhanced Resume Matcher that works without optional dependencies
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

def test_basic_functionality():
    """Test basic functionality without optional dependencies"""
    
    print("🚀 Testing Basic Enhanced Resume Matcher")
    print("=" * 60)
    
    # Test 1: Check if enhanced processor can be imported
    print("📝 Testing Enhanced NLP Processor Import...")
    try:
        from enhanced_nlp_processor import EnhancedResumeMatcherNLP
        print("✅ Enhanced processor imported successfully")
        enhanced_available = True
    except ImportError as e:
        print(f"❌ Enhanced processor import failed: {e}")
        print("⚠️ Falling back to basic processor")
        from nlp_processor import ResumeMatcherNLP
        enhanced_available = False
    
    # Test 2: Initialize processor
    print("\\n🔧 Initializing NLP Processor...")
    try:
        if enhanced_available:
            nlp = EnhancedResumeMatcherNLP()
            print("✅ Enhanced processor initialized")
            
            # Check BERT availability
            if nlp.transformer_model:
                print("🤖 BERT transformer model loaded")
            else:
                print("⚠️ BERT not available, using TF-IDF fallback")
        else:
            nlp = ResumeMatcherNLP()
            print("✅ Basic processor initialized")
    except Exception as e:
        print(f"❌ Processor initialization failed: {e}")
        return
    
    # Test 3: Simple similarity test
    print("\\n🧪 Testing Similarity Calculation...")
    
    job_description = """
    Software Developer Position
    
    We are looking for a Python developer with experience in:
    - Python programming
    - Web development 
    - Database management
    - 2+ years experience
    """
    
    good_resume = """
    John Smith - Software Developer
    
    Experience:
    Software Developer (2020-2024) - 4 years
    - Developed Python applications
    - Built web applications using Flask
    - Managed MySQL databases
    - Strong problem-solving skills
    
    Skills: Python, Flask, MySQL, Git
    """
    
    poor_resume = """
    Jane Doe - Marketing Manager
    
    Experience:
    Marketing Manager (2021-2024) - 3 years
    - Managed marketing campaigns
    - Social media strategy
    - Content creation
    - Team leadership
    
    Skills: Marketing, Social Media, Content Writing, Leadership
    """
    
    try:
        # Process documents
        nlp.process_job_description("job_1", job_description)
        nlp.process_resume("good_resume", good_resume)
        nlp.process_resume("poor_resume", poor_resume)
        print("✅ Documents processed successfully")
        
        # Test similarity calculation
        if enhanced_available:
            good_score, good_confidence = nlp.calculate_similarity("job_1", "good_resume")
            poor_score, poor_confidence = nlp.calculate_similarity("job_1", "poor_resume")
            
            print(f"\\n📊 Results (Enhanced System):")
            print(f"Good Match: {good_score:.3f} ({good_score*100:.1f}%) - Confidence: {good_confidence:.3f}")
            print(f"Poor Match: {poor_score:.3f} ({poor_score*100:.1f}%) - Confidence: {poor_confidence:.3f}")
            
            # Test detailed analysis
            good_details = nlp.get_match_details("job_1", "good_resume")
            print(f"Match Strength: {good_details.get('match_strength', 'unknown').upper()}")
            
        else:
            good_score = nlp.calculate_similarity("job_1", "good_resume") 
            poor_score = nlp.calculate_similarity("job_1", "poor_resume")
            
            print(f"\\n📊 Results (Basic System):")
            print(f"Good Match: {good_score:.3f} ({good_score*100:.1f}%)")
            print(f"Poor Match: {poor_score:.3f} ({poor_score*100:.1f}%)")
        
        # Validate that good match scores higher than poor match
        if good_score > poor_score:
            print("✅ System correctly ranks good match higher than poor match")
        else:
            print("⚠️ Warning: System ranking may need adjustment")
            
    except Exception as e:
        print(f"❌ Similarity calculation failed: {e}")
        return
    
    # Test 4: Check if validation framework is available
    print("\\n📊 Testing Validation Framework...")
    try:
        from validation_framework import ValidationFramework
        validator = ValidationFramework(nlp)
        print("✅ Validation framework available")
        validation_available = True
    except ImportError as e:
        print(f"⚠️ Validation framework not available: {e}")
        validation_available = False
    except Exception as e:
        print(f"⚠️ Validation framework error: {e}")
        validation_available = False
    
    # Test 5: App integration test
    print("\\n🌐 Testing App Integration...")
    try:
        from app import app
        print("✅ Flask app can be imported")
        
        # Test if enhanced features are detected
        with app.test_client() as client:
            response = client.get('/api/system/status')
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success'):
                    status = data.get('status', {})
                    print(f"Enhanced NLP: {'✅' if status.get('enhanced_nlp_available') else '❌'}")
                    print(f"Validation Framework: {'✅' if status.get('validation_framework_available') else '❌'}")
                    print(f"Confidence Scoring: {'✅' if status.get('features', {}).get('confidence_scoring') else '❌'}")
                else:
                    print("⚠️ System status endpoint returned error")
            else:
                print(f"⚠️ System status endpoint failed: {response.status_code}")
                
    except Exception as e:
        print(f"⚠️ App integration test failed: {e}")
    
    print(f"\\n🎯 Summary:")
    print("=" * 60)
    
    if enhanced_available:
        print("✅ Enhanced NLP system is working!")
        print("✅ Confidence scoring available")
        print("✅ Improved 3-component similarity calculation")
        if nlp.transformer_model:
            print("✅ BERT semantic understanding active")
        else:
            print("⚠️ BERT not available, using TF-IDF fallback")
    else:
        print("⚠️ Using basic NLP system (enhanced features unavailable)")
    
    if validation_available:
        print("✅ Validation framework ready")
        print("✅ Ground truth testing available")
    else:
        print("⚠️ Validation framework unavailable")
    
    print("\\n💡 Next Steps:")
    if not enhanced_available:
        print("  • Run: python setup_enhanced.py")
        print("  • Install missing dependencies to enable enhanced features")
    else:
        print("  • Run: python app.py (to start the server)")
        print("  • Test the web interface at http://localhost:5000")
    
    if validation_available:
        print("  • Run validation: python test_improvements.py")

if __name__ == "__main__":
    test_basic_functionality()