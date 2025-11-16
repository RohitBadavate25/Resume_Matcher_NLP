from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename
import PyPDF2
import docx
# Import both processors - enhanced one is primary, original as fallback
try:
    from enhanced_nlp_processor import EnhancedResumeMatcherNLP
    from validation_framework import ValidationFramework
    ENHANCED_NLP_AVAILABLE = True
except ImportError:
    from nlp_processor import ResumeMatcherNLP
    ENHANCED_NLP_AVAILABLE = False
    
from database import Database
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize NLP processor and database - use enhanced version if available
if ENHANCED_NLP_AVAILABLE:
    logger.info("Using Enhanced NLP Processor with improved accuracy")
    nlp_processor = EnhancedResumeMatcherNLP()
    validation_framework = ValidationFramework(nlp_processor)
else:
    logger.info("Using Standard NLP Processor")
    nlp_processor = ResumeMatcherNLP()
    validation_framework = None

db = Database()

def initialize_nlp_with_existing_data():
    """Load existing job descriptions and resumes into NLP processor"""
    try:
        logger.info("Initializing NLP processor with existing data...")
        
        # Load all existing job descriptions
        jobs = db.get_job_descriptions()
        for job in jobs:
            job_id = job['id']
            description = job['description']
            nlp_processor.process_job_description(job_id, description)
            logger.info(f"Loaded job description: {job_id}")
        
        # Load all existing resumes
        resumes = db.get_resumes()
        for resume in resumes:
            resume_id = resume['id']
            content = resume['content']
            nlp_processor.process_resume(resume_id, content)
            logger.info(f"Loaded resume: {resume_id}")
        
        # Fit corpus vectorizers if we have enough documents
        if len(nlp_processor.all_texts) >= 2:
            nlp_processor.fit_corpus_vectorizers()
            logger.info(f"Fitted corpus vectorizers with {len(nlp_processor.all_texts)} documents")
        
        logger.info("NLP processor initialization completed")
        
    except Exception as e:
        logger.error(f"Error initializing NLP processor: {str(e)}")

