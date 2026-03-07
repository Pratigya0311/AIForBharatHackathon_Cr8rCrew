import React from 'react';

import { FileText, TrendingUp, FolderOpen, CheckCircle, Trophy, Bell } from 'lucide-react';

const ActivityFeed = ({ activities, compact = false }) => {
  const getTimeAgo = (timestamp) => {
    const seconds = Math.floor((Date.now() - timestamp) / 1000);
    if (seconds < 60) return 'Just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    return `${Math.floor(seconds / 86400)}d ago`;
  };

  const getActivityIconConfig = (type) => {
    switch (type) {
      case 'script_generated':
        return { icon: FileText, color: '#3b82f6', bg: 'rgba(59, 130, 246, 0.1)' };
      case 'trend_discovered':
        return { icon: TrendingUp, color: '#10b981', bg: 'rgba(16, 185, 129, 0.1)' };
      case 'content_uploaded':
        return { icon: FolderOpen, color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)' };
      case 'script_finalized':
      case 'script_published':
        return { icon: CheckCircle, color: '#10b981', bg: 'rgba(16, 185, 129, 0.1)' };
      case 'milestone':
        return { icon: Trophy, color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)' };
      default:
        return { icon: Bell, color: '#8b5cf6', bg: 'rgba(139, 92, 246, 0.1)' };
    }
  };

  if (!activities || activities.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">
          <Bell size={64} strokeWidth={1.5} />
        </div>
        <div className="empty-state-title">No activity yet</div>
        <div className="empty-state-description">
          Start creating content and your activity will appear here
        </div>
      </div>
    );
  }

  return (
    <div className={`activity-list ${compact ? 'compact' : ''}`}>
      {activities.map((activity) => {
        const config = getActivityIconConfig(activity.type);
        const Icon = config.icon;
        return (
          <div key={activity.id} className="activity-item">
            <div className="activity-icon-outline" style={{ backgroundColor: config.bg }}>
              <Icon size={18} color={config.color} strokeWidth={2} />
            </div>
            <div className="activity-content">
              <div className="activity-title">{activity.title}</div>
              <div className="activity-time">{getTimeAgo(activity.timestamp)}</div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ActivityFeed;
