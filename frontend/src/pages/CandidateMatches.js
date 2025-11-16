import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { 
  ArrowLeftIcon,
  BriefcaseIcon,
  BuildingOfficeIcon,
  CalendarIcon,
  ChartBarIcon,
  CheckCircleIcon,
  XCircleIcon,
  StarIcon
} from '@heroicons/react/24/outline';
import apiService from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

const CandidateMatches = () => {
  const { resumeId } = useParams();
  const navigate = useNavigate();
  const [matchData, setMatchData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (resumeId) {
      fetchMatchingJobs();
    }
  }, [resumeId]);

  const fetchMatchingJobs = async () => {
    try {
      setLoading(true);
      const response = await apiService.findMatchingJobs(resumeId);
      setMatchData(response);
    } catch (error) {
      toast.error('Failed to fetch job matches');
      console.error('Error fetching matches:', error);
    } finally {
      setLoading(false);
    }
  };

  const getMatchColor = (category) => {
    switch (category?.toLowerCase()) {
      case 'excellent': return 'text-green-700 bg-green-100';
      case 'good': return 'text-blue-700 bg-blue-100';
      case 'fair': return 'text-yellow-700 bg-yellow-100';
      case 'poor': return 'text-orange-700 bg-orange-100';
      case 'very_poor': return 'text-red-700 bg-red-100';
      default: return 'text-gray-700 bg-gray-100';
    }
  };

  const getMatchIcon = (percentage) => {
    if (percentage >= 80) return <StarIcon className="h-5 w-5 text-yellow-500" />;
    if (percentage >= 60) return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
    if (percentage >= 40) return <ChartBarIcon className="h-5 w-5 text-blue-500" />;
    return <XCircleIcon className="h-5 w-5 text-red-500" />;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  if (!matchData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900">No match data found</h2>
          <button
            onClick={() => navigate('/candidate')}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/candidate')}
            className="flex items-center text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeftIcon className="h-5 w-5 mr-2" />
            Back to Dashboard
          </button>
          
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Job Matches</h1>
              <p className="text-gray-600 mt-2">
                Found {matchData.total_jobs} job opportunities for {matchData.candidate_name}
              </p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500">Resume ID</div>
              <div className="text-lg font-mono text-gray-900">{matchData.resume_id.substring(0, 8)}...</div>
            </div>
          </div>
        </div>

        {/* Match Summary */}
        <div className="bg-white rounded-lg shadow mb-8 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Match Summary</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">{matchData.total_jobs}</div>
              <div className="text-sm text-gray-600">Total Jobs</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {matchData.matching_jobs.filter(job => job.match_percentage >= 50).length}
              </div>
              <div className="text-sm text-gray-600">Good Matches (≥50%)</div>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {matchData.matching_jobs.filter(job => job.match_percentage >= 30 && job.match_percentage < 50).length}
              </div>
              <div className="text-sm text-gray-600">Fair Matches (30-49%)</div>
            </div>
            <div className="text-center p-4 bg-yellow-50 rounded-lg">
              <div className="text-2xl font-bold text-yellow-600">
                {matchData.matching_jobs.length > 0 ? Math.round(matchData.matching_jobs[0].match_percentage) : 0}%
              </div>
              <div className="text-sm text-gray-600">Best Match</div>
            </div>
          </div>
        </div>

        {/* Job Matches List */}
        <div className="space-y-6">
          {matchData.matching_jobs.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-lg shadow">
              <BriefcaseIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No job matches found</h3>
              <p className="text-gray-600">There are no job postings available at the moment.</p>
            </div>
          ) : (
            matchData.matching_jobs.map((job, index) => (
              <div key={job.job_id} className="bg-white rounded-lg shadow hover:shadow-md transition-shadow duration-200 p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-start space-x-4">
                    <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg">
                      <BriefcaseIcon className="h-6 w-6 text-blue-600" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-xl font-semibold text-gray-900">{job.title}</h3>
                        <span className="text-lg font-mono text-gray-600">#{index + 1}</span>
                      </div>
                      <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                        <div className="flex items-center space-x-1">
                          <BuildingOfficeIcon className="h-4 w-4" />
                          <span>{job.company}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <CalendarIcon className="h-4 w-4" />
                          <span>Posted {formatDate(job.created_at)}</span>
                        </div>
                      </div>
                      <p className="text-gray-700 text-sm leading-relaxed">
                        {job.description_preview}
                      </p>
                    </div>
                  </div>
                  
                  {/* Match Score */}
                  <div className="text-right">
                    <div className="flex items-center space-x-2 mb-2">
                      {getMatchIcon(job.match_percentage)}
                      <span className="text-2xl font-bold text-gray-900">{job.match_percentage}%</span>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getMatchColor(job.match_category)}`}>
                      {job.match_category?.replace('_', ' ').toUpperCase() || 'UNKNOWN'}
                    </span>
                  </div>
                </div>

                {/* Component Scores */}
                {job.component_scores && (
                  <div className="mb-4 p-4 bg-gray-50 rounded-lg">
                    <h4 className="text-sm font-medium text-gray-900 mb-3">Match Components</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      {Object.entries(job.component_scores).map(([component, score]) => (
                        <div key={component} className="text-center">
                          <div className="text-lg font-semibold text-gray-900">
                            {Math.round(score * 100)}%
                          </div>
                          <div className="text-xs text-gray-600 capitalize">
                            {component.replace('_', ' ').replace('similarity', '')}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Skills Analysis */}
                {job.skills_analysis && (job.skills_analysis.matched_skills?.length > 0 || job.skills_analysis.missing_skills?.length > 0) && (
                  <div className="border-t pt-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {job.skills_analysis.matched_skills?.length > 0 && (
                        <div>
                          <h4 className="text-sm font-medium text-green-700 mb-2 flex items-center">
                            <CheckCircleIcon className="h-4 w-4 mr-1" />
                            Matched Skills ({job.skills_analysis.matched_skills.length})
                          </h4>
                          <div className="flex flex-wrap gap-1">
                            {job.skills_analysis.matched_skills.slice(0, 6).map((skill, idx) => (
                              <span key={idx} className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                                {skill}
                              </span>
                            ))}
                            {job.skills_analysis.matched_skills.length > 6 && (
                              <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                                +{job.skills_analysis.matched_skills.length - 6} more
                              </span>
                            )}
                          </div>
                        </div>
                      )}
                      
                      {job.skills_analysis.missing_skills?.length > 0 && (
                        <div>
                          <h4 className="text-sm font-medium text-red-700 mb-2 flex items-center">
                            <XCircleIcon className="h-4 w-4 mr-1" />
                            Skills to Develop ({job.skills_analysis.missing_skills.length})
                          </h4>
                          <div className="flex flex-wrap gap-1">
                            {job.skills_analysis.missing_skills.slice(0, 4).map((skill, idx) => (
                              <span key={idx} className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-full">
                                {skill}
                              </span>
                            ))}
                            {job.skills_analysis.missing_skills.length > 4 && (
                              <span className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-full">
                                +{job.skills_analysis.missing_skills.length - 4} more
                              </span>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
        </div>

        {/* Tips for Improvement */}
        <div className="mt-8 bg-blue-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-4">Tips to Improve Your Matches</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start space-x-2">
              <CheckCircleIcon className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <p className="text-blue-800">Add missing technical skills to your resume</p>
            </div>
            <div className="flex items-start space-x-2">
              <CheckCircleIcon className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <p className="text-blue-800">Include relevant project experience and achievements</p>
            </div>
            <div className="flex items-start space-x-2">
              <CheckCircleIcon className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <p className="text-blue-800">Use industry-standard keywords and terminology</p>
            </div>
            <div className="flex items-start space-x-2">
              <CheckCircleIcon className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <p className="text-blue-800">Quantify your experience with specific metrics</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CandidateMatches;