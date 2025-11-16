import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('Response error:', error);
    
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.error || error.response.data?.message || 'Server error';
      throw new Error(message);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('No response from server. Please check your connection.');
    } else {
      // Something else happened
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
);

export const apiService = {
  // Health check
  async healthCheck() {
    const response = await api.get('/api/health');
    return response.data;
  },

  // Job Description APIs
  async createJobDescription(jobData) {
    const response = await api.post('/api/job-description', jobData);
    return response.data;
  },

  async getJobDescriptions() {
    const response = await api.get('/api/job-descriptions');
    return response.data;
  },

  // Resume APIs
  async uploadResume(formData) {
    const response = await api.post('/api/resume', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async getResumes() {
    const response = await api.get('/api/resumes');
    return response.data;
  },

  async getResumeDetails(resumeId) {
    const response = await api.get(`/api/resume/${resumeId}`);
    return response.data;
  },

  // Matching APIs
  async matchResumes(jobId) {
    const response = await api.post('/api/match', { job_id: jobId });
    return response.data;
  },

  async getMatches() {
    const response = await api.get('/api/matches');
    return response.data;
  },

  // Candidate matching APIs
  async findMatchingJobs(resumeId) {
    const response = await api.get(`/api/candidate/matches/${resumeId}`);
    return response.data;
  },

  async getCandidateResumes() {
    const response = await api.get('/api/candidate/resumes');
    return response.data;
  },

  // Enhanced feedback and validation APIs
  async submitFeedback(feedbackData) {
    const response = await api.post('/api/feedback', feedbackData);
    return response.data;
  },

  async getValidationMetrics() {
    const response = await api.get('/api/validation/metrics');
    return response.data;
  },

  async runValidationTest(testData = {}) {
    const response = await api.post('/api/validation/run-test', testData);
    return response.data;
  },

  async getValidationReport(testName = null) {
    const params = testName ? { test_name: testName } : {};
    const response = await api.get('/api/validation/report', { params });
    return response.data;
  },

  async getSystemStatus() {
    const response = await api.get('/api/system/status');
    return response.data;
  },
};

export default apiService;
