console.log('🔍 Route Debugging Checklist');
console.log('='.repeat(40));

// Check if React Router is working
if (typeof window !== 'undefined' && window.location) {
  console.log('✅ Current URL:', window.location.href);
  console.log('✅ Current pathname:', window.location.pathname);
}

// Check if the buttons have correct paths
const buttons = document.querySelectorAll('a[href*="/recruiter"], a[href*="/candidate"]');
console.log('✅ Found', buttons.length, 'navigation buttons with correct paths');

// Check for any JavaScript errors
window.addEventListener('error', (e) => {
  console.error('❌ JavaScript Error:', e.message);
});

// Check React Router navigation
if (window.React && window.ReactRouter) {
  console.log('✅ React Router is loaded');
} else {
  console.log('⚠️ React Router might not be loaded properly');
}

console.log('🎯 If buttons show white screen:');
console.log('1. Check browser console for errors');
console.log('2. Verify React app is compiled successfully');
console.log('3. Check if backend API is accessible');
console.log('4. Test direct navigation to /recruiter and /candidate');