import React from 'react';
import { SearchX } from 'lucide-react';
import TrendCard from './TrendCard';

const TrendList = ({ trends, selectedTrendId, onSelectTrend }) => {
  if (!trends || trends.length === 0) {
    return (
      <section className="trend-list-empty">
        <SearchX size={42} strokeWidth={1.5} />
        <h3>No matching trends</h3>
        <p>Try relaxing filters or lowering the relevance threshold.</p>
      </section>
    );
  }

  return (
    <section className="trend-explorer-list">
      {trends.map((trend) => (
        <TrendCard
          key={trend.trendId}
          trend={trend}
          selected={selectedTrendId === trend.trendId}
          onSelect={onSelectTrend}
        />
      ))}
    </section>
  );
};

export default TrendList;
