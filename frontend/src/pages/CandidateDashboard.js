import React, { useState, useEffect, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { 
  CloudArrowUpIcon, 
  DocumentTextIcon, 
  UserIcon, 
  CheckCircleIcon,
  CalendarIcon,
  EyeIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';
import apiService from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

const CandidateDashboard = () => {
  const navigate = useNavigate();
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [candidateInfo, setCandidateInfo] = useState({
    name: '',
    email: ''
  });

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    try {
      const response = await apiService.getCandidateResumes();
      setResumes(response.resumes || []);
    } catch (error) {
      toast.error('Failed to fetch resumes');
      console.error('Error fetching resumes:', error);
    } finally {
      setLoading(false);
    }
  };

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    
    // Validate file type
    const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    if (!allowedTypes.includes(file.type)) {
      toast.error('Please upload a PDF, DOC, DOCX, or TXT file');
      return;
    }

    // Validate file size (16MB max)
    if (file.size > 16 * 1024 * 1024) {
      toast.error('File size must be less than 16MB');
      return;
    }

    // Check if candidate info is provided
    if (!candidateInfo.name.trim()) {
      toast.error('Please enter your name before uploading');
      return;
    }

    setUploading(true);
    
    try {
      const formData = new FormData();
      formData.append('resume', file);
      formData.append('candidate_name', candidateInfo.name);
      formData.append('candidate_email', candidateInfo.email);

      const response = await apiService.uploadResume(formData);
      
      if (response.success) {
        toast.success('Resume uploaded successfully!');
        fetchResumes();
        // Clear candidate info after successful upload
        setCandidateInfo({ name: '', email: '' });
      }
    } catch (error) {
      toast.error(error.message || 'Failed to upload resume');
    } finally {
      setUploading(false);
    }
  }, [candidateInfo]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    multiple: false,
    disabled: uploading
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCandidateInfo(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getFileIcon = (filename) => {
    const extension = filename.split('.').pop().toLowerCase();
    switch (extension) {
      case 'pdf':
        return '📄';
      case 'doc':
      case 'docx':
        return '📝';
      case 'txt':
        return '📃';
      default:
        return '📄';
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Header Section */}
      <div className="relative bg-gradient-to-r from-green-600 to-teal-700 py-16 overflow-hidden">
        <div className="absolute inset-0">
          <img
            src="https://images.unsplash.com/photo-1586953208448-b95a79798f07?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2000&q=80"
            alt="Professional writing resume and job application documents"
            className="w-full h-full object-cover opacity-20"
          />
        </div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center text-white">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">Candidate Dashboard</h1>
            <p className="text-xl text-green-100 mb-8 max-w-3xl mx-auto">
              Upload your resume and get matched with relevant job opportunities using our AI-powered matching system
            </p>
            <div className="flex flex-wrap justify-center gap-6 text-green-100">
              <div className="flex items-center">
                <DocumentTextIcon className="h-5 w-5 mr-2" />
                <span>Smart Resume Analysis</span>
              </div>
              <div className="flex items-center">
                <CheckCircleIcon className="h-5 w-5 mr-2" />
                <span>Instant Job Matching</span>
              </div>
              <div className="flex items-center">
                <UserIcon className="h-5 w-5 mr-2" />
                <span>Profile Management</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-8 relative z-10">

        {/* Enhanced Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-gradient-to-r from-blue-500 to-blue-600 p-4 rounded-xl">
                <DocumentTextIcon className="h-8 w-8 text-white" />
              </div>
              <div className="text-right">
                <p className="text-3xl font-bold text-gray-900">{resumes.length}</p>
                <p className="text-blue-600 font-semibold">Uploaded Resumes</p>
              </div>
            </div>
            <div className="bg-blue-50 rounded-lg p-3">
              <p className="text-sm text-blue-700">Your resume portfolio ready for matching</p>
            </div>
          </div>
          
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-gradient-to-r from-green-500 to-green-600 p-4 rounded-xl">
                <CheckCircleIcon className="h-8 w-8 text-white" />
              </div>
              <div className="text-right">
                <p className="text-3xl font-bold text-gray-900">0</p>
                <p className="text-green-600 font-semibold">Job Matches</p>
              </div>
            </div>
            <div className="bg-green-50 rounded-lg p-3">
              <p className="text-sm text-green-700">AI-matched job opportunities for your profile</p>
            </div>
          </div>
          
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-gradient-to-r from-purple-500 to-purple-600 p-4 rounded-xl">
                <UserIcon className="h-8 w-8 text-white" />
              </div>
              <div className="text-right">
                <p className="text-3xl font-bold text-gray-900">Active</p>
                <p className="text-purple-600 font-semibold">Profile Status</p>
              </div>
            </div>
            <div className="bg-purple-50 rounded-lg p-3">
              <p className="text-sm text-purple-700">Your profile is ready for job matching</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Upload Your Resume</h2>
            
            {/* Candidate Information Form */}
            <div className="mb-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Your Name *
                </label>
                <input
                  type="text"
                  name="name"
                  value={candidateInfo.name}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter your full name"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address (Optional)
                </label>
                <input
                  type="email"
                  name="email"
                  value={candidateInfo.email}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                  placeholder="your.email@example.com"
                />
              </div>
            </div>

            {/* File Upload Area */}
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors duration-200 ${
                isDragActive
                  ? 'border-blue-500 bg-blue-50'
                  : uploading
                  ? 'border-gray-300 bg-gray-50 cursor-not-allowed'
                  : 'border-gray-300 hover:border-blue-500 hover:bg-blue-50'
              }`}
            >
              <input {...getInputProps()} />
              
              {uploading ? (
                <div className="flex flex-col items-center">
                  <div className="spinner mb-4" />
                  <p className="text-gray-600">Uploading and processing your resume...</p>
                </div>
              ) : (
                <div className="flex flex-col items-center">
                  <CloudArrowUpIcon className="h-12 w-12 text-gray-400 mb-4" />
                  {isDragActive ? (
                    <p className="text-blue-600 font-medium">Drop your resume here...</p>
                  ) : (
                    <div>
                      <p className="text-gray-600 mb-2">
                        Drag and drop your resume here, or <span className="text-blue-600 font-medium">click to browse</span>
                      </p>
                      <p className="text-sm text-gray-500">
                        Supports PDF, DOC, DOCX, and TXT files (max 16MB)
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Resume History */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Your Uploaded Resumes</h2>
            
            {resumes.length === 0 ? (
              <div className="text-center py-8">
                <DocumentTextIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No resumes uploaded yet</h3>
                <p className="text-gray-600">Upload your first resume to get started with job matching</p>
              </div>
            ) : (
              <div className="space-y-4">
                {resumes.map((resume) => (
                  <div key={resume.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow duration-200">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-start space-x-3">
                        <div className="text-2xl">{getFileIcon(resume.filename)}</div>
                        <div className="flex-1">
                          <h4 className="font-medium text-gray-900">{resume.filename}</h4>
                          <p className="text-gray-600 text-sm">{resume.candidate_name}</p>
                          {resume.candidate_email && (
                            <p className="text-gray-500 text-sm">{resume.candidate_email}</p>
                          )}
                          <div className="flex items-center space-x-1 text-xs text-gray-500 mt-1">
                            <CalendarIcon className="h-3 w-3" />
                            <span>Uploaded {formatDate(resume.uploaded_at)}</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <CheckCircleIcon className="h-5 w-5 text-green-500" />
                        <span className="text-sm text-green-600 font-medium">Processed</span>
                      </div>
                    </div>

                    {/* Match Summary */}
                    <div className="bg-gray-50 rounded-lg p-4 mb-4">
                      <div className="grid grid-cols-3 gap-4">
                        <div className="text-center">
                          <div className="text-lg font-semibold text-gray-900">
                            {resume.total_jobs_available || 0}
                          </div>
                          <div className="text-xs text-gray-600">Available Jobs</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-semibold text-blue-600">
                            {resume.best_match_score || 0}%
                          </div>
                          <div className="text-xs text-gray-600">Best Match</div>
                        </div>
                        <div className="text-center">
                          <ChartBarIcon className="h-6 w-6 text-gray-400 mx-auto" />
                          <div className="text-xs text-gray-600 mt-1">Ready to Match</div>
                        </div>
                      </div>
                      
                      {resume.best_match_job && (
                        <div className="mt-3 pt-3 border-t border-gray-200">
                          <p className="text-xs text-gray-600">
                            <span className="font-medium">Top Match:</span> {resume.best_match_job}
                          </p>
                        </div>
                      )}
                    </div>

                    {/* Actions */}
                    <div className="flex items-center justify-between">
                      <div className="text-sm text-gray-500">
                        {resume.total_jobs_available > 0 ? (
                          <span className="text-green-600">Ready for job matching</span>
                        ) : (
                          <span className="text-orange-600">No jobs available to match</span>
                        )}
                      </div>
                      
                      <button
                        onClick={() => navigate(`/candidate/matches/${resume.id}`)}
                        disabled={!resume.total_jobs_available || resume.total_jobs_available === 0}
                        className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                          resume.total_jobs_available > 0
                            ? 'bg-blue-600 text-white hover:bg-blue-700'
                            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        }`}
                      >
                        <EyeIcon className="h-4 w-4" />
                        <span>View Matches</span>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Tips Section */}
        <div className="mt-8 bg-blue-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-4">Tips for Better Matches</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start space-x-2">
              <CheckCircleIcon className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <p className="text-blue-800">Include specific technical skills and technologies</p>
            </div>
            <div className="flex items-start space-x-2">
              <CheckCircleIcon className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <p className="text-blue-800">Mention years of experience and level of expertise</p>
            </div>
            <div className="flex items-start space-x-2">
              <CheckCircleIcon className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <p className="text-blue-800">Use industry-standard keywords and terminology</p>
            </div>
            <div className="flex items-start space-x-2">
              <CheckCircleIcon className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <p className="text-blue-800">Keep your resume updated with latest achievements</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CandidateDashboard;
