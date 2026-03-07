import React from 'react';

const ContentDistribution = ({ data }) => {
  const colors = [
    'rgba(167, 139, 250, 0.8)',
    'rgba(236, 72, 153, 0.8)',
    'rgba(6, 182, 212, 0.8)',
    'rgba(16, 185, 129, 0.8)',
    'rgba(245, 158, 11, 0.8)',
  ];

  return (
    <div className="content-distribution-compact">
      <div className="chart-section">
        <div className="pie-chart">
          {/* Pie chart visual */}
        </div>
      </div>
      <div className="legend-section">
        {data.map((item, index) => (
          <div key={index} className="legend-item-compact">
            <div className="legend-left">
              <div
                className="legend-color"
                style={{ background: colors[index] }}
              />
              <span className="legend-label">{item.category}</span>
            </div>
            <div className="legend-right">
              <span className="legend-count">{item.count}</span>
              <span className="legend-percentage">{item.percentage}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ContentDistribution;
