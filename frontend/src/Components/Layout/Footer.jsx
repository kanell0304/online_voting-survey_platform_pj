import React from 'react';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white border-t border-gray-200">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 text-center text-sm text-gray-500">
        <p>
          &copy; {currentYear} Voting & Survey. All rights reserved.
        </p>
        <p className="mt-1">
          Made by Your Team Name
        </p>
      </div>
    </footer>
  );
}