import React, { useMemo, useState } from 'react';
import { Search, Filter, ArrowUpDown, Trash2, Youtube, FileText, Clock3, Library, ChevronDown } from 'lucide-react';

const ContentList = ({ contents, selectedId, onSelect, onDelete }) => {
  const [query, setQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState('all');
  const [sortBy, setSortBy] = useState('recent');

  const filteredContents = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();

    const filtered = contents.filter((item) => {
      const matchesQuery =
        !normalizedQuery ||
        item.title.toLowerCase().includes(normalizedQuery) ||
        item.sourceUrl.toLowerCase().includes(normalizedQuery);
      const matchesType = typeFilter === 'all' || item.sourceType === typeFilter;
      return matchesQuery && matchesType;
    });

    return filtered.sort((a, b) => {
      if (sortBy === 'recent') return b.createdAt - a.createdAt;
      if (sortBy === 'oldest') return a.createdAt - b.createdAt;
      if (sortBy === 'title') return a.title.localeCompare(b.title);
      if (sortBy === 'words') return (b.wordCount || 0) - (a.wordCount || 0);
      return 0;
    });
  }, [contents, query, typeFilter, sortBy]);

  return (
    <section className="content-list-card">
      <div className="content-list-header-row">
        <div>
          <h3 className="content-title-with-icon">
            <Library size={18} className="content-heading-icon list" />
            Content Library
          </h3>
          <p>{filteredContents.length} item{filteredContents.length === 1 ? '' : 's'} in view</p>
        </div>
      </div>

      <div className="content-list-controls">
        <label className="content-control-field content-search-field">
          <Search size={16} />
          <input
            type="text"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search by title or URL"
          />
        </label>

        <label className="content-control-field has-select">
          <Filter size={16} />
          <select value={typeFilter} onChange={(event) => setTypeFilter(event.target.value)}>
            <option value="all">All Types</option>
            <option value="youtube">YouTube URL</option>
            <option value="transcript">Transcript</option>
          </select>
          <ChevronDown size={14} className="content-select-arrow" />
        </label>

        <label className="content-control-field has-select">
          <ArrowUpDown size={16} />
          <select value={sortBy} onChange={(event) => setSortBy(event.target.value)}>
            <option value="recent">Newest First</option>
            <option value="oldest">Oldest First</option>
            <option value="title">Title A-Z</option>
            <option value="words">Word Count</option>
          </select>
          <ChevronDown size={14} className="content-select-arrow" />
        </label>
      </div>

      <div className="content-list-items">
        {filteredContents.length === 0 ? (
          <div className="content-empty-state">
            <FileText size={40} strokeWidth={1.5} />
            <p>No content found for current filters.</p>
          </div>
        ) : (
          filteredContents.map((item) => (
            <article
              key={item.contentId}
              className={`content-list-item ${selectedId === item.contentId ? 'selected' : ''}`}
              onClick={() => onSelect(item)}
            >
              <div className="content-item-main">
                <div className={`content-item-icon ${item.sourceType === 'youtube' ? 'youtube' : 'transcript'}`}>
                  {item.sourceType === 'youtube' ? <Youtube size={16} /> : <FileText size={16} />}
                </div>
                <div className="content-item-text">
                  <h4>{item.title}</h4>
                  {item.sourceUrl ? (
                    <a href={item.sourceUrl} target="_blank" rel="noreferrer" onClick={(event) => event.stopPropagation()}>
                      {item.sourceUrl}
                    </a>
                  ) : (
                    <span className="content-source-fallback">Direct transcript input</span>
                  )}
                  <div className="content-item-meta">
                    <span><Clock3 size={14} /> {new Date(item.createdAt).toLocaleDateString()}</span>
                    <span>{item.wordCount} words</span>
                    <span>{item.language.toUpperCase()}</span>
                  </div>
                </div>
              </div>

              <button
                type="button"
                className="content-delete-btn"
                onClick={(event) => {
                  event.stopPropagation();
                  onDelete(item.contentId);
                }}
                title="Delete content"
              >
                <Trash2 size={16} />
              </button>
            </article>
          ))
        )}
      </div>
    </section>
  );
};

export default ContentList;
