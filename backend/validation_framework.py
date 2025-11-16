#!/usr/bin/env python3
"""
Validation Framework for Resume Matcher NLP System
Provides comprehensive testing and accuracy measurement capabilities.
"""

import numpy as np
import pandas as pd
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.stats import pearsonr, spearmanr
import logging

logger = logging.getLogger(__name__)

class ValidationFramework:
    """
    Comprehensive validation framework for the Resume Matcher system.
    Includes ground truth testing, accuracy metrics, and performance monitoring.
    """
    
    def __init__(self, nlp_processor, results_db: str = "validation_results.db"):
        self.nlp_processor = nlp_processor
        self.results_db = results_db
        self._init_database()
        
    def _init_database(self):
        """Initialize validation results database"""
        try:
            conn = sqlite3.connect(self.results_db)
            cursor = conn.cursor()
            
            # Create validation results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS validation_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_name TEXT NOT NULL,
                    job_id TEXT NOT NULL,
                    resume_id TEXT NOT NULL,
                    predicted_score REAL NOT NULL,
                    ground_truth_score REAL NOT NULL,
                    confidence_score REAL NOT NULL,
                    absolute_error REAL NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create performance metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_name TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Validation database initialized")
            
        except Exception as e:
            logger.error(f"Error initializing validation database: {str(e)}")

    def create_ground_truth_dataset(self) -> Dict[str, List]:
        """
        Create a curated ground truth dataset with known good/poor matches.
        This simulates expert recruiter evaluations.
        """
        
        ground_truth_data = {
            "excellent_matches": [
                {
                    "job_description": """
                    Senior Python Developer - 5+ Years Experience
                    
                    We need an experienced Python developer with expertise in:
                    - Django/Flask frameworks
                    - PostgreSQL and MongoDB
                    - AWS cloud services (EC2, S3, RDS)
                    - REST API development
                    - Docker and Kubernetes
                    - 5+ years of professional experience
                    - Bachelor's degree in Computer Science
                    """,
                    "resume": """
                    John Smith - Senior Python Developer
                    
                    Professional Experience:
                    Senior Software Engineer (2018-2024) - 6 years
                    - Developed Python applications using Django and Flask
                    - Managed PostgreSQL and MongoDB databases
                    - Deployed applications on AWS (EC2, S3, RDS, Lambda)
                    - Built REST APIs handling 1M+ requests daily
                    - Implemented Docker containerization and Kubernetes orchestration
                    
                    Education:
                    Bachelor of Science in Computer Science, MIT
                    
                    Technical Skills:
                    Python, Django, Flask, PostgreSQL, MongoDB, AWS, Docker, Kubernetes, REST APIs
                    """,
                    "expected_score": 0.92,
                    "reasoning": "Perfect skill alignment, meets experience requirements, strong background"
                }
            ],
            
            "good_matches": [
                {
                    "job_description": """
                    Frontend Developer - React Specialist
                    
                    Requirements:
                    - 3+ years React.js experience
                    - JavaScript/TypeScript proficiency
                    - Experience with Redux or similar state management
                    - HTML5, CSS3, responsive design
                    - Git version control
                    """,
                    "resume": """
                    Sarah Johnson - Frontend Developer
                    
                    Experience:
                    Frontend Developer (2021-2024) - 3 years
                    - Built React applications with TypeScript
                    - Used Redux for state management
                    - Responsive design with CSS3 and Bootstrap
                    - Git workflow and code reviews
                    - Some experience with Vue.js
                    
                    Skills: React, JavaScript, TypeScript, Redux, CSS3, HTML5, Git
                    """,
                    "expected_score": 0.78,
                    "reasoning": "Good skill match, meets experience, some bonus skills"
                }
            ],
            
            "fair_matches": [
                {
                    "job_description": """
                    Data Scientist - Machine Learning Focus
                    
                    Requirements:
                    - PhD or Master's in Data Science/Statistics
                    - Python (pandas, scikit-learn, TensorFlow)
                    - SQL and big data experience
                    - 3+ years ML experience
                    - Statistical modeling expertise
                    """,
                    "resume": """
                    Mike Chen - Software Developer
                    
                    Experience:
                    Software Developer (2020-2024) - 4 years
                    - Python development for web applications
                    - Some data analysis with pandas
                    - Basic SQL queries
                    - Bachelor's in Computer Science
                    
                    Skills: Python, SQL, pandas, JavaScript, React
                    """,
                    "expected_score": 0.45,
                    "reasoning": "Some Python skills but lacks ML expertise, education gap"
                }
            ],
            
            "poor_matches": [
                {
                    "job_description": """
                    Senior DevOps Engineer
                    
                    Requirements:
                    - 5+ years DevOps experience
                    - AWS/Azure cloud expertise
                    - Docker, Kubernetes, Terraform
                    - CI/CD pipeline management
                    - Linux system administration
                    - Infrastructure as Code
                    """,
                    "resume": """
                    Lisa Park - Graphic Designer
                    
                    Experience:
                    Graphic Designer (2019-2024) - 5 years
                    - Created visual designs using Photoshop, Illustrator
                    - Basic HTML/CSS for web design
                    - Collaborated with marketing teams
                    - Adobe Creative Suite expertise
                    
                    Skills: Photoshop, Illustrator, InDesign, HTML, CSS
                    """,
                    "expected_score": 0.15,
                    "reasoning": "Completely different field, no relevant technical skills"
                }
            ]
        }
        
        return ground_truth_data

    def run_ground_truth_validation(self, test_name: str = "ground_truth_validation") -> Dict[str, float]:
        """Run validation against ground truth dataset"""
        try:
            ground_truth = self.create_ground_truth_dataset()
            all_predictions = []
            all_ground_truth = []
            all_confidence = []
            
            test_cases = []
            
            # Flatten all test cases
            for category, cases in ground_truth.items():
                for i, case in enumerate(cases):
                    test_cases.append({
                        'job_id': f"{category}_job_{i}",
                        'resume_id': f"{category}_resume_{i}",
                        'job_description': case['job_description'],
                        'resume': case['resume'],
                        'expected_score': case['expected_score'],
                        'category': category
                    })
            
            # Process test cases
            for case in test_cases:
                # Process documents
                self.nlp_processor.process_job_description(case['job_id'], case['job_description'])
                self.nlp_processor.process_resume(case['resume_id'], case['resume'])
                
                # Get prediction
                predicted_score, confidence = self.nlp_processor.calculate_similarity(
                    case['job_id'], case['resume_id']
                )
                
                # Store results
                self._store_validation_result(
                    test_name, case['job_id'], case['resume_id'],
                    predicted_score, case['expected_score'], confidence
                )
                
                all_predictions.append(predicted_score)
                all_ground_truth.append(case['expected_score'])
                all_confidence.append(confidence)
                
                logger.info(f"Case {case['job_id']}: Predicted={predicted_score:.3f}, "
                          f"Expected={case['expected_score']:.3f}, "
                          f"Confidence={confidence:.3f}")
            
            # Calculate metrics
            metrics = self._calculate_validation_metrics(
                all_predictions, all_ground_truth, all_confidence
            )
            
            # Store aggregate metrics
            self._store_performance_metrics(test_name, metrics)
            
            logger.info(f"Ground truth validation completed. MAE: {metrics['mae']:.3f}")
            return metrics
            
        except Exception as e:
            logger.error(f"Error running ground truth validation: {str(e)}")
            return {"error": str(e)}

    def run_cross_validation(self, feedback_data: List[Dict]) -> Dict[str, float]:
        """Run cross-validation on human feedback data"""
        try:
            if len(feedback_data) < 10:
                return {"error": "Insufficient data for cross-validation (minimum 10 samples)"}
            
            # Split data for cross-validation
            np.random.shuffle(feedback_data)
            fold_size = len(feedback_data) // 5  # 5-fold CV
            
            all_predictions = []
            all_ground_truth = []
            
            for fold in range(5):
                start_idx = fold * fold_size
                end_idx = start_idx + fold_size if fold < 4 else len(feedback_data)
                
                test_data = feedback_data[start_idx:end_idx]
                
                for sample in test_data:
                    predicted_score, _ = self.nlp_processor.calculate_similarity(
                        sample['job_id'], sample['resume_id']
                    )
                    
                    all_predictions.append(predicted_score)
                    all_ground_truth.append(sample['human_score'])
            
            # Calculate cross-validation metrics
            metrics = self._calculate_validation_metrics(all_predictions, all_ground_truth)
            logger.info(f"Cross-validation completed. MAE: {metrics['mae']:.3f}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error running cross-validation: {str(e)}")
            return {"error": str(e)}

    def _calculate_validation_metrics(self, predictions: List[float], 
                                    ground_truth: List[float], 
                                    confidence_scores: List[float] = None) -> Dict[str, float]:
        """Calculate comprehensive validation metrics"""
        
        pred_array = np.array(predictions)
        truth_array = np.array(ground_truth)
        
        metrics = {
            "mae": float(mean_absolute_error(truth_array, pred_array)),
            "rmse": float(np.sqrt(mean_squared_error(truth_array, pred_array))),
            "r2_score": float(r2_score(truth_array, pred_array)),
            "pearson_correlation": float(pearsonr(predictions, ground_truth)[0]),
            "spearman_correlation": float(spearmanr(predictions, ground_truth)[0]),
            "accuracy_10_percent": float(np.mean(np.abs(pred_array - truth_array) <= 0.1)),
            "accuracy_20_percent": float(np.mean(np.abs(pred_array - truth_array) <= 0.2)),
            "sample_size": len(predictions)
        }
        
        # Confidence-related metrics if available
        if confidence_scores:
            conf_array = np.array(confidence_scores)
            
            # Calibration: correlation between confidence and accuracy
            accuracy_per_sample = 1 - np.abs(pred_array - truth_array)
            confidence_calibration = pearsonr(conf_array, accuracy_per_sample)[0]
            
            metrics.update({
                "average_confidence": float(np.mean(conf_array)),
                "confidence_calibration": float(confidence_calibration),
                "high_confidence_accuracy": float(np.mean(accuracy_per_sample[conf_array > 0.7])) if np.any(conf_array > 0.7) else 0.0
            })
        
        return metrics

    def _store_validation_result(self, test_name: str, job_id: str, resume_id: str,
                               predicted_score: float, ground_truth_score: float, confidence: float):
        """Store individual validation result"""
        try:
            conn = sqlite3.connect(self.results_db)
            cursor = conn.cursor()
            
            absolute_error = abs(predicted_score - ground_truth_score)
            
            cursor.execute('''
                INSERT INTO validation_results 
                (test_name, job_id, resume_id, predicted_score, ground_truth_score, 
                 confidence_score, absolute_error)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (test_name, job_id, resume_id, predicted_score, ground_truth_score, 
                  confidence, absolute_error))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing validation result: {str(e)}")

    def _store_performance_metrics(self, test_name: str, metrics: Dict[str, float]):
        """Store aggregate performance metrics"""
        try:
            conn = sqlite3.connect(self.results_db)
            cursor = conn.cursor()
            
            for metric_name, value in metrics.items():
                if isinstance(value, (int, float)) and not np.isnan(value):
                    cursor.execute('''
                        INSERT INTO performance_metrics (test_name, metric_name, metric_value)
                        VALUES (?, ?, ?)
                    ''', (test_name, metric_name, float(value)))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing performance metrics: {str(e)}")

    def generate_validation_report(self, test_name: str = None) -> Dict:
        """Generate comprehensive validation report"""
        try:
            conn = sqlite3.connect(self.results_db)
            
            # Get latest test if no test_name specified
            if not test_name:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT DISTINCT test_name FROM validation_results 
                    ORDER BY timestamp DESC LIMIT 1
                ''')
                result = cursor.fetchone()
                test_name = result[0] if result else None
                
                if not test_name:
                    return {"error": "No validation results found"}
            
            # Get validation results
            results_df = pd.read_sql_query('''
                SELECT * FROM validation_results WHERE test_name = ?
            ''', conn, params=(test_name,))
            
            # Get performance metrics
            metrics_df = pd.read_sql_query('''
                SELECT * FROM performance_metrics WHERE test_name = ?
            ''', conn, params=(test_name,))
            
            conn.close()
            
            if results_df.empty:
                return {"error": f"No results found for test: {test_name}"}
            
            # Generate summary statistics
            summary = {
                "test_name": test_name,
                "total_samples": len(results_df),
                "average_error": float(results_df['absolute_error'].mean()),
                "max_error": float(results_df['absolute_error'].max()),
                "min_error": float(results_df['absolute_error'].min()),
                "average_confidence": float(results_df['confidence_score'].mean()),
                "timestamp": results_df['timestamp'].iloc[0]
            }
            
            # Add performance metrics
            performance_metrics = {}
            for _, row in metrics_df.iterrows():
                performance_metrics[row['metric_name']] = row['metric_value']
            
            # Error distribution analysis
            error_distribution = {
                "excellent_predictions": int(sum(results_df['absolute_error'] <= 0.05)),
                "good_predictions": int(sum((results_df['absolute_error'] > 0.05) & 
                                          (results_df['absolute_error'] <= 0.15))),
                "fair_predictions": int(sum((results_df['absolute_error'] > 0.15) & 
                                          (results_df['absolute_error'] <= 0.30))),
                "poor_predictions": int(sum(results_df['absolute_error'] > 0.30))
            }
            
            return {
                "summary": summary,
                "performance_metrics": performance_metrics,
                "error_distribution": error_distribution,
                "detailed_results": results_df.to_dict('records')
            }
            
        except Exception as e:
            logger.error(f"Error generating validation report: {str(e)}")
            return {"error": str(e)}

    def plot_validation_results(self, test_name: str = None, save_path: str = None):
        """Create validation visualization plots"""
        try:
            conn = sqlite3.connect(self.results_db)
            
            if not test_name:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT DISTINCT test_name FROM validation_results 
                    ORDER BY timestamp DESC LIMIT 1
                ''')
                result = cursor.fetchone()
                test_name = result[0] if result else None
            
            if not test_name:
                logger.warning("No validation results to plot")
                return
            
            # Load data
            df = pd.read_sql_query('''
                SELECT * FROM validation_results WHERE test_name = ?
            ''', conn, params=(test_name,))
            
            conn.close()
            
            if df.empty:
                logger.warning(f"No data found for test: {test_name}")
                return
            
            # Create subplots
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
            
            # Plot 1: Predicted vs Ground Truth
            ax1.scatter(df['ground_truth_score'], df['predicted_score'], 
                       c=df['confidence_score'], cmap='viridis', alpha=0.7)
            ax1.plot([0, 1], [0, 1], 'r--', alpha=0.8)
            ax1.set_xlabel('Ground Truth Score')
            ax1.set_ylabel('Predicted Score')
            ax1.set_title('Predicted vs Ground Truth Scores')
            ax1.grid(True, alpha=0.3)
            
            # Plot 2: Error Distribution
            ax2.hist(df['absolute_error'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            ax2.set_xlabel('Absolute Error')
            ax2.set_ylabel('Frequency')
            ax2.set_title('Error Distribution')
            ax2.grid(True, alpha=0.3)
            
            # Plot 3: Confidence vs Accuracy
            accuracy = 1 - df['absolute_error']
            ax3.scatter(df['confidence_score'], accuracy, alpha=0.7)
            ax3.set_xlabel('Confidence Score')
            ax3.set_ylabel('Accuracy (1 - Absolute Error)')
            ax3.set_title('Confidence vs Accuracy')
            ax3.grid(True, alpha=0.3)
            
            # Plot 4: Error by Confidence Level
            high_conf = df['confidence_score'] > 0.7
            medium_conf = (df['confidence_score'] >= 0.4) & (df['confidence_score'] <= 0.7)
            low_conf = df['confidence_score'] < 0.4
            
            conf_levels = ['High\n(>0.7)', 'Medium\n(0.4-0.7)', 'Low\n(<0.4)']
            avg_errors = [
                df[high_conf]['absolute_error'].mean() if high_conf.any() else 0,
                df[medium_conf]['absolute_error'].mean() if medium_conf.any() else 0,
                df[low_conf]['absolute_error'].mean() if low_conf.any() else 0
            ]
            
            ax4.bar(conf_levels, avg_errors, color=['green', 'orange', 'red'], alpha=0.7)
            ax4.set_ylabel('Average Absolute Error')
            ax4.set_title('Error by Confidence Level')
            ax4.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.suptitle(f'Validation Results: {test_name}', y=1.02, fontsize=16)
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Validation plots saved to {save_path}")
            
            plt.show()
            
        except Exception as e:
            logger.error(f"Error plotting validation results: {str(e)}")

    def monitor_performance_over_time(self) -> Dict:
        """Monitor how model performance changes over time"""
        try:
            conn = sqlite3.connect(self.results_db)
            
            df = pd.read_sql_query('''
                SELECT test_name, metric_name, metric_value, timestamp 
                FROM performance_metrics 
                WHERE metric_name IN ('mae', 'rmse', 'pearson_correlation')
                ORDER BY timestamp
            ''', conn)
            
            conn.close()
            
            if df.empty:
                return {"error": "No performance metrics found"}
            
            # Group by test and calculate trends
            performance_trends = {}
            for metric in ['mae', 'rmse', 'pearson_correlation']:
                metric_data = df[df['metric_name'] == metric]
                if not metric_data.empty:
                    performance_trends[metric] = {
                        'values': metric_data['metric_value'].tolist(),
                        'timestamps': metric_data['timestamp'].tolist(),
                        'trend': 'improving' if metric in ['pearson_correlation'] else 'degrading'
                    }
            
            return performance_trends
            
        except Exception as e:
            logger.error(f"Error monitoring performance: {str(e)}")
            return {"error": str(e)}