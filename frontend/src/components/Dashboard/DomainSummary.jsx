import { Target, Palette, Users } from 'lucide-react';

const DomainSummary = ({ profile }) => {
  return (
    <div className="domain-summary">
      <h3><Users size={20} style={{ color: '#60a5fa' }} /> Creator Profile</h3>
      <div className="domain-content">
        {/* Row 1: Niche and Style */}
        <div className="domain-stats-row">
          <div className="domain-stat">
            <div className="domain-stat-icon-outline" style={{ backgroundColor: 'rgba(239, 68, 68, 0.1)' }}>
              <Target size={18} color="#ef4444" strokeWidth={2} />
            </div>
            <div className="domain-stat-info">
              <div className="domain-stat-label">Niche</div>
              <div className="domain-stat-value">{profile.niche}</div>
            </div>
          </div>
          
          <div className="domain-stat">
            <div className="domain-stat-icon-outline" style={{ backgroundColor: 'rgba(236, 72, 153, 0.1)' }}>
              <Palette size={18} color="#ec4899" strokeWidth={2} />
            </div>
            <div className="domain-stat-info">
              <div className="domain-stat-label">Style</div>
              <div className="domain-stat-value">{profile.tone}</div>
            </div>
          </div>
        </div>
        
        {/* Row 2: Audience */}
        <div className="domain-stat domain-stat-full">
          <div className="domain-stat-icon-outline" style={{ backgroundColor: 'rgba(96, 165, 250, 0.1)' }}>
            <Users size={18} color="#60a5fa" strokeWidth={2} />
          </div>
          <div className="domain-stat-info">
            <div className="domain-stat-label">Audience</div>
            <div className="domain-stat-value">{profile.targetAudience}</div>
          </div>
        </div>
        
        {/* Row 3: Metrics */}
        <div className="domain-metrics">
          <div className="domain-metric">
            <div className="domain-metric-value">{profile.contentCount}</div>
            <div className="domain-metric-label">Content Pieces</div>
          </div>
          <div className="domain-metric">
            <div className="domain-metric-value">{(profile.totalViews / 1000000).toFixed(1)}M</div>
            <div className="domain-metric-label">Total Views</div>
          </div>
          <div className="domain-metric">
            <div className="domain-metric-value">{(profile.subscriberCount / 1000).toFixed(0)}K</div>
            <div className="domain-metric-label">Subscribers</div>
          </div>
        </div>
        
        {/* Row 4: Languages */}
        <div className="domain-languages">
          <span className="domain-languages-label">Languages:</span>
          <div className="domain-tags">
            {profile.languages.map((lang) => (
              <span key={lang} className="domain-tag">
                {lang.toUpperCase()}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DomainSummary;
