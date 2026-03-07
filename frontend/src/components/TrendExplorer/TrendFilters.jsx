import React from 'react';
import { Search, Filter, ArrowUpDown, SlidersHorizontal, RefreshCw, ChevronDown } from 'lucide-react';

const TrendFilters = ({ filters, onChange, categories, sources, totalCount, filteredCount, onRefresh }) => {
  return (
    <section className="trend-filters-card">
      <div className="trend-filters-top">
        <div>
          <h2>Explore Trends</h2>
          <p>{filteredCount} of {totalCount} trends in view</p>
        </div>
        <button type="button" className="trend-refresh-btn" onClick={onRefresh}>
          <RefreshCw size={15} /> Refresh
        </button>
      </div>

      <div className="trend-filters-grid">
        <label className="trend-filter-field search">
          <Search size={16} />
          <input
            type="text"
            value={filters.query}
            onChange={(event) => onChange('query', event.target.value)}
            placeholder="Search trends"
          />
        </label>

        <label className="trend-filter-field has-select">
          <Filter size={16} />
          <select value={filters.category} onChange={(event) => onChange('category', event.target.value)}>
            <option value="all">All Categories</option>
            {categories.map((item) => (
              <option key={item} value={item}>{item}</option>
            ))}
          </select>
          <ChevronDown size={14} className="trend-select-arrow" />
        </label>

        <label className="trend-filter-field has-select">
          <SlidersHorizontal size={16} />
          <select value={filters.source} onChange={(event) => onChange('source', event.target.value)}>
            <option value="all">All Sources</option>
            {sources.map((item) => (
              <option key={item} value={item}>{item}</option>
            ))}
          </select>
          <ChevronDown size={14} className="trend-select-arrow" />
        </label>

        <label className="trend-filter-field has-select">
          <ArrowUpDown size={16} />
          <select value={filters.sortBy} onChange={(event) => onChange('sortBy', event.target.value)}>
            <option value="relevance">Sort: Relevance</option>
            <option value="newest">Sort: Newest</option>
            <option value="velocity">Sort: Velocity</option>
            <option value="views">Sort: Views</option>
          </select>
          <ChevronDown size={14} className="trend-select-arrow" />
        </label>
      </div>

      <div className="trend-relevance-filter">
        <span>Min relevance: <strong>{filters.minRelevance}%</strong></span>
        <input
          type="range"
          min="50"
          max="100"
          step="5"
          value={filters.minRelevance}
          onChange={(event) => onChange('minRelevance', Number(event.target.value))}
        />
      </div>
    </section>
  );
};

export default TrendFilters;
