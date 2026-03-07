import React from 'react';
import { Eye, Share2, TrendingUp, Clock3, Sparkles } from 'lucide-react';
import RelevanceScore from './RelevanceScore';

const formatNumber = (num) => {
  if (!Number.isFinite(num)) return '0';
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
  return `${num}`;
};

const getTimeAgo = (timestamp) => {
  const seconds = Math.floor((Date.now() - timestamp) / 1000);
  if (seconds < 3600) return `${Math.max(1, Math.floor(seconds / 60))}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
};

const deriveTrajectory = (velocity) => {
  if (velocity >= 88) return 'Rising';
  if (velocity >= 72) return 'Peaking';
  return 'Cooling';
};

const TrendCard = ({ trend, selected, onSelect }) => {
  const velocity = trend.engagementMetrics?.velocity || 0;
  const trajectory = trend.trajectory || deriveTrajectory(velocity);

  return (
    <article className={`trend-explorer-card ${selected ? 'selected' : ''}`}>
      <header className="trend-explorer-head">
        <div>
          <h3>{trend.title}</h3>
          <div className="trend-explorer-tags">
            <span className="trend-chip category">{trend.category}</span>
            <span className="trend-chip source">{trend.source}</span>
            <span className="trend-chip trajectory">{trajectory}</span>
          </div>
        </div>
        <RelevanceScore score={trend.relevanceScore} compact />
      </header>

      <p className="trend-explorer-desc">{trend.description}</p>

      <div className="trend-explorer-meta">
        <span className="meta-views"><Eye size={14} /> {formatNumber(trend.engagementMetrics?.views || 0)}</span>
        <span className="meta-shares"><Share2 size={14} /> {formatNumber(trend.engagementMetrics?.shares || 0)}</span>
        <span className="meta-velocity"><TrendingUp size={14} /> {velocity}% velocity</span>
        <span className="meta-time"><Clock3 size={14} /> {getTimeAgo(trend.timestamp)}</span>
      </div>

      <div className="trend-explorer-actions">
        <button
          type="button"
          className="trend-btn ghost view-details"
          onClick={(event) => {
            event.stopPropagation();
            onSelect(trend);
          }}
        >
          <Sparkles size={14} /> View Details
        </button>
      </div>
    </article>
  );
};

export default TrendCard;
