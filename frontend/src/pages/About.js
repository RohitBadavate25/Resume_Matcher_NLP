import React from 'react';
import { 
  BriefcaseIcon, 
  SparklesIcon, 
  ShieldCheckIcon, 
  ClockIcon,
  UsersIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';

const About = () => {
  const features = [
    {
      icon: SparklesIcon,
      title: 'Advanced NLP Technology',
      description: 'Utilizes state-of-the-art Natural Language Processing with BERT embeddings and semantic similarity analysis for accurate matching.'
    },
    {
      icon: ClockIcon,
      title: 'Real-time Processing',
      description: 'Fast document processing and matching algorithms that deliver results in seconds, not hours.'
    },
    {
      icon: ShieldCheckIcon,
      title: 'Secure & Private',
      description: 'Your documents are processed securely with privacy in mind. No data is shared with third parties.'
    },
    {
      icon: ChartBarIcon,
      title: 'Detailed Analytics',
      description: 'Comprehensive similarity scores, skill matching, and detailed insights to help make informed decisions.'
    },
    {
      icon: UsersIcon,
      title: 'Dual Interface',
      description: 'Separate optimized experiences for recruiters and job seekers with tailored workflows.'
    },
    {
      icon: BriefcaseIcon,
      title: 'Multiple File Formats',
      description: 'Supports PDF, DOC, DOCX, and TXT file formats for maximum compatibility.'
    }
  ];

  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-br from-indigo-600 via-purple-600 to-blue-800 py-20 overflow-hidden">
        <div className="absolute inset-0">
          <img
            src="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2000&q=80"
            alt="Modern office with laptops showing resume analysis and AI technology"
            className="w-full h-full object-cover opacity-20"
          />
        </div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-white">
          <h1 className="text-4xl md:text-6xl font-bold mb-8">
            About <span className="text-yellow-400">ResumeMatch</span>
          </h1>
          <p className="text-xl md:text-2xl text-indigo-100 max-w-4xl mx-auto mb-12 leading-relaxed">
            ResumeMatch is an AI-powered recruitment platform that uses advanced Natural Language Processing 
            to match job descriptions with resumes, helping recruiters find the best candidates faster and 
            more accurately than ever before.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
              <div className="text-3xl font-bold text-yellow-400 mb-2">95%</div>
              <div className="text-indigo-100">Match Accuracy</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
              <div className="text-3xl font-bold text-yellow-400 mb-2">&lt;5s</div>
              <div className="text-indigo-100">Processing Time</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
              <div className="text-3xl font-bold text-yellow-400 mb-2">10k+</div>
              <div className="text-indigo-100">Resumes Processed</div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-16 relative z-10">

        {/* Problem & Solution */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-20">
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-red-50 rounded-full -mr-16 -mt-16"></div>
            <div className="relative">
              <div className="bg-gradient-to-r from-red-500 to-red-600 w-16 h-16 rounded-xl flex items-center justify-center mb-6">
                <span className="text-white text-2xl font-bold">!</span>
              </div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">The Problem</h2>
              <div className="space-y-6 text-gray-700">
                <p className="text-lg leading-relaxed">
                  Traditional recruitment processes are time-consuming and often ineffective. Recruiters spend 
                  countless hours manually reviewing resumes, trying to match candidates with job requirements.
                </p>
                <div className="space-y-4">
                  <div className="flex items-start space-x-4 p-4 bg-red-50 rounded-lg">
                    <div className="bg-red-500 w-2 h-2 rounded-full mt-2 flex-shrink-0"></div>
                    <span className="text-gray-800">Manual resume screening takes 10-15 minutes per resume</span>
                  </div>
                  <div className="flex items-start space-x-4 p-4 bg-red-50 rounded-lg">
                    <div className="bg-red-500 w-2 h-2 rounded-full mt-2 flex-shrink-0"></div>
                    <span className="text-gray-800">Human bias can lead to missed opportunities</span>
                  </div>
                  <div className="flex items-start space-x-4 p-4 bg-red-50 rounded-lg">
                    <div className="bg-red-500 w-2 h-2 rounded-full mt-2 flex-shrink-0"></div>
                    <span className="text-gray-800">Inconsistent evaluation criteria across reviewers</span>
                  </div>
                  <div className="flex items-start space-x-4 p-4 bg-red-50 rounded-lg">
                    <div className="bg-red-500 w-2 h-2 rounded-full mt-2 flex-shrink-0"></div>
                    <span className="text-gray-800">Difficulty in quantifying candidate fit</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-green-50 rounded-full -mr-16 -mt-16"></div>
            <div className="relative">
              <div className="bg-gradient-to-r from-green-500 to-green-600 w-16 h-16 rounded-xl flex items-center justify-center mb-6">
                <SparklesIcon className="h-8 w-8 text-white" />
              </div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">Our Solution</h2>
              <div className="space-y-6 text-gray-700">
                <p className="text-lg leading-relaxed">
                  ResumeMatch leverages cutting-edge AI and NLP technologies to automate and improve the 
                  resume matching process, providing objective, consistent, and fast results.
                </p>
                <div className="space-y-4">
                  <div className="flex items-start space-x-4 p-4 bg-green-50 rounded-lg">
                    <div className="bg-green-500 w-2 h-2 rounded-full mt-2 flex-shrink-0"></div>
                    <span className="text-gray-800">Automated processing in under 5 seconds</span>
                  </div>
                  <div className="flex items-start space-x-4 p-4 bg-green-50 rounded-lg">
                    <div className="bg-green-500 w-2 h-2 rounded-full mt-2 flex-shrink-0"></div>
                    <span className="text-gray-800">Objective, bias-free candidate ranking</span>
                  </div>
                  <div className="flex items-start space-x-4 p-4 bg-green-50 rounded-lg">
                    <div className="bg-green-500 w-2 h-2 rounded-full mt-2 flex-shrink-0"></div>
                    <span className="text-gray-800">Consistent evaluation using AI algorithms</span>
                  </div>
                  <div className="flex items-start space-x-4 p-4 bg-green-50 rounded-lg">
                    <div className="bg-green-500 w-2 h-2 rounded-full mt-2 flex-shrink-0"></div>
                    <span className="text-gray-800">Quantified similarity scores and insights</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Features */}
        <div className="mb-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Key Features</h2>
            <p className="text-lg text-gray-600">
              Everything you need for intelligent resume matching
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200">
                <div className="bg-blue-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="h-6 w-6 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* How It Works */}
        <div className="mb-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">How It Works</h2>
            <p className="text-lg text-gray-600">
              Advanced AI technology behind the matching process
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-blue-600">1</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Text Extraction</h3>
                <p className="text-gray-600">Extract and clean text from various document formats</p>
              </div>

              <div className="text-center">
                <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-blue-600">2</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">NLP Processing</h3>
                <p className="text-gray-600">Apply advanced NLP techniques to understand context and meaning</p>
              </div>

              <div className="text-center">
                <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-blue-600">3</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Semantic Analysis</h3>
                <p className="text-gray-600">Generate embeddings and calculate semantic similarities</p>
              </div>

              <div className="text-center">
                <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-blue-600">4</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Smart Matching</h3>
                <p className="text-gray-600">Rank candidates based on multiple similarity metrics</p>
              </div>
            </div>
          </div>
        </div>

       

        {/* Stats */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-8 text-white text-center">
          <h2 className="text-3xl font-bold mb-8">ResumeMatch by the Numbers</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="text-4xl font-bold mb-2">95%</div>
              <div className="text-blue-100">Match Accuracy</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">&lt;5s</div>
              <div className="text-blue-100">Processing Time</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">80%</div>
              <div className="text-blue-100">Time Saved</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">4+</div>
              <div className="text-blue-100">File Formats</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
