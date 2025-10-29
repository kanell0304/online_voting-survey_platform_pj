import React from 'react';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white border-t border-gray-200">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 text-center text-sm text-gray-500">
        <p className="font-medium text-gray-700">Made for mz, built with FORMZ</p>
        <p className="mt-1 text-gray-400">{currentYear} FORMZ. Designed by Group2</p>
      </div>
    </footer>
  );
}
