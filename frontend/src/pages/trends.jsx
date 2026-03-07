import React from 'react';
import TrendList from '../components/TrendExplorer/TrendList';
import TrendFilters from '../components/TrendExplorer/TrendFilters';
import { mockTrends } from '../data/mockData';

const TrendsPage = () => {
  const handleFilterChange = (filters) => {
    console.log('Filters changed:', filters);
  };

  return (
    <div className="trends-page">
      <h1>Trending Topics</h1>
      <TrendFilters onFilterChange={handleFilterChange} />
      <TrendList trends={mockTrends} />
    </div>
  );
};

export default TrendsPage;
