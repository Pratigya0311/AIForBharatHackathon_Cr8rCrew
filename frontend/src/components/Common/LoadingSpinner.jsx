import React from 'react';

const LoadingSpinner = ({ message }) => {
  return (
    <div className="loading-spinner">
      <div className="spinner"></div>
      {message && <p>{message}</p>}
    </div>
  );
};

export default LoadingSpinner;
