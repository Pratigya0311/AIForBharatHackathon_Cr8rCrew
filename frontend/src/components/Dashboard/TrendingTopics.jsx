import React from 'react';
import { useNavigate } from 'react-router-dom';

import { Flame, Eye, Share2, TrendingUp, Clock, Search } from 'lucide-react';

const formatNumber = (num) => {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
  return num.toString();
};

const getTimeAgo = (timestamp) => {
  const seconds = Math.floor((Date.now() - timestamp) / 1000);
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
};

const TrendingTopics = ({ trends }) => {
  const navigate = useNavigate();

  const openTrendInExplorer = (trendId) => {
    navigate(`/trends?trend=${encodeURIComponent(trendId)}`);
  };

  if (!trends || trends.length === 0) {
    return (
      <div className="trending-topics">
        <h2><Flame size={24} style={{ color: '#f59e0b' }} /> Trending Topics</h2>
        <div className="empty-state">
          <div className="empty-state-icon">
            <Search size={64} strokeWidth={1.5} />
          </div>
          <div className="empty-state-title">No trending topics yet</div>
          <div className="empty-state-description">
            We're analyzing trends based on your profile. Check back soon to discover relevant topics!
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="trending-topics">
      <h2><Flame size={24} style={{ color: '#f59e0b' }} /> Trending Topics</h2>
      <div className="trends-grid">
        {trends.map((trend) => (
          <div
            key={trend.trendId}
            className="trend-card"
            role="button"
            tabIndex={0}
            onClick={() => openTrendInExplorer(trend.trendId)}
            onKeyDown={(event) => {
              if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                openTrendInExplorer(trend.trendId);
              }
            }}
            aria-label={`Open ${trend.title} in Trend Explorer`}
          >
            <div className="trend-header">
              <div style={{ flex: 1 }}>
                <div className="trend-title">{trend.title}</div>
                <span className="trend-category">{trend.category}</span>
              </div>
              <div className="trend-score">
                {trend.relevanceScore}%
              </div>
            </div>
            <div className="trend-description">{trend.description}</div>
            <div className="trend-meta">
              <div className="trend-meta-item">
                <Eye size={14} style={{ color: '#06b6d4' }} />
                <span>{formatNumber(trend.engagementMetrics.views)}</span>
              </div>
              <div className="trend-meta-item">
                <Share2 size={14} style={{ color: '#ec4899' }} />
                <span>{formatNumber(trend.engagementMetrics.shares)}</span>
              </div>
              <div className="trend-meta-item">
                <TrendingUp size={14} style={{ color: '#10b981' }} />
                <span>{trend.engagementMetrics.velocity}%</span>
              </div>
              <div className="trend-meta-item">
                <Clock size={14} style={{ color: '#94a3b8' }} />
                <span>{getTimeAgo(trend.timestamp)}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TrendingTopics;
