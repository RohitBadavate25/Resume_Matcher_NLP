import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Bars3Icon, XMarkIcon, BriefcaseIcon } from '@heroicons/react/24/outline';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'For Recruiters', href: '/recruiter' },
    { name: 'For Candidates', href: '/candidate' },
    { name: 'About', href: '/about' },
  ];

  const isActive = (path) => {
    if (path === '/' && location.pathname === '/') return true;
    return path !== '/' && location.pathname.startsWith(path);
  };

  return (
    <header className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-3 sm:py-4">
          {/* Logo - Responsive sizing */}
          <Link to="/" className="flex items-center space-x-2 flex-shrink-0">
            <div className="flex items-center justify-center w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg">
              <BriefcaseIcon className="h-5 w-5 sm:h-6 sm:w-6 text-white" />
            </div>
            <div className="hidden sm:block">
              <h1 className="text-lg sm:text-xl font-display font-bold text-gray-900">ResumeMatch</h1>
              <p className="text-xs text-gray-500 font-body">AI-Powered Recruitment</p>
            </div>
            <div className="block sm:hidden">
              <h1 className="text-lg font-display font-bold text-gray-900">RM</h1>
            </div>
          </Link>

          {/* Desktop Navigation - Better responsive breakpoints */}
          <nav className="hidden lg:flex space-x-6 xl:space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`px-3 py-2 rounded-md text-sm font-display font-medium transition-colors duration-200 whitespace-nowrap ${
                  isActive(item.href)
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </nav>

          {/* Tablet Navigation - Show condensed version on medium screens */}
          <nav className="hidden md:flex lg:hidden space-x-4">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`px-2 py-2 rounded-md text-sm font-display font-medium transition-colors duration-200 ${
                  isActive(item.href)
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
                }`}
              >
                {item.name === 'For Recruiters' ? 'Recruiters' : 
                 item.name === 'For Candidates' ? 'Candidates' : item.name}
              </Link>
            ))}
          </nav>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
              aria-label={isMenuOpen ? 'Close menu' : 'Open menu'}
            >
              {isMenuOpen ? (
                <XMarkIcon className="h-6 w-6" />
              ) : (
                <Bars3Icon className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation - Enhanced with animations */}
        <div 
          className={`md:hidden border-t border-gray-200 transition-all duration-300 ease-in-out ${
            isMenuOpen 
              ? 'opacity-100 max-h-96 pb-4' 
              : 'opacity-0 max-h-0 overflow-hidden'
          }`}
        >
          <div className="py-2 space-y-1">
            {navigation.map((item, index) => (
              <Link
                key={item.name}
                to={item.href}
                onClick={() => setIsMenuOpen(false)}
                className={`block px-4 py-3 rounded-md text-base font-display font-medium transition-all duration-200 transform hover:translate-x-1 ${
                  isActive(item.href)
                    ? 'text-blue-600 bg-blue-50 border-l-4 border-blue-600'
                    : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
                }`}
                style={{ 
                  transitionDelay: isMenuOpen ? `${index * 50}ms` : '0ms' 
                }}
              >
                <div className="flex items-center space-x-3">
                  <span>{item.name}</span>
                  {isActive(item.href) && (
                    <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                  )}
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
