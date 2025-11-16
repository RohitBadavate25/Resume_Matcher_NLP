import React from 'react';

const LoadingSpinner = ({ message = 'Loading...' }) => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-blue-200 border-solid rounded-full animate-spin border-t-blue-600 mx-auto mb-4"></div>
        </div>
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Please wait</h2>
        <p className="text-gray-600">{message}</p>
      </div>
    </div>
  );
};

export default LoadingSpinner;
