import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Clock3, Eye, Flame, Info, Share2, TrendingUp, X } from 'lucide-react';
import TrendList from '../components/TrendExplorer/TrendList';
import TrendFilters from '../components/TrendExplorer/TrendFilters';
import { mockTrends } from '../data/mockData';

const deriveTrajectory = (velocity) => {
  if (velocity >= 88) return 'Rising';
  if (velocity >= 72) return 'Peaking';
  return 'Cooling';
};

const getForecastReason = (trend) => {
  const velocity = trend.engagementMetrics?.velocity || 0;
  if (velocity >= 88) return 'Strong acceleration and high share velocity across sources.';
  if (velocity >= 72) return 'Sustained engagement with stable momentum.';
  return 'Early signals detected but currently flattening.';
};

const getTrendContext = (trend) => {
  if (trend.context && trend.context.trim()) {
    return trend.context;
  }
  return `Audience interest is concentrated around ${trend.category.toLowerCase()} content with strong ${
    trend.source
  } discovery momentum.`;
};

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

const TrendsPage = () => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const [filters, setFilters] = useState({
    query: '',
    category: 'all',
    source: 'all',
    sortBy: 'relevance',
    minRelevance: 70,
  });
  const detailsPanelRef = useRef(null);
  const selectedTrendId = searchParams.get('trend');

  const categories = useMemo(
    () => Array.from(new Set(mockTrends.map((trend) => trend.category))).sort(),
    []
  );

  const sources = useMemo(
    () => Array.from(new Set(mockTrends.map((trend) => trend.source))).sort(),
    []
  );

  const filteredTrends = useMemo(() => {
    const query = filters.query.trim().toLowerCase();

    const list = mockTrends.filter((trend) => {
      const matchesQuery =
        !query ||
        trend.title.toLowerCase().includes(query) ||
        trend.description.toLowerCase().includes(query);
      const matchesCategory = filters.category === 'all' || trend.category === filters.category;
      const matchesSource = filters.source === 'all' || trend.source === filters.source;
      const matchesRelevance = trend.relevanceScore >= filters.minRelevance;

      return matchesQuery && matchesCategory && matchesSource && matchesRelevance;
    });

    return list.sort((a, b) => {
      if (filters.sortBy === 'newest') return b.timestamp - a.timestamp;
      if (filters.sortBy === 'velocity') return (b.engagementMetrics?.velocity || 0) - (a.engagementMetrics?.velocity || 0);
      if (filters.sortBy === 'views') return (b.engagementMetrics?.views || 0) - (a.engagementMetrics?.views || 0);
      return b.relevanceScore - a.relevanceScore;
    });
  }, [filters]);

  const effectiveSelectedTrendId = filteredTrends.some((trend) => trend.trendId === selectedTrendId)
    ? selectedTrendId
    : null;

  const selectedTrend = useMemo(
    () => filteredTrends.find((trend) => trend.trendId === effectiveSelectedTrendId) || null,
    [filteredTrends, effectiveSelectedTrendId]
  );

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const handleGenerateScript = (trend) => {
    navigate('/scripts', {
      state: {
        source: 'trends',
        selectedTrend: {
          trendId: trend.trendId,
          title: trend.title,
          category: trend.category,
          source: trend.source,
          relevanceScore: trend.relevanceScore,
          description: trend.description,
        },
      },
    });
  };

  const handleViewDetails = (trend) => {
    const nextParams = new URLSearchParams(searchParams);
    nextParams.set('trend', trend.trendId);
    setSearchParams(nextParams);
  };

  useEffect(() => {
    if (selectedTrend && detailsPanelRef.current) {
      detailsPanelRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, [selectedTrend]);

  const handleRefresh = () => {
    console.log('Trend feed refreshed successfully.');
  };

  const velocity = selectedTrend?.engagementMetrics?.velocity || 0;
  const trajectory = selectedTrend ? deriveTrajectory(velocity) : 'N/A';

  return (
    <div className="trends-page">
      <section className="trends-hero">
        <h1>
          <span className="trends-hero-icon"><TrendingUp size={20} /></span>
          Trend Explorer
        </h1>
        <p>Discover high-relevance trends, inspect momentum signals, and move winning topics into script generation.</p>
      </section>

      <TrendFilters
        filters={filters}
        onChange={handleFilterChange}
        categories={categories}
        sources={sources}
        totalCount={mockTrends.length}
        filteredCount={filteredTrends.length}
        onRefresh={handleRefresh}
      />

      <div className={`trends-layout ${selectedTrend ? 'details-open' : 'details-collapsed'}`}>
        <TrendList
          trends={filteredTrends.slice(0, 10)}
          selectedTrendId={effectiveSelectedTrendId}
          onSelectTrend={handleViewDetails}
        />

        {selectedTrend && (
          <aside ref={detailsPanelRef} className="trend-details-panel">
            <div className="trend-details-head">
              <div>
                <span className="trend-details-kicker">Selected Topic</span>
                <h3>Trend Details</h3>
              </div>
              <button
                type="button"
                className="trend-details-close"
                onClick={() => {
                  const nextParams = new URLSearchParams(searchParams);
                  nextParams.delete('trend');
                  setSearchParams(nextParams);
                }}
                title="Collapse details"
                aria-label="Collapse details panel"
              >
                <X size={16} />
              </button>
            </div>

            <div className="trend-details-context-card">
              <div className="trend-details-context">{selectedTrend.title}</div>
              <div className="trend-explorer-tags trend-details-tags">
                <span className="trend-chip category">{selectedTrend.category}</span>
                <span className="trend-chip source">{selectedTrend.source}</span>
                <span className="trend-chip trajectory">{trajectory}</span>
              </div>
              <div className="trend-explorer-meta trend-details-meta">
                <span className="meta-views"><Eye size={14} /> {formatNumber(selectedTrend.engagementMetrics?.views || 0)}</span>
                <span className="meta-shares"><Share2 size={14} /> {formatNumber(selectedTrend.engagementMetrics?.shares || 0)}</span>
                <span className="meta-velocity"><TrendingUp size={14} /> {velocity}% velocity</span>
                <span className="meta-time"><Clock3 size={14} /> {getTimeAgo(selectedTrend.timestamp)}</span>
              </div>
            </div>

            <div className="trend-context-box">
              <h4>Full Context</h4>
              <p>{selectedTrend.description}</p>
              <p>{getTrendContext(selectedTrend)}</p>
            </div>

            <div className="trend-details-grid">
              <div className="trend-detail-item">
                <span>Trajectory</span>
                <strong>{trajectory}</strong>
              </div>
              <div className="trend-detail-item">
                <span>Novelty Score</span>
                <strong>{Math.max(55, Math.min(95, selectedTrend.relevanceScore - 8))}%</strong>
              </div>
            </div>

            <div className="trend-forecast-box">
              <h4><Info size={15} /> Why this is relevant</h4>
              <p>{getForecastReason(selectedTrend)}</p>
            </div>

            <button
              type="button"
              className="trend-details-generate-btn"
              onClick={() => handleGenerateScript(selectedTrend)}
            >
              <Flame size={15} /> Generate Script
            </button>
          </aside>
        )}
      </div>
    </div>
  );
};

export default TrendsPage;
