import { FileText, TrendingUp, CheckSquare, Clock } from 'lucide-react';

const QuickStats = ({ stats }) => {
  const statItems = [
    {
      label: 'Scripts Generated',
      value: stats.scriptsGenerated,
      icon: FileText,
      change: '+12%',
      positive: true,
      iconColor: '#ffffff',
      bgColor: '#3b82f6'
    },
    {
      label: 'Trends Tracked',
      value: stats.trendsTracked,
      icon: TrendingUp,
      change: '+8%',
      positive: true,
      iconColor: '#ffffff',
      bgColor: '#10b981'
    },
    {
      label: 'Scripts Used',
      value: stats.scriptsUsed,
      icon: CheckSquare,
      change: `${Math.round((stats.scriptsUsed / stats.scriptsGenerated) * 100)}%`,
      positive: true,
      iconColor: '#ffffff',
      bgColor: '#f59e0b'
    },
    {
      label: 'Time Saved',
      value: `${stats.timeSaved}h`,
      icon: Clock,
      change: '+15%',
      positive: true,
      iconColor: '#ffffff',
      bgColor: '#06b6d4'
    },
  ];

  return (
    <div className="quick-stats">
      {statItems.map((stat, index) => {
        const Icon = stat.icon;
        return (
          <div key={index} className="stat-card">
            <div className="stat-content">
              <div className="stat-icon-wrapper" style={{ backgroundColor: stat.bgColor }}>
                <Icon size={18} color={stat.iconColor} strokeWidth={2} />
              </div>
              <div className="stat-info">
                <div className="stat-value">{stat.value}</div>
                <div className="stat-label">{stat.label}</div>
                <div className={`stat-change ${stat.positive ? 'positive' : 'negative'}`}>
                  ↑ {stat.change} from last month
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default QuickStats;
