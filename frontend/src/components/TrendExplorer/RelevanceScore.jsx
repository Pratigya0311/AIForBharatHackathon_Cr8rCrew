import React from 'react';

const RelevanceScore = ({ score, compact = false }) => {
  const value = Math.max(0, Math.min(100, Number(score) || 0));
  let level = 'low';
  if (value >= 85) level = 'high';
  else if (value >= 70) level = 'medium';

  return (
    <div className={`trend-relevance ${compact ? 'compact' : ''}`}>
      <span className={`trend-relevance-pill ${level}`}>{value}%</span>
      {!compact && (
        <div className="trend-relevance-track" aria-hidden="true">
          <div className={`trend-relevance-fill ${level}`} style={{ width: `${value}%` }} />
        </div>
      )}
    </div>
  );
};

export default RelevanceScore;
