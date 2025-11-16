import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  BriefcaseIcon, 
  UserGroupIcon, 
  ChartBarIcon, 
  SparklesIcon,
  ArrowRightIcon,
  CheckCircleIcon,
  DocumentTextIcon,
  CpuChipIcon,
  ChartPieIcon,
  AcademicCapIcon
} from '@heroicons/react/24/outline';

const Home = () => {
  // Background images for the hero carousel
  const backgroundImages = [
    {
      url: "https://images.unsplash.com/photo-1557804506-669a67965ba0?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2000&q=80",
      alt: "Resume matching professional environment"
    },
    {
      url: "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2000&q=80",
      alt: "HR team reviewing resumes and candidate profiles"
    },
    {
      url: "https://images.unsplash.com/photo-1586953208448-b95a79798f07?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2000&q=80",
      alt: "Professional writing resume and job applications"
    },
    {
      url: "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2000&q=80",
      alt: "Modern office with laptops and technology"
    }
  ];

  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(true);

  // Auto-slide effect
  useEffect(() => {
    if (!isPlaying) return;
    
    const interval = setInterval(() => {
      setCurrentImageIndex((prevIndex) => 
        prevIndex === backgroundImages.length - 1 ? 0 : prevIndex + 1
      );
    }, 5000); // Change image every 5 seconds

    return () => clearInterval(interval);
  }, [backgroundImages.length, isPlaying]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section 
        className="relative min-h-screen bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 overflow-hidden"
        onMouseEnter={() => setIsPlaying(false)}
        onMouseLeave={() => setIsPlaying(true)}
      >
        {/* Background Image Carousel */}
        <div className="absolute inset-0">
          {backgroundImages.map((image, index) => (
            <div
              key={index}
              className={`absolute inset-0 transition-opacity duration-1000 ease-in-out ${
                index === currentImageIndex ? 'opacity-80' : 'opacity-0'
              }`}
            >
              <img
                src={image.url}
                alt={image.alt}
                className="w-full h-full object-cover"
              />
            </div>
          ))}
          <div className="absolute inset-0 bg-black opacity-50"></div>
        </div>

        {/* Navigation Arrows */}
        <button
          onClick={() => setCurrentImageIndex(currentImageIndex === 0 ? backgroundImages.length - 1 : currentImageIndex - 1)}
          className="absolute left-4 top-1/2 transform -translate-y-1/2 z-20 bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-full p-3 transition-all duration-300 group"
          aria-label="Previous image"
        >
          <svg className="w-6 h-6 text-white group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <button
          onClick={() => setCurrentImageIndex(currentImageIndex === backgroundImages.length - 1 ? 0 : currentImageIndex + 1)}
          className="absolute right-4 top-1/2 transform -translate-y-1/2 z-20 bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-full p-3 transition-all duration-300 group"
          aria-label="Next image"
        >
          <svg className="w-6 h-6 text-white group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>

        {/* Image Indicators */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-2 z-20">
          {backgroundImages.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentImageIndex(index)}
              className={`w-3 h-3 rounded-full transition-all duration-300 ${
                index === currentImageIndex 
                  ? 'bg-yellow-400 scale-110 shadow-lg' 
                  : 'bg-white/50 hover:bg-white/75 hover:scale-105'
              }`}
              aria-label={`Go to slide ${index + 1}`}
            />
          ))}
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 min-h-screen flex items-center">
          <div className="text-center text-white z-10 w-full">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-display font-bold leading-tight mb-6 tracking-tight">
              AI-Powered Resume Matching
              <span className="block text-yellow-400 font-extrabold">Made Simple</span>
            </h1>
            
            <p className="text-xl md:text-2xl font-body text-gray-200 mb-12 max-w-3xl mx-auto leading-relaxed">
              Connect the right talent with the right opportunities using advanced 
              Natural Language Processing technology. Smart, fast, and accurate.
            </p>

            <div className="flex flex-col sm:flex-row gap-6 justify-center mb-16">
              <Link
                to="/recruiter"
                className="bg-yellow-400 text-gray-900 px-8 py-4 rounded-lg text-lg font-display font-semibold hover:bg-yellow-300 transition-colors duration-300 flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl transform hover:scale-105"
              >
                <BriefcaseIcon className="h-6 w-6" />
                <span>Post a Job</span>
                <ArrowRightIcon className="h-5 w-5" />
              </Link>
              <Link
                to="/candidate"
                className="bg-transparent border-2 border-white text-white px-8 py-4 rounded-lg text-lg font-display font-semibold hover:bg-white hover:text-gray-900 transition-colors duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
              >
                Upload Resume
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
              <div className="bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg rounded-lg p-6">
                <SparklesIcon className="h-12 w-12 text-yellow-400 mx-auto mb-4" />
                <h3 className="text-xl font-display font-semibold mb-2">AI-Powered</h3>
                <p className="text-gray-200 font-body">Advanced algorithms for precise matching</p>
              </div>
              <div className="bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg rounded-lg p-6">
                <ChartBarIcon className="h-12 w-12 text-yellow-400 mx-auto mb-4" />
                <h3 className="text-xl font-display font-semibold mb-2">Smart Analytics</h3>
                <p className="text-gray-200 font-body">Detailed insights and match scores</p>
              </div>
              <div className="bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg rounded-lg p-6">
                <UserGroupIcon className="h-12 w-12 text-yellow-400 mx-auto mb-4" />
                <h3 className="text-xl font-display font-semibold mb-2">User Friendly</h3>
                <p className="text-gray-200 font-body">Simple interface for everyone</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            {/* Left Image */}
            <div className="relative">
              <img
                src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80"
                alt="Team collaboration in modern office"
                className="rounded-2xl shadow-xl"
              />
              <div className="absolute -bottom-8 -right-8 bg-white rounded-xl p-6 shadow-lg">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-1"></div>
                  <div className="text-sm text-gray-600"></div>
                </div>
              </div>
            </div>

            {/* Right Content */}
            <div>
              <div className="text-blue-600 font-display font-semibold text-lg mb-4 tracking-wide">WHY CHOOSE US</div>
              <h2 className="text-3xl md:text-4xl font-heading font-bold text-gray-900 mb-6 leading-tight">
                We Help Companies Scale Engineering Capacity
              </h2>
              <p className="text-gray-600 mb-8 font-body leading-relaxed text-lg">
                Our cutting-edge AI technology makes recruitment smarter, faster, and more accurate. 
                We understand the challenges of finding the right talent and provide solutions that 
                scale with your business needs.
              </p>

              <div className="space-y-6">
                {[
                  {
                    icon: SparklesIcon,
                    title: "AI-Powered Matching",
                    description: "Advanced NLP algorithms analyze resumes and job descriptions for perfect matches."
                  },
                  {
                    icon: ChartBarIcon,
                    title: "Detailed Analytics",
                    description: "Get comprehensive similarity scores and detailed match insights."
                  },
                  {
                    icon: UserGroupIcon,
                    title: "Scalable Solution",
                    description: "Handle thousands of candidates with consistent, objective evaluation."
                  }
                ].map((item, index) => (
                  <div key={index} className="flex items-start space-x-4">
                    <div className="bg-blue-100 p-3 rounded-lg flex-shrink-0">
                      <item.icon className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="font-display font-semibold text-gray-900 mb-2">{item.title}</h3>
                      <p className="text-gray-600 font-body">{item.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="text-blue-600 font-display font-semibold text-lg mb-4 tracking-wide">OUR SERVICES</div>
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-gray-900 mb-4 leading-tight">
              AI-Powered Solutions for Your Business
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto font-body leading-relaxed">
              Comprehensive recruitment tools designed to streamline your hiring process
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                icon: CpuChipIcon,
                title: "AI Matching",
                description: "Advanced NLP algorithms for precise candidate-job matching with 95% accuracy."
              },
              {
                icon: ChartPieIcon,
                title: "Analytics Dashboard",
                description: "Comprehensive insights and detailed match analytics for better decisions."
              },
              {
                icon: DocumentTextIcon,
                title: "Resume Processing",
                description: "Support for multiple file formats with instant text extraction and analysis."
              },
              {
                icon: AcademicCapIcon,
                title: "Skill Assessment",
                description: "Intelligent skill extraction and comparison for technical competency evaluation."
              }
            ].map((service, index) => (
              <div key={index} className="bg-blue-600 text-white p-8 rounded-2xl hover:bg-blue-700 transition-colors duration-300 group cursor-pointer">
                <div className="bg-white/20 w-16 h-16 rounded-xl flex items-center justify-center mb-6 group-hover:bg-white/30 transition-colors duration-300">
                  <service.icon className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-display font-semibold mb-4">{service.title}</h3>
                <p className="text-blue-100 leading-relaxed font-body">{service.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="text-blue-600 font-display font-semibold text-lg mb-4 tracking-wide">PROCESS</div>
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-gray-900 mb-4 leading-tight">
              How We Work
            </h2>
            <p className="text-xl text-gray-600 font-body leading-relaxed">
              Simple, fast, and effective recruitment process
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            {/* For Recruiters */}
            <div>
              <h3 className="text-2xl font-heading font-bold text-gray-900 mb-6">For Recruiters</h3>
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <CheckCircleIcon className="h-6 w-6 text-green-500 mt-1 flex-shrink-0" />
                  <div>
                    <h4 className="font-display font-semibold text-gray-900">Post Job Description</h4>
                    <p className="text-gray-600 font-body">Enter your job requirements and description</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircleIcon className="h-6 w-6 text-green-500 mt-1 flex-shrink-0" />
                  <div>
                    <h4 className="font-display font-semibold text-gray-900">AI Analysis</h4>
                    <p className="text-gray-600 font-body">Our NLP engine processes and analyzes the content</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircleIcon className="h-6 w-6 text-green-500 mt-1 flex-shrink-0" />
                  <div>
                    <h4 className="font-display font-semibold text-gray-900">Get Matches</h4>
                    <p className="text-gray-600 font-body">Receive ranked candidates with similarity scores</p>
                  </div>
                </div>
              </div>
            </div>

            {/* For Candidates */}
            <div>
              <h3 className="text-2xl font-heading font-bold text-gray-900 mb-6">For Job Seekers</h3>
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <CheckCircleIcon className="h-6 w-6 text-green-500 mt-1 flex-shrink-0" />
                  <div>
                    <h4 className="font-display font-semibold text-gray-900">Upload Resume</h4>
                    <p className="text-gray-600 font-body">Upload your resume in PDF, DOC, or TXT format</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircleIcon className="h-6 w-6 text-green-500 mt-1 flex-shrink-0" />
                  <div>
                    <h4 className="font-display font-semibold text-gray-900">Smart Processing</h4>
                    <p className="text-gray-600 font-body">AI extracts and analyzes your skills and experience</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircleIcon className="h-6 w-6 text-green-500 mt-1 flex-shrink-0" />
                  <div>
                    <h4 className="font-display font-semibold text-gray-900">Find Opportunities</h4>
                    <p className="text-gray-600 font-body">Get matched with relevant job opportunities</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-heading font-bold text-white mb-4 leading-tight">
            Ready to Transform Your Recruitment?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto font-body leading-relaxed">
            Join thousands of recruiters and job seekers who are already using AI to make better matches.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/recruiter"
              className="bg-white text-blue-600 px-8 py-4 rounded-lg font-display font-semibold hover:bg-gray-100 transition-colors duration-200"
            >
              Start as Recruiter
            </Link>
            <Link
              to="/candidate"
              className="bg-blue-700 text-white px-8 py-4 rounded-lg font-display font-semibold hover:bg-blue-800 transition-colors duration-200"
            >
              Start as Job Seeker
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
