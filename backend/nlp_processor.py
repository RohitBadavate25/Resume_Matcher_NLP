import numpy as np
import re
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import spacy

logger = logging.getLogger(__name__)

class ResumeMatcherNLP:
    def __init__(self):
        self.job_embeddings = {}
        self.resume_embeddings = {}
        self.job_texts = {}
        self.resume_texts = {}
        self.all_texts = []  # Store all texts for corpus-wide TF-IDF
        self.corpus_fitted = False
        
        # Initialize models
        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
            
            # Enhanced TF-IDF vectorizer for better corpus analysis
            logger.info("Initializing enhanced TF-IDF vectorizer...")
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=5000,   # Reasonable vocabulary size
                stop_words='english', # Use English stopwords for better results
                ngram_range=(1, 1),  # Use only unigrams to avoid sparsity issues
                lowercase=True,
                min_df=1,            # Include all terms for small datasets
                max_df=0.9,          # Remove very common terms
                sublinear_tf=True,   # Use sublinear TF scaling
                smooth_idf=True,
                norm='l2',           # L2 normalization
                use_idf=True
            )
            
            # Semantic similarity vectorizer (different params for raw text)
            self.semantic_vectorizer = TfidfVectorizer(
                max_features=3000,
                stop_words='english',  # Use stopwords for raw text analysis
                ngram_range=(1, 1),    # Use unigrams only to avoid sparsity
                lowercase=True,
                min_df=1,
                max_df=0.85,
                norm='l2'
            )
            
            # Try to load spaCy model for advanced NLP
            try:
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("spaCy model loaded successfully")
            except (OSError, ImportError):
                logger.warning("spaCy model not available, using fallback methods")
                self.nlp = None
            
            logger.info("Enhanced NLP models initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing NLP models: {str(e)}")
            raise

    def preprocess_text(self, text):
        """Clean and preprocess text for better matching - Less aggressive preprocessing"""
        try:
            # Convert to lowercase
            text = text.lower()
            
            # Remove excessive punctuation but keep important chars like +, #, .
            text = re.sub(r'[^\w\s\+\#\.\-/]', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            
            # Tokenize
            tokens = word_tokenize(text)
            
            # Less aggressive filtering - keep more terms
            processed_tokens = []
            for token in tokens:
                # Keep tokens that are:
                # 1. Not in stopwords OR
                # 2. Are technical terms (contain numbers, +, #) OR  
                # 3. Are at least 2 chars (not just 3+)
                if (token not in self.stop_words and len(token) >= 2) or \
                   any(char in token for char in ['+', '#', '.']) or \
                   any(char.isdigit() for char in token):
                    # Only lemmatize if it's a regular word (no special chars)
                    if token.isalpha() and len(token) > 2:
                        processed_tokens.append(self.lemmatizer.lemmatize(token))
                    else:
                        processed_tokens.append(token)
            
            return ' '.join(processed_tokens)
        
        except Exception as e:
            logger.error(f"Error preprocessing text: {str(e)}")
            return text

    def extract_skills(self, text):
        """Extract skills from text using comprehensive keyword matching and NLP"""
        try:
            # Comprehensive technical skills database
            skill_patterns = [
                # Programming Languages
                r'\b(?:python|java|javascript|typescript|c\+\+|c#|php|ruby|go|rust|swift|kotlin|scala|r|matlab|perl|shell|bash|powershell)\b',
                # Web Technologies
                r'\b(?:react|angular|vue|node\.?js|express|django|flask|spring|laravel|rails|asp\.net|nextjs|nuxt|gatsby)\b',
                r'\b(?:html|css|sass|less|scss|bootstrap|tailwind|material-ui|chakra|bulma|foundation)\b',
                # Databases
                r'\b(?:sql|mysql|postgresql|mongodb|redis|elasticsearch|cassandra|dynamodb|sqlite|oracle|mariadb|couchdb)\b',
                # Cloud & DevOps
                r'\b(?:aws|azure|gcp|google cloud|docker|kubernetes|jenkins|terraform|ansible|chef|puppet|vagrant)\b',
                r'\b(?:ci/cd|devops|microservices|serverless|lambda|api gateway|load balancer|nginx|apache)\b',
                # Data Science & ML
                r'\b(?:machine learning|deep learning|ai|artificial intelligence|nlp|computer vision|data science|big data)\b',
                r'\b(?:tensorflow|pytorch|scikit-learn|pandas|numpy|matplotlib|seaborn|jupyter|keras|xgboost|lightgbm)\b',
                r'\b(?:spark|hadoop|kafka|airflow|dask|mlflow|kubeflow|sagemaker)\b',
                # Methodologies & Frameworks
                r'\b(?:agile|scrum|kanban|lean|waterfall|tdd|bdd|solid|design patterns|microservices|rest|graphql|soap)\b',
                # Version Control & Tools
                r'\b(?:git|github|gitlab|bitbucket|svn|mercurial|jira|confluence|slack|teams)\b',
                # Mobile Development
                r'\b(?:ios|android|react native|flutter|xamarin|cordova|ionic|swift|objective-c)\b',
                # Testing
                r'\b(?:unit testing|integration testing|selenium|cypress|jest|mocha|pytest|junit|testng)\b',
                # Soft Skills
                r'\b(?:leadership|communication|problem solving|analytical thinking|teamwork|project management|time management)\b',
                # Industries
                r'\b(?:fintech|healthcare|e-commerce|education|gaming|automotive|blockchain|cryptocurrency)\b'
            ]
            
            skills = set()
            text_lower = text.lower()
            
            # Pattern-based extraction with proper word boundaries
            for pattern in skill_patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                # Clean up matches - remove empty strings and whitespace
                clean_matches = [match.strip() for match in matches if match.strip()]
                skills.update(clean_matches)
            
            # Enhanced extraction using spaCy if available
            if self.nlp:
                try:
                    doc = self.nlp(text)
                    
                    # Extract entities that might be skills (more selective)
                    for ent in doc.ents:
                        if ent.label_ in ['ORG', 'PRODUCT']:  # Focus on organizations and products
                            ent_text = ent.text.lower().strip()
                            # Only add if it looks like a technology/company name
                            if (len(ent_text) > 2 and len(ent_text) <= 20 and 
                                not any(char.isdigit() for char in ent_text) and
                                ent_text not in self.stop_words):
                                skills.add(ent_text)
                    
                    # Extract compound technical terms (more conservative)
                    for chunk in doc.noun_chunks:
                        chunk_text = chunk.text.lower().strip()
                        # Only extract 1-2 word technical compounds
                        if (1 <= len(chunk_text.split()) <= 2 and 
                            3 <= len(chunk_text) <= 25):
                            # Check if it contains technical indicators
                            tech_indicators = ['dev', 'script', 'code', 'data', 'web', 'api', 'sql', 'ml']
                            if any(indicator in chunk_text for indicator in tech_indicators):
                                skills.add(chunk_text)
                                
                except Exception as e:
                    logger.warning(f"Error in spaCy skill extraction: {str(e)}")
            
            # Additional extraction for certifications (more precise patterns)
            cert_patterns = [
                r'\b(aws certified [a-z\s]+)\b',
                r'\b(azure certified [a-z\s]+)\b', 
                r'\b(google cloud certified [a-z\s]+)\b',
                r'\b(cissp|ceh|comptia [a-z\+]+|pmp|scrum master)\b',
                r'\b(bachelor.{0,20}computer science|master.{0,20}computer science|computer science degree)\b',
                r'\b(bachelor.{0,20}engineering|master.{0,20}engineering|engineering degree)\b'
            ]
            
            for pattern in cert_patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                # Clean certification matches
                clean_matches = [match.strip()[:50] for match in matches if match.strip()]
                skills.update(clean_matches)
            
            # Clean and filter skills more aggressively
            cleaned_skills = []
            for skill in skills:
                skill = skill.strip()
                # More stringent filtering
                if (2 <= len(skill) <= 30 and           # Reasonable length
                    not skill.isdigit() and             # Not just numbers
                    skill not in self.stop_words and    # Not a stopword
                    not skill.startswith(('the ', 'and ', 'or ', 'in ', 'of ')) and  # No leading articles
                    skill.count(' ') <= 4):             # Max 5 words
                    cleaned_skills.append(skill)
            
            return list(set(cleaned_skills))  # Remove duplicates
        
        except Exception as e:
            logger.error(f"Error extracting skills: {str(e)}")
            return []

    def fit_corpus_vectorizers(self):
        """Fit TF-IDF vectorizers on the entire corpus for better accuracy"""
        try:
            if len(self.all_texts) < 2:
                logger.warning("Not enough texts to fit corpus vectorizers")
                return
            
            logger.info(f"Fitting vectorizers on corpus of {len(self.all_texts)} documents")
            
            # Fit main TF-IDF vectorizer
            self.tfidf_vectorizer.fit(self.all_texts)
            
            # Fit semantic vectorizer
            self.semantic_vectorizer.fit(self.all_texts)
            
            self.corpus_fitted = True
            logger.info("Corpus vectorizers fitted successfully")
            
        except Exception as e:
            logger.error(f"Error fitting corpus vectorizers: {str(e)}")

    def process_job_description(self, job_id, job_text):
        """Process and store job description"""
        try:
            logger.info(f"Processing job description: {job_id}")
            
            # Store original text
            self.job_texts[job_id] = job_text
            
            # Preprocess text
            processed_text = self.preprocess_text(job_text)
            self.job_embeddings[job_id] = processed_text
            
            # Add to corpus for vectorizer fitting
            if processed_text not in self.all_texts:
                self.all_texts.append(processed_text)
                self.corpus_fitted = False  # Need to refit
            
            logger.info(f"Job description {job_id} processed successfully")
            
        except Exception as e:
            logger.error(f"Error processing job description {job_id}: {str(e)}")
            raise

    def process_resume(self, resume_id, resume_text):
        """Process and store resume"""
        try:
            logger.info(f"Processing resume: {resume_id}")
            
            # Store original text
            self.resume_texts[resume_id] = resume_text
            
            # Preprocess text
            processed_text = self.preprocess_text(resume_text)
            self.resume_embeddings[resume_id] = processed_text
            
            # Add to corpus for vectorizer fitting
            if processed_text not in self.all_texts:
                self.all_texts.append(processed_text)
                self.corpus_fitted = False  # Need to refit
            
            logger.info(f"Resume {resume_id} processed successfully")
            
        except Exception as e:
            logger.error(f"Error processing resume {resume_id}: {str(e)}")
            raise

    def calculate_similarity(self, job_id, resume_id):
        """Calculate enhanced similarity between job description and resume"""
        try:
            if job_id not in self.job_embeddings or resume_id not in self.resume_embeddings:
                logger.warning(f"Missing embeddings for job {job_id} or resume {resume_id}")
                return 0.0
            
            # Ensure vectorizers are fitted on corpus
            if not self.corpus_fitted and len(self.all_texts) >= 2:
                self.fit_corpus_vectorizers()
            
            # Get processed texts
            job_text = self.job_embeddings[job_id]
            resume_text = self.resume_embeddings[resume_id]
            
            # Calculate corpus-based TF-IDF similarity with fallback
            if self.corpus_fitted:
                try:
                    job_vector = self.tfidf_vectorizer.transform([job_text])
                    resume_vector = self.tfidf_vectorizer.transform([resume_text])
                    tfidf_similarity = cosine_similarity(job_vector, resume_vector)[0][0]
                except Exception as e:
                    logger.warning(f"Corpus TF-IDF failed: {e}, using fallback")
                    tfidf_similarity = self._fallback_text_similarity(job_text, resume_text)
            else:
                # Fallback to pairwise TF-IDF
                try:
                    texts = [job_text, resume_text]
                    tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
                    tfidf_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                except Exception as e:
                    logger.warning(f"Pairwise TF-IDF failed: {e}, using fallback")
                    tfidf_similarity = self._fallback_text_similarity(job_text, resume_text)
            
            # Calculate additional similarity metrics
            semantic_similarity = self.calculate_semantic_similarity(job_id, resume_id)
            skill_similarity = self.calculate_skill_similarity(job_id, resume_id)
            keyword_similarity = self.calculate_keyword_similarity(job_id, resume_id)
            context_similarity = self.calculate_context_similarity(job_id, resume_id)
            
            # Enhanced weighted combination with better balance
            # If TF-IDF is very low, rely more on skills and keywords
            if tfidf_similarity < 0.1:
                final_similarity = (
                    0.15 * tfidf_similarity +      # Reduced when TF-IDF fails
                    0.40 * skill_similarity +      # Increased skill importance
                    0.15 * semantic_similarity +   # Semantic understanding
                    0.25 * keyword_similarity +    # Increased keyword importance
                    0.05 * context_similarity      # Context and structure
                )
            else:
                final_similarity = (
                    0.30 * tfidf_similarity +      # Main content similarity
                    0.30 * skill_similarity +      # Skill matching (very important)
                    0.20 * semantic_similarity +   # Semantic understanding
                    0.15 * keyword_similarity +    # Important keyword matching
                    0.05 * context_similarity      # Context and structure
                )
            
            # Apply non-linear transformation for better discrimination
            final_similarity = self.apply_similarity_transformation(final_similarity)
            
            return max(0.0, min(1.0, final_similarity))
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0

    def calculate_semantic_similarity(self, job_id, resume_id):
        """Calculate semantic similarity between texts using corpus-fitted vectorizer"""
        try:
            job_text = self.job_texts.get(job_id, '')
            resume_text = self.resume_texts.get(resume_id, '')
            
            if not job_text or not resume_text:
                return 0.0
            
            # Use corpus-fitted semantic vectorizer on raw texts
            try:
                if self.corpus_fitted:
                    job_vector = self.semantic_vectorizer.transform([job_text])
                    resume_vector = self.semantic_vectorizer.transform([resume_text])
                    similarity = cosine_similarity(job_vector, resume_vector)[0][0]
                else:
                    # Always use fallback method for semantic similarity
                    texts = [job_text, resume_text]
                    temp_vectorizer = TfidfVectorizer(
                        max_features=2000, 
                        stop_words='english', 
                        ngram_range=(1, 1),  # Use unigrams only
                        min_df=1,
                        lowercase=True
                    )
                    try:
                        tfidf_matrix = temp_vectorizer.fit_transform(texts)
                        if tfidf_matrix.shape[1] > 0:  # Check if any features were extracted
                            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                        else:
                            similarity = self._fallback_text_similarity(job_text, resume_text)
                    except Exception:
                        similarity = self._fallback_text_similarity(job_text, resume_text)
                        
            except Exception:
                similarity = self._fallback_text_similarity(job_text, resume_text)
            
            return max(0.0, min(1.0, similarity))
            
        except Exception as e:
            logger.error(f"Error calculating semantic similarity: {str(e)}")
            return 0.0

    def calculate_keyword_similarity(self, job_id, resume_id):
        """Calculate similarity based on important keywords and phrases"""
        try:
            job_text = self.job_texts.get(job_id, '').lower()
            resume_text = self.resume_texts.get(resume_id, '').lower()
            
            if not job_text or not resume_text:
                return 0.0
            
            # Important keywords for job matching
            important_keywords = [
                'experience', 'years', 'senior', 'junior', 'lead', 'manager',
                'required', 'preferred', 'must', 'should', 'bachelor', 'master',
                'degree', 'certification', 'remote', 'onsite', 'full-time', 'part-time'
            ]
            
            job_keywords = set()
            resume_keywords = set()
            
            for keyword in important_keywords:
                if keyword in job_text:
                    job_keywords.add(keyword)
                if keyword in resume_text:
                    resume_keywords.add(keyword)
            
            if not job_keywords:
                return 0.5  # Neutral score if no important keywords found
            
            # Calculate Jaccard similarity for keywords
            intersection = len(job_keywords.intersection(resume_keywords))
            union = len(job_keywords.union(resume_keywords))
            
            return intersection / union if union > 0 else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating keyword similarity: {str(e)}")
            return 0.0

    def calculate_context_similarity(self, job_id, resume_id):
        """Calculate similarity based on document structure and context"""
        try:
            job_text = self.job_texts.get(job_id, '')
            resume_text = self.resume_texts.get(resume_id, '')
            
            if not job_text or not resume_text:
                return 0.0
            
            # Analyze document structure
            job_sections = self.analyze_document_structure(job_text)
            resume_sections = self.analyze_document_structure(resume_text)
            
            # Compare section relevance
            section_similarity = 0.0
            total_sections = len(job_sections)
            
            if total_sections > 0:
                for section, job_content in job_sections.items():
                    if section in resume_sections:
                        resume_content = resume_sections[section]
                        if job_content and resume_content:
                            # Quick TF-IDF on section content
                            texts = [job_content, resume_content]
                            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
                            try:
                                vectors = vectorizer.fit_transform(texts)
                                similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
                                section_similarity += similarity
                            except:
                                pass
                
                section_similarity /= total_sections
            
            return section_similarity
            
        except Exception as e:
            logger.error(f"Error calculating context similarity: {str(e)}")
            return 0.0

    def analyze_document_structure(self, text):
        """Analyze document structure to identify sections"""
        sections = {}
        lines = text.split('\n')
        current_section = 'general'
        current_content = []
        
        section_headers = {
            'experience': ['experience', 'work history', 'employment', 'professional experience'],
            'education': ['education', 'academic', 'degree', 'university', 'college'],
            'skills': ['skills', 'technical skills', 'technologies', 'competencies'],
            'requirements': ['requirements', 'qualifications', 'must have', 'required'],
            'responsibilities': ['responsibilities', 'duties', 'job description', 'role'],
        }
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if line is a section header
            section_found = None
            for section, keywords in section_headers.items():
                if any(keyword in line_lower for keyword in keywords):
                    section_found = section
                    break
            
            if section_found:
                # Save previous section
                if current_content:
                    sections[current_section] = ' '.join(current_content)
                
                # Start new section
                current_section = section_found
                current_content = []
            else:
                if line.strip():  # Non-empty line
                    current_content.append(line.strip())
        
        # Save last section
        if current_content:
            sections[current_section] = ' '.join(current_content)
        
        return sections

    def apply_similarity_transformation(self, similarity):
        """Apply mild non-linear transformation to improve similarity discrimination"""
        try:
            # Apply a gentler transformation that doesn't overly penalize moderate scores
            if similarity < 0.1:
                # Boost very low scores slightly
                transformed = similarity * 1.2
            elif similarity < 0.5:
                # Gentle boost for low-moderate scores
                transformed = similarity * 1.1
            elif similarity < 0.8:
                # Keep moderate-high scores as is
                transformed = similarity
            else:
                # Slightly boost high scores
                transformed = min(1.0, similarity * 1.05)
            
            return max(0.0, min(1.0, transformed))
            
        except Exception as e:
            logger.error(f"Error applying similarity transformation: {str(e)}")
            return similarity

    def calculate_skill_similarity(self, job_id, resume_id):
        """Calculate enhanced skill-based similarity with weighted matching"""
        try:
            job_text = self.job_texts.get(job_id, '')
            resume_text = self.resume_texts.get(resume_id, '')
            
            if not job_text or not resume_text:
                return 0.0
            
            job_skills = set(self.extract_skills(job_text))
            resume_skills = set(self.extract_skills(resume_text))
            
            if not job_skills:
                return 0.0
            
            # Enhanced skill matching with priority weights
            skill_weights = self.get_skill_weights(job_skills)
            
            # Calculate weighted skill similarity
            matched_weight = 0.0
            total_weight = sum(skill_weights.values())
            
            for skill in job_skills:
                if skill in resume_skills:
                    matched_weight += skill_weights.get(skill, 1.0)
            
            weighted_similarity = matched_weight / total_weight if total_weight > 0 else 0.0
            
            # Also calculate traditional Jaccard similarity
            intersection = len(job_skills.intersection(resume_skills))
            union = len(job_skills.union(resume_skills))
            jaccard_similarity = intersection / union if union > 0 else 0.0
            
            # Combine weighted and Jaccard similarities
            final_skill_similarity = 0.7 * weighted_similarity + 0.3 * jaccard_similarity
            
            return final_skill_similarity
            
        except Exception as e:
            logger.error(f"Error calculating skill similarity: {str(e)}")
            return 0.0

    def get_skill_weights(self, skills):
        """Assign weights to skills based on their importance and rarity"""
        weights = {}
        
        # High-value technical skills
        high_value_skills = {
            'python', 'java', 'javascript', 'react', 'node.js', 'aws', 'docker', 'kubernetes',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'sql', 'mongodb',
            'microservices', 'devops', 'ci/cd', 'agile', 'scrum', 'leadership', 'architect'
        }
        
        # Medium-value skills
        medium_value_skills = {
            'html', 'css', 'git', 'linux', 'testing', 'debugging', 'problem solving',
            'communication', 'teamwork', 'project management'
        }
        
        for skill in skills:
            skill_lower = skill.lower()
            if any(hv_skill in skill_lower for hv_skill in high_value_skills):
                weights[skill] = 3.0
            elif any(mv_skill in skill_lower for mv_skill in medium_value_skills):
                weights[skill] = 2.0
            else:
                weights[skill] = 1.0
        
        return weights

    def get_match_details(self, job_id, resume_id):
        """Get comprehensive match information with detailed analysis"""
        try:
            job_text = self.job_texts.get(job_id, '')
            resume_text = self.resume_texts.get(resume_id, '')
            
            if not job_text or not resume_text:
                return {}
            
            job_skills = self.extract_skills(job_text)
            resume_skills = self.extract_skills(resume_text)
            
            matched_skills = list(set(job_skills).intersection(set(resume_skills)))
            missing_skills = list(set(job_skills) - set(resume_skills))
            extra_skills = list(set(resume_skills) - set(job_skills))
            
            # Calculate individual similarity components
            tfidf_sim = self.calculate_similarity(job_id, resume_id)
            semantic_sim = self.calculate_semantic_similarity(job_id, resume_id)
            skill_sim = self.calculate_skill_similarity(job_id, resume_id)
            keyword_sim = self.calculate_keyword_similarity(job_id, resume_id)
            context_sim = self.calculate_context_similarity(job_id, resume_id)
            
            # Analyze skill importance
            skill_weights = self.get_skill_weights(job_skills)
            high_priority_matched = [s for s in matched_skills if skill_weights.get(s, 1.0) >= 2.5]
            high_priority_missing = [s for s in missing_skills if skill_weights.get(s, 1.0) >= 2.5]
            
            # Calculate experience level match (if extractable)
            experience_match = self.calculate_experience_match(job_text, resume_text)
            
            return {
                'overall_similarity': tfidf_sim,
                'component_scores': {
                    'tfidf_similarity': tfidf_sim,
                    'semantic_similarity': semantic_sim,
                    'skill_similarity': skill_sim,
                    'keyword_similarity': keyword_sim,
                    'context_similarity': context_sim
                },
                'skills_analysis': {
                    'job_skills': job_skills,
                    'resume_skills': resume_skills,
                    'matched_skills': matched_skills,
                    'missing_skills': missing_skills,
                    'extra_skills': extra_skills,
                    'high_priority_matched': high_priority_matched,
                    'high_priority_missing': high_priority_missing,
                    'skill_match_ratio': len(matched_skills) / len(job_skills) if job_skills else 0,
                    'skill_coverage': len(matched_skills) / len(set(job_skills + resume_skills)) if (job_skills or resume_skills) else 0
                },
                'experience_analysis': experience_match,
                'match_strength': self.categorize_match_strength(tfidf_sim),
                'recommendations': self.generate_recommendations(matched_skills, missing_skills, high_priority_missing)
            }
            
        except Exception as e:
            logger.error(f"Error getting match details: {str(e)}")
            return {}

    def calculate_experience_match(self, job_text, resume_text):
        """Extract and compare experience requirements"""
        try:
            # Extract years of experience from job description
            job_exp_pattern = r'(\d+)[\s\-+]*(?:years?|yrs?)[\s\-+]*(?:of\s+)?(?:experience|exp)'
            job_matches = re.findall(job_exp_pattern, job_text.lower())
            
            # Extract years of experience from resume
            resume_exp_pattern = r'(\d+)[\s\-+]*(?:years?|yrs?)[\s\-+]*(?:of\s+)?(?:experience|exp)'
            resume_matches = re.findall(resume_exp_pattern, resume_text.lower())
            
            job_years = max([int(match) for match in job_matches]) if job_matches else None
            resume_years = max([int(match) for match in resume_matches]) if resume_matches else None
            
            if job_years is None or resume_years is None:
                return {'status': 'unknown', 'job_years': job_years, 'resume_years': resume_years}
            
            if resume_years >= job_years:
                return {'status': 'meets_requirement', 'job_years': job_years, 'resume_years': resume_years}
            elif resume_years >= job_years * 0.8:  # Within 20% of requirement
                return {'status': 'close_match', 'job_years': job_years, 'resume_years': resume_years}
            else:
                return {'status': 'below_requirement', 'job_years': job_years, 'resume_years': resume_years}
                
        except Exception as e:
            logger.error(f"Error calculating experience match: {str(e)}")
            return {'status': 'error'}

    def categorize_match_strength(self, similarity_score):
        """Categorize match strength based on similarity score"""
        if similarity_score >= 0.8:
            return 'excellent'
        elif similarity_score >= 0.6:
            return 'good'
        elif similarity_score >= 0.4:
            return 'fair'
        elif similarity_score >= 0.2:
            return 'poor'
        else:
            return 'very_poor'

    def generate_recommendations(self, matched_skills, missing_skills, high_priority_missing):
        """Generate recommendations for improving the match"""
        recommendations = []
        
        if high_priority_missing:
            recommendations.append({
                'type': 'critical_skills',
                'message': f"Critical skills missing: {', '.join(high_priority_missing[:3])}",
                'priority': 'high'
            })
        
        if len(missing_skills) > len(matched_skills):
            recommendations.append({
                'type': 'skill_gap',
                'message': "Significant skill gap detected. Consider additional training or experience.",
                'priority': 'medium'
            })
        
        if len(matched_skills) > 0:
            recommendations.append({
                'type': 'strengths',
                'message': f"Strong match in: {', '.join(matched_skills[:3])}",
                'priority': 'positive'
            })
        
        return recommendations

    def _fallback_text_similarity(self, text1, text2):
        """Fallback similarity calculation using simple token overlap"""
        try:
            # Simple token-based similarity as fallback
            tokens1 = set(text1.lower().split())
            tokens2 = set(text2.lower().split())
            
            # Remove very short tokens and common words
            tokens1 = {t for t in tokens1 if len(t) > 2 and t not in self.stop_words}
            tokens2 = {t for t in tokens2 if len(t) > 2 and t not in self.stop_words}
            
            if not tokens1 or not tokens2:
                return 0.0
            
            intersection = len(tokens1.intersection(tokens2))
            union = len(tokens1.union(tokens2))
            
            return intersection / union if union > 0 else 0.0
            
        except Exception as e:
            logger.error(f"Fallback similarity failed: {e}")
            return 0.0
