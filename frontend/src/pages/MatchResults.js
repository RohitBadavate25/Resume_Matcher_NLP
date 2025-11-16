import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { 
  ArrowLeftIcon,
  UserGroupIcon,
  ChartBarIcon,
  TrophyIcon,
  DocumentTextIcon,
  CalendarIcon,
  EnvelopeIcon,
  StarIcon
} from '@heroicons/react/24/outline';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import apiService from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

const MatchResults = () => {
  const { jobId } = useParams();
  const [matches, setMatches] = useState([]);
  const [jobInfo, setJobInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  
  // Enhanced feedback functionality
  const [feedbackModal, setFeedbackModal] = useState({ isOpen: false, match: null });
  const [feedback, setFeedback] = useState({
    humanScore: 5,
    recruiterFeedback: '',
    matchQuality: 'good'
  });

  useEffect(() => {
    if (jobId) {
      fetchJobInfo();
      performMatching();
    }
  }, [jobId]);

  const fetchJobInfo = async () => {
    try {
      const response = await apiService.getJobDescriptions();
      const job = response.job_descriptions.find(j => j.id === jobId);
      setJobInfo(job);
    } catch (error) {
      toast.error('Failed to fetch job information');
      console.error('Error fetching job info:', error);
    }
  };

  const performMatching = async () => {
    setAnalyzing(true);
    try {
      const response = await apiService.matchResumes(jobId);
      if (response.success) {
        setMatches(response.matches || []);
        toast.success(`Found ${response.total_candidates} candidates to analyze`);
      }
    } catch (error) {
      toast.error(error.message || 'Failed to perform matching');
      console.error('Error performing matching:', error);
    } finally {
      setLoading(false);
      setAnalyzing(false);
    }
  };

  const getMatchColor = (percentage) => {
    if (percentage >= 80) return 'text-green-600 bg-green-100';
    if (percentage >= 60) return 'text-yellow-600 bg-yellow-100';
    if (percentage >= 40) return 'text-orange-600 bg-orange-100';
    return 'text-red-600 bg-red-100';
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 70) return 'text-green-700 bg-green-50 border border-green-200';
    if (confidence >= 50) return 'text-yellow-700 bg-yellow-50 border border-yellow-200';
    return 'text-red-700 bg-red-50 border border-red-200';
  };

  const getMatchGrade = (percentage) => {
    if (percentage >= 90) return 'A+';
    if (percentage >= 80) return 'A';
    if (percentage >= 70) return 'B+';
    if (percentage >= 60) return 'B';
    if (percentage >= 50) return 'C+';
    if (percentage >= 40) return 'C';
    return 'D';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  // Enhanced helper functions for new NLP features
  const getMatchCategoryColor = (category) => {
    switch (category) {
      case 'excellent': return 'bg-green-100 text-green-800 border border-green-300';
      case 'good': return 'bg-blue-100 text-blue-800 border border-blue-300';
      case 'fair': return 'bg-yellow-100 text-yellow-800 border border-yellow-300';
      case 'poor': return 'bg-orange-100 text-orange-800 border border-orange-300';
      case 'very_poor': return 'bg-red-100 text-red-800 border border-red-300';
      default: return 'bg-gray-100 text-gray-800 border border-gray-300';
    }
  };

  const getMatchCategoryLabel = (category) => {
    switch (category) {
      case 'excellent': return '🌟 Excellent Match';
      case 'good': return '✅ Good Match';
      case 'fair': return '⚡ Fair Match';
      case 'poor': return '⚠️ Poor Match';
      case 'very_poor': return '❌ Very Poor Match';
      default: return '❓ Unknown';
    }
  };

  const getExperienceColor = (status) => {
    switch (status) {
      case 'meets_requirement': return 'bg-green-100 text-green-800';
      case 'close_match': return 'bg-yellow-100 text-yellow-800';
      case 'below_requirement': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getExperienceLabel = (status) => {
    switch (status) {
      case 'meets_requirement': return '✅ Meets Requirements';
      case 'close_match': return '⚡ Close Match';
      case 'below_requirement': return '⚠️ Below Requirements';
      default: return '❓ Unknown';
    }
  };

  const getRecommendationColor = (priority) => {
    switch (priority) {
      case 'high': return 'bg-red-50 text-red-700 border-l-4 border-red-400';
      case 'medium': return 'bg-yellow-50 text-yellow-700 border-l-4 border-yellow-400';
      case 'positive': return 'bg-green-50 text-green-700 border-l-4 border-green-400';
      default: return 'bg-gray-50 text-gray-700 border-l-4 border-gray-400';
    }
  };

  // Enhanced feedback functionality
  const openFeedbackModal = (match) => {
    setFeedbackModal({ isOpen: true, match });
    setFeedback({
      humanScore: Math.round(match.match_percentage / 10), // Convert to 1-10 scale
      recruiterFeedback: '',
      matchQuality: match.match_category || 'good'
    });
  };

  const closeFeedbackModal = () => {
    setFeedbackModal({ isOpen: false, match: null });
    setFeedback({ humanScore: 5, recruiterFeedback: '', matchQuality: 'good' });
  };

  const submitFeedback = async () => {
    try {
      const response = await apiService.submitFeedback({
        job_id: jobId,
        resume_id: feedbackModal.match.resume_id,
        human_score: feedback.humanScore / 10, // Convert back to 0-1 scale
        recruiter_feedback: feedback.recruiterFeedback,
        match_quality: feedback.matchQuality
      });

      if (response.success) {
        toast.success('Feedback submitted successfully! This helps improve our AI.');
        closeFeedbackModal();
      }
    } catch (error) {
      toast.error('Failed to submit feedback');
      console.error('Error submitting feedback:', error);
    }
  };

  // Prepare chart data
  const chartData = matches.slice(0, 10).map((match, index) => ({
    name: match.candidate_name.split(' ')[0] || `Candidate ${index + 1}`,
    score: match.match_percentage,
    fullName: match.candidate_name
  }));

  const distributionData = [
    { name: 'Excellent (80-100%)', value: matches.filter(m => m.match_percentage >= 80).length, fill: '#10b981' },
    { name: 'Good (60-79%)', value: matches.filter(m => m.match_percentage >= 60 && m.match_percentage < 80).length, fill: '#f59e0b' },
    { name: 'Fair (40-59%)', value: matches.filter(m => m.match_percentage >= 40 && m.match_percentage < 60).length, fill: '#f97316' },
    { name: 'Poor (0-39%)', value: matches.filter(m => m.match_percentage < 40).length, fill: '#ef4444' }
  ].filter(item => item.value > 0);

  if (loading) {
    return <LoadingSpinner message="Analyzing resumes and calculating matches..." />;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-4 mb-4">
            <Link
              to="/recruiter"
              className="flex items-center space-x-2 text-blue-600 hover:text-blue-800 transition-colors duration-200"
            >
              <ArrowLeftIcon className="h-5 w-5" />
              <span>Back to Dashboard</span>
            </Link>
          </div>
          
          {jobInfo && (
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">{jobInfo.title}</h1>
              {jobInfo.company && (
                <p className="text-gray-600 mb-2">{jobInfo.company}</p>
              )}
              <p className="text-gray-700 mb-4">{jobInfo.description.substring(0, 200)}...</p>
              <div className="flex items-center space-x-4 text-sm text-gray-500">
                <div className="flex items-center space-x-1">
                  <CalendarIcon className="h-4 w-4" />
                  <span>Posted {formatDate(jobInfo.created_at)}</span>
                </div>
                {jobInfo.created_by && (
                  <span>by {jobInfo.created_by}</span>
                )}
              </div>
            </div>
          )}
        </div>

        {analyzing && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div className="flex items-center space-x-2">
              <div className="spinner" />
              <span className="text-blue-800 font-medium">Analyzing candidates...</span>
            </div>
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="bg-blue-100 p-3 rounded-full">
                <UserGroupIcon className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">{matches.length}</p>
                <p className="text-gray-600">Total Candidates</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="bg-green-100 p-3 rounded-full">
                <TrophyIcon className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">
                  {matches.filter(m => m.match_percentage >= 80).length}
                </p>
                <p className="text-gray-600">Excellent Matches</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="bg-yellow-100 p-3 rounded-full">
                <ChartBarIcon className="h-6 w-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">
                  {matches.length > 0 ? Math.round(matches.reduce((sum, m) => sum + m.match_percentage, 0) / matches.length) : 0}%
                </p>
                <p className="text-gray-600">Average Match</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="bg-purple-100 p-3 rounded-full">
                <StarIcon className="h-6 w-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">
                  {matches.length > 0 ? Math.round(Math.max(...matches.map(m => m.match_percentage))) : 0}%
                </p>
                <p className="text-gray-600">Best Match</p>
              </div>
            </div>
          </div>
        </div>

        {matches.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <UserGroupIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No Candidates Found</h3>
            <p className="text-gray-600 mb-6">
              There are no uploaded resumes to match against this job description yet.
            </p>
            <Link
              to="/candidate"
              className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
            >
              <DocumentTextIcon className="h-5 w-5 mr-2" />
              Upload Resume as Candidate
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Candidate Rankings */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-lg shadow-md">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-xl font-semibold text-gray-900">Candidate Rankings</h2>
                </div>
                
                <div className="divide-y divide-gray-200">
                  {matches.map((match, index) => (
                    <div key={match.resume_id} className="p-6 hover:bg-gray-50 transition-colors duration-200">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-4">
                          <div className="flex items-center justify-center w-10 h-10 bg-gray-100 rounded-full font-bold text-gray-700">
                            #{index + 1}
                          </div>
                          <div>
                            <h3 className="text-lg font-semibold text-gray-900">{match.candidate_name}</h3>
                            {match.candidate_email && (
                              <div className="flex items-center space-x-1 text-gray-600">
                                <EnvelopeIcon className="h-4 w-4" />
                                <span className="text-sm">{match.candidate_email}</span>
                              </div>
                            )}
                            {/* Enhanced Match Category Badge */}
                            {match.match_category && (
                              <div className="mt-1">
                                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getMatchCategoryColor(match.match_category)}`}>
                                  {getMatchCategoryLabel(match.match_category)}
                                </span>
                              </div>
                            )}
                          </div>
                        </div>
                        
                        <div className="text-right">
                          <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getMatchColor(match.match_percentage)}`}>
                            {match.match_percentage}% Match
                          </div>
                          <div className="text-sm text-gray-500 mt-1">
                            Grade: {getMatchGrade(match.match_percentage)}
                          </div>
                          {/* Confidence Score */}
                          {match.confidence_percentage && (
                            <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs mt-2 ${getConfidenceColor(match.confidence_percentage)}`}>
                              🎯 {match.confidence_percentage}% Confident
                            </div>
                          )}
                        </div>
                      </div>
                      
                      {/* Enhanced Progress Bar with Component Breakdown */}
                      <div className="w-full bg-gray-200 rounded-full h-3 mb-3 overflow-hidden">
                        <div className="flex h-full">
                          {match.component_scores && (
                            <>
                              <div 
                                className="bg-blue-600 transition-all duration-500"
                                style={{ width: `${(match.component_scores.tfidf_similarity || 0) * 35}%` }}
                                title={`Content Match: ${((match.component_scores.tfidf_similarity || 0) * 100).toFixed(1)}%`}
                              />
                              <div 
                                className="bg-green-500 transition-all duration-500"
                                style={{ width: `${(match.component_scores.skill_similarity || 0) * 25}%` }}
                                title={`Skills Match: ${((match.component_scores.skill_similarity || 0) * 100).toFixed(1)}%`}
                              />
                              <div 
                                className="bg-purple-500 transition-all duration-500"
                                style={{ width: `${(match.component_scores.semantic_similarity || 0) * 20}%` }}
                                title={`Semantic Match: ${((match.component_scores.semantic_similarity || 0) * 100).toFixed(1)}%`}
                              />
                              <div 
                                className="bg-yellow-500 transition-all duration-500"
                                style={{ width: `${(match.component_scores.keyword_similarity || 0) * 15}%` }}
                                title={`Keywords Match: ${((match.component_scores.keyword_similarity || 0) * 100).toFixed(1)}%`}
                              />
                              <div 
                                className="bg-orange-500 transition-all duration-500"
                                style={{ width: `${(match.component_scores.context_similarity || 0) * 5}%` }}
                                title={`Context Match: ${((match.component_scores.context_similarity || 0) * 100).toFixed(1)}%`}
                              />
                            </>
                          )}
                          {!match.component_scores && (
                            <div
                              className="bg-blue-600 h-full transition-all duration-500"
                              style={{ width: `${match.match_percentage}%` }}
                            />
                          )}
                        </div>
                      </div>

                      {/* Enhanced Skills Analysis */}
                      {match.skills_analysis && (
                        <div className="mb-3 bg-gray-50 rounded-lg p-3">
                          <div className="grid grid-cols-2 gap-4 text-sm">
                            <div>
                              <span className="font-medium text-gray-700">Skills Matched:</span>
                              <span className="ml-2 text-green-600 font-semibold">
                                {match.skills_analysis.matched_skills?.length || 0}
                              </span>
                            </div>
                            <div>
                              <span className="font-medium text-gray-700">Skills Missing:</span>
                              <span className="ml-2 text-red-600 font-semibold">
                                {match.skills_analysis.missing_skills?.length || 0}
                              </span>
                            </div>
                          </div>
                          
                          {/* High Priority Skills */}
                          {match.skills_analysis.high_priority_matched?.length > 0 && (
                            <div className="mt-2">
                              <span className="text-xs text-gray-600">Key Skills Matched: </span>
                              <span className="text-xs text-green-700 font-medium">
                                {match.skills_analysis.high_priority_matched.slice(0, 3).join(', ')}
                                {match.skills_analysis.high_priority_matched.length > 3 && '...'}
                              </span>
                            </div>
                          )}
                          
                          {match.skills_analysis.high_priority_missing?.length > 0 && (
                            <div className="mt-1">
                              <span className="text-xs text-gray-600">Critical Missing: </span>
                              <span className="text-xs text-red-700 font-medium">
                                {match.skills_analysis.high_priority_missing.slice(0, 3).join(', ')}
                                {match.skills_analysis.high_priority_missing.length > 3 && '...'}
                              </span>
                            </div>
                          )}
                        </div>
                      )}

                      {/* Experience Analysis */}
                      {match.experience_analysis && match.experience_analysis.status !== 'unknown' && (
                        <div className="mb-3">
                          <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs ${getExperienceColor(match.experience_analysis.status)}`}>
                            Experience: {getExperienceLabel(match.experience_analysis.status)}
                            {match.experience_analysis.job_years && match.experience_analysis.resume_years && (
                              <span className="ml-1">
                                ({match.experience_analysis.resume_years}/{match.experience_analysis.job_years} years)
                              </span>
                            )}
                          </div>
                        </div>
                      )}

                      {/* Recommendations */}
                      {match.recommendations && match.recommendations.length > 0 && (
                        <div className="mb-3">
                          {match.recommendations.slice(0, 2).map((rec, recIndex) => (
                            <div key={recIndex} className={`text-xs mt-1 p-2 rounded ${getRecommendationColor(rec.priority)}`}>
                              {rec.message}
                            </div>
                          ))}
                        </div>
                      )}
                      
                      <div className="flex items-center justify-between text-sm text-gray-500">
                        <span>📄 {match.filename}</span>
                        <div className="flex items-center space-x-2">
                          <span>Uploaded {formatDate(match.uploaded_at)}</span>
                          {/* Enhanced Feedback Button */}
                          <button
                            onClick={() => openFeedbackModal(match)}
                            className="ml-2 px-2 py-1 text-xs bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-md transition-colors duration-200 flex items-center space-x-1"
                            title="Provide feedback to improve AI accuracy"
                          >
                            <span>💬</span>
                            <span>Feedback</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Analytics Sidebar */}
            <div className="space-y-6">
              {/* Match Distribution Chart */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Match Distribution</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={distributionData}
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        dataKey="value"
                        label={({ name, value }) => `${value}`}
                      >
                        {distributionData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.fill} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                <div className="mt-4 space-y-2">
                  {distributionData.map((item, index) => (
                    <div key={index} className="flex items-center space-x-2 text-sm">
                      <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.fill }} />
                      <span className="text-gray-700">{item.name}: {item.value}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Top Matches Chart */}
              {chartData.length > 0 && (
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Top 10 Matches</h3>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={chartData} layout="horizontal">
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis type="number" domain={[0, 100]} />
                        <YAxis dataKey="name" type="category" width={60} />
                        <Tooltip
                          formatter={(value, name, props) => [
                            `${value}%`,
                            props.payload.fullName
                          ]}
                        />
                        <Bar dataKey="score" fill="#3b82f6" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              )}

              {/* Enhanced Matching Legend */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">🧠 AI Matching Components</h3>
                <div className="space-y-3 text-sm">
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-2 bg-blue-600 rounded"></div>
                    <span className="text-gray-700">Content Similarity (35%)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-2 bg-green-500 rounded"></div>
                    <span className="text-gray-700">Skills Matching (25%)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-2 bg-purple-500 rounded"></div>
                    <span className="text-gray-700">Semantic Analysis (20%)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-2 bg-yellow-500 rounded"></div>
                    <span className="text-gray-700">Keywords Match (15%)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-2 bg-orange-500 rounded"></div>
                    <span className="text-gray-700">Context Analysis (5%)</span>
                  </div>
                </div>
                <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                  <p className="text-xs text-blue-700">
                    💡 Our enhanced AI analyzes multiple factors to provide more accurate matching than traditional keyword-based systems.
                  </p>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
                <div className="space-y-3">
                  <button
                    onClick={performMatching}
                    disabled={analyzing}
                    className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50"
                  >
                    {analyzing ? 'Refreshing...' : 'Refresh Matches'}
                  </button>
                  <Link
                    to="/recruiter"
                    className="block w-full bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors duration-200 text-center"
                  >
                    Back to Dashboard
                  </Link>
                </div>
              </div>
            </div>
          </div>
        )}
        
        {/* Enhanced Feedback Modal */}
        {feedbackModal.isOpen && feedbackModal.match && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">
                  Provide Feedback
                </h3>
                <button
                  onClick={closeFeedbackModal}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
              
              <div className="mb-4">
                <p className="text-sm text-gray-600 mb-2">
                  Help us improve our AI by providing feedback for:
                </p>
                <p className="font-medium text-gray-900">
                  {feedbackModal.match.candidate_name}
                </p>
                <p className="text-sm text-gray-500">
                  Current AI Score: {feedbackModal.match.match_percentage}% 
                  {feedbackModal.match.confidence_percentage && (
                    <span className="ml-2">
                      (Confidence: {feedbackModal.match.confidence_percentage}%)
                    </span>
                  )}
                </p>
              </div>

              <div className="space-y-4">
                {/* Human Score */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Your Assessment (1-10 scale):
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={feedback.humanScore}
                    onChange={(e) => setFeedback(prev => ({
                      ...prev,
                      humanScore: parseInt(e.target.value)
                    }))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Poor (1)</span>
                    <span className="font-medium">
                      Current: {feedback.humanScore}/10
                    </span>
                    <span>Excellent (10)</span>
                  </div>
                </div>

                {/* Match Quality */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Overall Match Quality:
                  </label>
                  <select
                    value={feedback.matchQuality}
                    onChange={(e) => setFeedback(prev => ({
                      ...prev,
                      matchQuality: e.target.value
                    }))}
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="excellent">Excellent Match</option>
                    <option value="good">Good Match</option>
                    <option value="fair">Fair Match</option>
                    <option value="poor">Poor Match</option>
                  </select>
                </div>

                {/* Recruiter Feedback */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Comments (optional):
                  </label>
                  <textarea
                    value={feedback.recruiterFeedback}
                    onChange={(e) => setFeedback(prev => ({
                      ...prev,
                      recruiterFeedback: e.target.value
                    }))}
                    placeholder="What makes this a good/poor match? Any specific skills or experience factors..."
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                  />
                </div>
              </div>

              <div className="flex space-x-3 mt-6">
                <button
                  onClick={closeFeedbackModal}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors duration-200"
                >
                  Cancel
                </button>
                <button
                  onClick={submitFeedback}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors duration-200"
                >
                  Submit Feedback
                </button>
              </div>
              
              <div className="mt-3 text-xs text-gray-500 text-center">
                Your feedback helps train our AI to provide better matches
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MatchResults;