# Initialize with existing data on startup
initialize_nlp_with_existing_data()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file_path):
    """Extract text content from uploaded files"""
    try:
        file_extension = file_path.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        
        elif file_extension == 'docx':
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        
        elif file_extension == 'txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        
        else:
            return ""
    
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {str(e)}")
        return ""

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/job-description', methods=['POST'])
def create_job_description():
    """Create a new job description"""
    try:
        data = request.get_json()
        
        if not data or 'description' not in data:
            return jsonify({'error': 'Job description is required'}), 400
        
        # Create job description in database
        job_id = db.create_job_description(
            title=data.get('title', 'Untitled Position'),
            company=data.get('company', ''),
            description=data['description'],
            requirements=data.get('requirements', ''),
            recruiter_name=data.get('recruiter_name', 'Anonymous Recruiter')
        )
        
        # Process the job description with NLP
        nlp_processor.process_job_description(job_id, data['description'])
        
        # Refit corpus vectorizers if we have enough documents
        if len(nlp_processor.all_texts) >= 2:
            nlp_processor.fit_corpus_vectorizers()
            logger.info("Refitted corpus vectorizers after adding job description")
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': 'Job description created successfully'
        }), 201
    
    except Exception as e:
        logger.error(f"Error creating job description: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/job-descriptions', methods=['GET'])
def get_job_descriptions():
    """Get all job descriptions"""
    try:
        job_descriptions = db.get_job_descriptions()
        return jsonify({
            'job_descriptions': job_descriptions
        })
    except Exception as e:
        logger.error(f"Error fetching job descriptions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/resume', methods=['POST'])
def upload_resume():
    """Upload and process a resume"""
    try:
        # Check if file is present
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF, DOC, DOCX, or TXT files'}), 400
        
        # Get additional form data
        candidate_name = request.form.get('candidate_name', 'Anonymous Candidate')
        candidate_email = request.form.get('candidate_email', '')
        
        # Save the file
        resume_id = str(uuid.uuid4())
        filename = secure_filename(f"{resume_id}_{file.filename}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract text from the file
        resume_text = extract_text_from_file(file_path)
        
        if not resume_text.strip():
            os.remove(file_path)  # Clean up the file
            return jsonify({'error': 'Could not extract text from the resume'}), 400
        
        # Store resume data in database
        resume_id = db.create_resume(
            filename=file.filename,
            candidate_name=candidate_name,
            candidate_email=candidate_email,
            content=resume_text,
            file_path=file_path
        )
        
        # Process the resume with NLP
        nlp_processor.process_resume(resume_id, resume_text)
        
        # Refit corpus vectorizers if we have enough documents
        if len(nlp_processor.all_texts) >= 2:
            nlp_processor.fit_corpus_vectorizers()
            logger.info("Refitted corpus vectorizers after adding resume")
        
        return jsonify({
            'success': True,
            'resume_id': resume_id,
            'message': 'Resume uploaded and processed successfully'
        }), 201
    
    except Exception as e:
        logger.error(f"Error uploading resume: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/match', methods=['POST'])
def match_resumes():
    """Match resumes against a job description"""
    try:
        data = request.get_json()
        
        if not data or 'job_id' not in data:
            return jsonify({'error': 'Job ID is required'}), 400
        
        job_id = data['job_id']
        
        # Check if job exists
        job_desc = db.get_job_description(job_id)
        if not job_desc:
            return jsonify({'error': 'Job description not found'}), 404
        
        # Get all resumes and calculate enhanced matches
        matches_result = []
        resumes = db.get_resumes()
        
        logger.info(f"Processing matches for job {job_id} against {len(resumes)} resumes")
        
        # Ensure the job description is processed in the NLP processor
        if ENHANCED_NLP_AVAILABLE:
            # Enhanced processor uses job_data
            if job_id not in nlp_processor.job_data:
                content = f"{job_desc['description']} {job_desc['requirements']}"
                nlp_processor.add_job_description(job_id, job_desc)
        else:
            # Standard processor uses job_texts
            if job_id not in nlp_processor.job_texts:
                content = f"{job_desc['description']} {job_desc['requirements']}"
                nlp_processor.process_job_description(job_id, content)
        
        # Ensure corpus vectorizers are fitted before matching
        if len(nlp_processor.all_texts) >= 2 and not nlp_processor.corpus_fitted:
            logger.info("Fitting corpus vectorizers for matching...")
            nlp_processor.fit_corpus_vectorizers()
        
        for resume_data in resumes:
            resume_id = resume_data['id']
            
            # Ensure resume is processed in the NLP processor
            if ENHANCED_NLP_AVAILABLE:
                # Enhanced processor uses resume_data
                if resume_id not in nlp_processor.resume_data:
                    nlp_processor.add_resume(resume_id, resume_data)
            else:
                # Standard processor uses resume_texts
                if resume_id not in nlp_processor.resume_texts:
                    nlp_processor.process_resume(resume_id, resume_data['content'])
            
            # Debug logging
            logger.info(f"Calculating similarity for job {job_id} vs resume {resume_id}")
            
            # Calculate enhanced similarity with detailed analysis
            if ENHANCED_NLP_AVAILABLE:
                similarity_score, confidence_score = nlp_processor.calculate_similarity(job_id, resume_id)
            else:
                similarity_score = nlp_processor.calculate_similarity(job_id, resume_id)
                confidence_score = 0.5  # Default confidence for original processor
                
            match_details = nlp_processor.get_match_details(job_id, resume_id)
            
            logger.info(f"Similarity: {similarity_score:.3f}, Confidence: {confidence_score:.3f}, "
                       f"Match strength: {match_details.get('match_strength', 'unknown')}")
            
            # Determine match category
            match_category = match_details.get('match_strength', 'unknown')
            
            match_result = {
                'resume_id': resume_id,
                'candidate_name': resume_data['candidate_name'],
                'candidate_email': resume_data['candidate_email'],
                'filename': resume_data['filename'],
                'similarity_score': similarity_score,
                'confidence_score': confidence_score,
                'match_percentage': round(similarity_score * 100, 2),
                'confidence_percentage': round(confidence_score * 100, 2),
                'match_category': match_category,
                'uploaded_at': resume_data['uploaded_at'],
                'skills_analysis': match_details.get('skills_analysis', {}),
                'component_scores': match_details.get('component_scores', {}),
                'experience_analysis': match_details.get('experience_analysis', {}),
                'recommendations': match_details.get('recommendations', []),
                'metadata': match_details.get('metadata', {})
            }
            
            matches_result.append(match_result)
            
            # Store enhanced match in database
            skills_analysis = match_details.get('skills_analysis', {})
            db.create_match(
                job_id=job_id,
                resume_id=resume_id,
                similarity_score=similarity_score,
                common_skills=skills_analysis.get('matched_skills', []),
                missing_skills=skills_analysis.get('missing_skills', []),
                match_details=match_result
            )
        
        # Sort by similarity score (descending)
        matches_result.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'matches': matches_result,
            'total_candidates': len(matches_result)
        })
    
    except Exception as e:
        logger.error(f"Error matching resumes: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/resumes', methods=['GET'])
def get_resumes():
    """Get all uploaded resumes"""
    try:
        resumes = db.get_resumes()
        resume_list = []
        for resume_data in resumes:
            resume_list.append({
                'id': resume_data['id'],
                'candidate_name': resume_data['candidate_name'],
                'candidate_email': resume_data['candidate_email'],
                'filename': resume_data['filename'],
                'uploaded_at': resume_data['uploaded_at']
            })
        
        return jsonify({'resumes': resume_list})
    except Exception as e:
        logger.error(f"Error fetching resumes: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/matches', methods=['GET'])
def get_matches():
    """Get all match results"""
    try:
        matches = db.get_all_matches()
        return jsonify({'matches': matches})
    except Exception as e:
        logger.error(f"Error fetching matches: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/match/details/<job_id>/<resume_id>', methods=['GET'])
def get_detailed_match_analysis(job_id, resume_id):
    """Get comprehensive match analysis between a job and resume"""
    try:
        # Verify both job and resume exist
        job_desc = db.get_job_description(job_id)
        resume_data = db.get_resume(resume_id)
        
        if not job_desc:
            return jsonify({'error': 'Job description not found'}), 404
        if not resume_data:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Get detailed match analysis
        match_details = nlp_processor.get_match_details(job_id, resume_id)
        similarity_score = nlp_processor.calculate_similarity(job_id, resume_id)
        
        # Enhance with job and resume information
        detailed_analysis = {
            'job_info': {
                'id': job_desc['id'],
                'title': job_desc['title'],
                'company': job_desc.get('company', ''),
                'created_at': job_desc['created_at']
            },
            'resume_info': {
                'id': resume_data['id'],
                'candidate_name': resume_data['candidate_name'],
                'candidate_email': resume_data['candidate_email'],
                'filename': resume_data['filename'],
                'uploaded_at': resume_data['uploaded_at']
            },
            'match_analysis': match_details,
            'overall_score': similarity_score,
            'match_percentage': round(similarity_score * 100, 2)
        }
        
        return jsonify(detailed_analysis)
        
    except Exception as e:
        logger.error(f"Error getting detailed match analysis: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/resume/<resume_id>', methods=['GET'])
def get_resume_details(resume_id):
    """Get detailed information about a specific resume"""
    try:
        resume_data = db.get_resume(resume_id)
        if not resume_data:
            return jsonify({'error': 'Resume not found'}), 404
        
        return jsonify({
            'id': resume_data['id'],
            'candidate_name': resume_data['candidate_name'],
            'candidate_email': resume_data['candidate_email'],
            'filename': resume_data['filename'],
            'text': resume_data['content'][:1000] + '...' if len(resume_data['content']) > 1000 else resume_data['content'],
            'uploaded_at': resume_data['uploaded_at']
        })
    except Exception as e:
        logger.error(f"Error fetching resume details: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/candidate/matches/<resume_id>', methods=['GET'])
def find_matching_jobs_for_resume(resume_id):
    """Find matching jobs for a specific resume (candidate view)"""
    try:
        # Verify resume exists
        resume_data = db.get_resume(resume_id)
        if not resume_data:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Get all available job descriptions
        jobs = db.get_job_descriptions()
        job_matches = []
        
        logger.info(f"Finding job matches for resume {resume_id} against {len(jobs)} jobs")
        
        # Ensure corpus vectorizers are fitted before matching
        if len(nlp_processor.all_texts) >= 2 and not nlp_processor.corpus_fitted:
            logger.info("Fitting corpus vectorizers for candidate matching...")
            nlp_processor.fit_corpus_vectorizers()
        
        for job in jobs:
            job_id = job['id']
            
            # Debug logging
            logger.info(f"Calculating similarity for resume {resume_id} vs job {job_id}")
            
            # Calculate similarity (resume vs job, reversed from recruiter view)
            similarity_score = nlp_processor.calculate_similarity(job_id, resume_id)
            match_details = nlp_processor.get_match_details(job_id, resume_id)
            
            logger.info(f"Similarity score: {similarity_score}, Match strength: {match_details.get('match_strength', 'unknown')}")
            
            # Determine match category
            match_category = match_details.get('match_strength', 'unknown')
            
            job_match = {
                'job_id': job_id,
                'title': job['title'],
                'company': job['company'],
                'description_preview': job['description'][:200] + '...' if len(job['description']) > 200 else job['description'],
                'created_at': job['created_at'],
                'similarity_score': similarity_score,
                'match_percentage': round(similarity_score * 100, 2),
                'match_category': match_category,
                'skills_analysis': match_details.get('skills_analysis', {}),
                'component_scores': match_details.get('component_scores', {}),
                'recommendations': match_details.get('recommendations', [])
            }
            
            job_matches.append(job_match)
        
        # Sort by similarity score (descending) - best matches first
        job_matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'resume_id': resume_id,
            'candidate_name': resume_data['candidate_name'],
            'matching_jobs': job_matches,
            'total_jobs': len(job_matches)
        })
        
    except Exception as e:
        logger.error(f"Error finding matching jobs for resume: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/candidate/resumes', methods=['GET'])
def get_candidate_resumes():
    """Get resumes with their match summaries for candidate dashboard"""
    try:
        resumes = db.get_resumes()
        
        # Add match summary for each resume
        for resume in resumes:
            resume_id = resume['id']
            
            # Get job count and best match info
            jobs = db.get_job_descriptions()
            if jobs and len(nlp_processor.all_texts) >= 2:
                # Calculate best match for this resume
                best_match_score = 0
                best_job_title = None
                
                for job in jobs:
                    job_id = job['id']
                    try:
                        similarity = nlp_processor.calculate_similarity(job_id, resume_id)
                        if similarity > best_match_score:
                            best_match_score = similarity
                            best_job_title = job['title']
                    except:
                        continue
                
                resume['best_match_score'] = round(best_match_score * 100, 2)
                resume['best_match_job'] = best_job_title
                resume['total_jobs_available'] = len(jobs)
            else:
                resume['best_match_score'] = 0
                resume['best_match_job'] = None
                resume['total_jobs_available'] = 0
        
        return jsonify({
            'success': True,
            'resumes': resumes
        })
        
    except Exception as e:
        logger.error(f"Error fetching candidate resumes: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# New endpoints for enhanced features
@app.route('/api/feedback', methods=['POST'])
def add_feedback():
    """Add human feedback for a match to improve model accuracy"""
    try:
        if not ENHANCED_NLP_AVAILABLE:
            return jsonify({'error': 'Enhanced NLP features not available'}), 400
            
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['job_id', 'resume_id', 'human_score', 'recruiter_feedback', 'match_quality']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Add feedback to the enhanced processor
        nlp_processor.add_feedback(
            job_id=data['job_id'],
            resume_id=data['resume_id'],
            human_score=float(data['human_score']),
            recruiter_feedback=data['recruiter_feedback'],
            match_quality=data['match_quality']
        )
        
        return jsonify({
            'success': True,
            'message': 'Feedback added successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error adding feedback: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/validation/metrics', methods=['GET'])
def get_validation_metrics():
    """Get current model validation metrics"""
    try:
        if not ENHANCED_NLP_AVAILABLE:
            return jsonify({'error': 'Enhanced NLP features not available'}), 400
        
        metrics = nlp_processor.get_validation_metrics()
        return jsonify({
            'success': True,
            'metrics': metrics
        })
        
    except Exception as e:
        logger.error(f"Error getting validation metrics: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/validation/run-test', methods=['POST'])
def run_validation_test():
    """Run ground truth validation test"""
    try:
        if not ENHANCED_NLP_AVAILABLE or not validation_framework:
            return jsonify({'error': 'Validation framework not available'}), 400
        
        data = request.get_json() or {}
        test_name = data.get('test_name', f'validation_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        
        # Run ground truth validation
        results = validation_framework.run_ground_truth_validation(test_name)
        
        return jsonify({
            'success': True,
            'test_name': test_name,
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Error running validation test: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/validation/report', methods=['GET'])
def get_validation_report():
    """Get comprehensive validation report"""
    try:
        if not ENHANCED_NLP_AVAILABLE or not validation_framework:
            return jsonify({'error': 'Validation framework not available'}), 400
        
        test_name = request.args.get('test_name')
        report = validation_framework.generate_validation_report(test_name)
        
        return jsonify({
            'success': True,
            'report': report
        })
        
    except Exception as e:
        logger.error(f"Error generating validation report: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/system/status', methods=['GET'])
def get_system_status():
    """Get system status and capabilities"""
    try:
        status = {
            'enhanced_nlp_available': ENHANCED_NLP_AVAILABLE,
            'validation_framework_available': validation_framework is not None,
            'features': {
                'confidence_scoring': ENHANCED_NLP_AVAILABLE,
                'feedback_collection': ENHANCED_NLP_AVAILABLE,
                'bert_semantic_analysis': ENHANCED_NLP_AVAILABLE,
                'simplified_components': ENHANCED_NLP_AVAILABLE,
                'ground_truth_testing': validation_framework is not None
            }
        }
        
        if ENHANCED_NLP_AVAILABLE:
            # Get some basic stats
            try:
                validation_metrics = nlp_processor.get_validation_metrics()
                status['validation_metrics'] = validation_metrics
            except:
                status['validation_metrics'] = {'error': 'No validation data available'}
        
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        logger.error(f"Error getting system status: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
