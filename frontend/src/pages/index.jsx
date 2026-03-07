import React from 'react';
import { BarChart3, Bell } from 'lucide-react';
import DomainSummary from '../components/Dashboard/DomainSummary';
import TrendingTopics from '../components/Dashboard/TrendingTopics';
import QuickStats from '../components/Dashboard/QuickStats';
import ActivityFeed from '../components/Dashboard/ActivityFeed';
import ContentDistribution from '../components/Dashboard/ContentDistribution';
import { mockCreatorProfile, mockTrends, mockStats, mockActivities, mockContentDistribution } from '../data/mockData';

const Dashboard = () => {
  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <div>
          <h1>
            Welcome back, Alex!
            <span className="welcome-emoji" aria-hidden="true"> {"\u{1F44B}"}</span>
          </h1>
          <p className="dashboard-subtitle">Here's what's happening with your content today</p>
        </div>
      </div>
      
      <QuickStats stats={mockStats} />
      
      {/* Row 1: Content Distribution + Domain Summary on left, Recent Activity on right */}
      <div className="dashboard-row-1">
        <div className="content-domain-section">
          <div className="section-card">
            <h3><BarChart3 size={20} style={{ color: '#60a5fa' }} /> Content Distribution</h3>
            <ContentDistribution data={mockContentDistribution} />
          </div>
          <div className="section-card">
            <DomainSummary profile={mockCreatorProfile} />
          </div>
        </div>
        <div className="activity-section">
          <div className="section-card activity-card">
            <h3><Bell size={20} style={{ color: '#06b6d4' }} /> Recent Activity</h3>
            <ActivityFeed activities={mockActivities} compact={true} />
          </div>
        </div>
      </div>
      
      {/* Row 2: Trending Topics */}
      <div className="dashboard-row-2">
        <TrendingTopics trends={mockTrends.slice(0, 6)} />
      </div>
    </div>
  );
};

export default Dashboard;
