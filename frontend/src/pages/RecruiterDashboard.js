import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { 
  PlusIcon, 
  BriefcaseIcon, 
  UserGroupIcon, 
  ChartBarIcon,
  EyeIcon,
  CalendarIcon
} from '@heroicons/react/24/outline';
import apiService from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

const RecruiterDashboard = () => {
  const [jobDescriptions, setJobDescriptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    description: '',
    requirements: '',
    recruiter_name: ''
  });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchJobDescriptions();
  }, []);

  const fetchJobDescriptions = async () => {
    try {
      const response = await apiService.getJobDescriptions();
      setJobDescriptions(response.job_descriptions || []);
    } catch (error) {
      toast.error('Failed to fetch job descriptions');
      console.error('Error fetching job descriptions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.title.trim() || !formData.description.trim()) {
      toast.error('Please fill in the required fields');
      return;
    }

    setSubmitting(true);
    try {
      const response = await apiService.createJobDescription(formData);
      
      if (response.success) {
        toast.success('Job description created successfully!');
        setFormData({
          title: '',
          company: '',
          description: '',
          requirements: '',
          recruiter_name: ''
        });
        setShowCreateForm(false);
        fetchJobDescriptions();
      }
    } catch (error) {
      toast.error(error.message || 'Failed to create job description');
    } finally {
      setSubmitting(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Header Section - Enhanced Responsive Design */}
      <div className="relative bg-gradient-to-r from-blue-600 to-indigo-700 py-8 sm:py-12 lg:py-16 overflow-hidden">
        <div className="absolute inset-0">
          <img
            src="https://images.unsplash.com/photo-1521737604893-d14cc237f11d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2000&q=80"
            alt="HR team reviewing resumes and candidate profiles"
            className="w-full h-full object-cover opacity-20"
          />
        </div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-6 lg:space-y-0">
            <div className="text-white flex-1">
              <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold mb-3 sm:mb-4">
                Recruiter Dashboard
              </h1>
              <p className="text-base sm:text-lg lg:text-xl text-blue-100 mb-4 sm:mb-6 max-w-2xl">
                Manage job descriptions and find the best candidates with AI-powered matching
              </p>
              
              {/* Feature badges - Responsive layout */}
              <div className="flex flex-col sm:flex-row sm:flex-wrap lg:flex-nowrap items-start sm:items-center space-y-2 sm:space-y-0 sm:space-x-4 lg:space-x-6 text-blue-100 text-sm sm:text-base">
                <div className="flex items-center">
                  <BriefcaseIcon className="h-4 w-4 sm:h-5 sm:w-5 mr-2 flex-shrink-0" />
                  <span className="whitespace-nowrap">Smart Job Posting</span>
                </div>
                <div className="flex items-center">
                  <UserGroupIcon className="h-4 w-4 sm:h-5 sm:w-5 mr-2 flex-shrink-0" />
                  <span className="whitespace-nowrap">AI Candidate Matching</span>
                </div>
                <div className="flex items-center">
                  <ChartBarIcon className="h-4 w-4 sm:h-5 sm:w-5 mr-2 flex-shrink-0" />
                  <span className="whitespace-nowrap">Analytics Dashboard</span>
                </div>
              </div>
            </div>
            
            {/* CTA Button - Responsive positioning and sizing */}
            <div className="flex-shrink-0">
              <button
                onClick={() => setShowCreateForm(true)}
                className="w-full sm:w-auto bg-yellow-400 text-gray-900 px-4 sm:px-6 lg:px-8 py-3 sm:py-4 rounded-xl font-semibold hover:bg-yellow-300 transition-all duration-300 flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl transform hover:scale-105 text-sm sm:text-base"
              >
                <PlusIcon className="h-5 w-5 sm:h-6 sm:w-6 flex-shrink-0" />
                <span className="whitespace-nowrap">New Job Posting</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-8 relative z-10">

        {/* Enhanced Stats Cards - Responsive Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mb-8 sm:mb-12">
          <div className="bg-white rounded-2xl shadow-xl p-4 sm:p-6 lg:p-8 border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
            <div className="flex items-center justify-between mb-3 sm:mb-4">
              <div className="bg-gradient-to-r from-blue-500 to-blue-600 p-3 sm:p-4 rounded-xl">
                <BriefcaseIcon className="h-6 w-6 sm:h-7 sm:w-7 lg:h-8 lg:w-8 text-white" />
              </div>
              <div className="text-right">
                <p className="text-2xl sm:text-3xl font-bold text-gray-900">{jobDescriptions.length}</p>
                <p className="text-blue-600 font-semibold text-sm sm:text-base">Active Job Postings</p>
              </div>
            </div>
            <div className="bg-blue-50 rounded-lg p-2 sm:p-3">
              <p className="text-xs sm:text-sm text-blue-700">Manage and track all your job postings in one place</p>
            </div>
          </div>
          
          <div className="bg-white rounded-2xl shadow-xl p-4 sm:p-6 lg:p-8 border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
            <div className="flex items-center justify-between mb-3 sm:mb-4">
              <div className="bg-gradient-to-r from-green-500 to-green-600 p-3 sm:p-4 rounded-xl">
                <UserGroupIcon className="h-6 w-6 sm:h-7 sm:w-7 lg:h-8 lg:w-8 text-white" />
              </div>
              <div className="text-right">
                <p className="text-2xl sm:text-3xl font-bold text-gray-900">0</p>
                <p className="text-green-600 font-semibold text-sm sm:text-base">Total Matches</p>
              </div>
            </div>
            <div className="bg-green-50 rounded-lg p-2 sm:p-3">
              <p className="text-xs sm:text-sm text-green-700">AI-powered candidates matched to your job postings</p>
            </div>
          </div>
          
          <div className="bg-white rounded-2xl shadow-xl p-4 sm:p-6 lg:p-8 border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 sm:col-span-2 lg:col-span-1">
            <div className="flex items-center justify-between mb-3 sm:mb-4">
              <div className="bg-gradient-to-r from-purple-500 to-purple-600 p-3 sm:p-4 rounded-xl">
                <ChartBarIcon className="h-6 w-6 sm:h-7 sm:w-7 lg:h-8 lg:w-8 text-white" />
              </div>
              <div className="text-right">
                <p className="text-2xl sm:text-3xl font-bold text-gray-900">95%</p>
                <p className="text-purple-600 font-semibold text-sm sm:text-base">Match Accuracy</p>
              </div>
            </div>
            <div className="bg-purple-50 rounded-lg p-2 sm:p-3">
              <p className="text-xs sm:text-sm text-purple-700">Advanced NLP algorithms ensure precise matching</p>
            </div>
          </div>
        </div>

        {/* Job Descriptions List - Responsive Design */}
        <div className="bg-white rounded-lg shadow-md">
          <div className="px-4 sm:px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg sm:text-xl font-semibold text-gray-900">Your Job Postings</h2>
          </div>
          
          {jobDescriptions.length === 0 ? (
            <div className="text-center py-8 sm:py-12 px-4">
              <BriefcaseIcon className="h-10 w-10 sm:h-12 sm:w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-base sm:text-lg font-medium text-gray-900 mb-2">No job postings yet</h3>
              <p className="text-gray-600 text-sm sm:text-base">Create your first job posting to start finding candidates</p>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {jobDescriptions.map((job) => (
                <div key={job.id} className="p-4 sm:p-6 hover:bg-gray-50 transition-colors duration-200">
                  <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
                    <div className="flex-1 min-w-0">
                      <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-1 truncate">{job.title}</h3>
                      {job.company && (
                        <p className="text-gray-600 mb-2 text-sm sm:text-base">{job.company}</p>
                      )}
                      <p className="text-gray-700 mb-3 line-clamp-2 text-sm sm:text-base">
                        {job.description.substring(0, 150)}...
                      </p>
                      <div className="flex flex-col sm:flex-row sm:items-center sm:space-x-4 space-y-2 sm:space-y-0 text-xs sm:text-sm text-gray-500">
                        <div className="flex items-center space-x-1">
                          <CalendarIcon className="h-3 w-3 sm:h-4 sm:w-4 flex-shrink-0" />
                          <span>Created {formatDate(job.created_at)}</span>
                        </div>
                        {job.created_by && (
                          <span className="hidden sm:inline">by {job.created_by}</span>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center justify-end lg:justify-start space-x-3 lg:ml-6">
                      <Link
                        to={`/matches/${job.id}`}
                        className="bg-blue-600 text-white px-3 sm:px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200 flex items-center space-x-2 text-sm sm:text-base"
                      >
                        <EyeIcon className="h-3 w-3 sm:h-4 sm:w-4 flex-shrink-0" />
                        <span className="whitespace-nowrap">View Matches</span>
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Create Job Form Modal - Responsive Design */}
        {showCreateForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-4 sm:p-6">
                <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4 sm:mb-6">Create New Job Posting</h2>
                
                <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Job Title *
                    </label>
                    <input
                      type="text"
                      name="title"
                      value={formData.title}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 text-sm sm:text-base border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                      placeholder="e.g., Senior Software Engineer"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Company Name
                    </label>
                    <input
                      type="text"
                      name="company"
                      value={formData.company}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 text-sm sm:text-base border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                      placeholder="e.g., TechCorp Inc."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Recruiter Name
                    </label>
                    <input
                      type="text"
                      name="recruiter_name"
                      value={formData.recruiter_name}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 text-sm sm:text-base border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Your name"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Job Description *
                    </label>
                    <textarea
                      name="description"
                      value={formData.description}
                      onChange={handleInputChange}
                      rows={5}
                      className="w-full px-3 py-2 text-sm sm:text-base border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 resize-none"
                      placeholder="Describe the role, responsibilities, and what you're looking for..."
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Requirements
                    </label>
                    <textarea
                      name="requirements"
                      value={formData.requirements}
                      onChange={handleInputChange}
                      rows={3}
                      className="w-full px-3 py-2 text-sm sm:text-base border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 resize-none"
                      placeholder="List specific skills, experience, and qualifications..."
                    />
                  </div>

                  <div className="flex flex-col sm:flex-row justify-end space-y-3 sm:space-y-0 sm:space-x-3 pt-4">
                    <button
                      type="button"
                      onClick={() => setShowCreateForm(false)}
                      className="w-full sm:w-auto px-4 sm:px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors duration-200 text-sm sm:text-base"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      disabled={submitting}
                      className="w-full sm:w-auto px-4 sm:px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 text-sm sm:text-base"
                    >
                      {submitting && <div className="spinner" />}
                      <span>{submitting ? 'Creating...' : 'Create Job Posting'}</span>
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecruiterDashboard;
