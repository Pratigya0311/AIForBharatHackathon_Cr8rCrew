import React from 'react';
import { CalendarDays, Languages, Clock3, Youtube, FileText, ScrollText } from 'lucide-react';

const ContentViewer = ({ content }) => {
  if (!content) {
    return (
      <section className="content-viewer-card content-viewer-empty">
        <FileText size={42} strokeWidth={1.4} />
        <h3>Select content to preview</h3>
        <p>Pick an item from the list to inspect transcript and metadata.</p>
      </section>
    );
  }

  return (
    <section className="content-viewer-card">
      <header className="content-viewer-header">
        <div className="content-viewer-title-row">
          <span className="content-type-chip">
            {content.sourceType === 'youtube' ? <Youtube size={14} /> : <FileText size={14} />}
            {content.sourceType === 'youtube' ? 'YouTube URL' : 'Transcript'}
          </span>
          <h3>{content.title}</h3>
        </div>
        {content.sourceUrl ? (
          <a href={content.sourceUrl} target="_blank" rel="noreferrer">
            Open Source
          </a>
        ) : (
          <span className="content-viewer-source-tag">Manual Input</span>
        )}
      </header>

      <div className="content-viewer-meta">
        <span><CalendarDays size={14} /> {new Date(content.createdAt).toLocaleString()}</span>
        <span><Clock3 size={14} /> {content.wordCount} words</span>
        <span><Languages size={14} /> {content.language.toUpperCase()}</span>
      </div>

      <div className="content-viewer-body">
        <h4 className="content-title-with-icon">
          <ScrollText size={17} className="content-heading-icon viewer" />
          Full Transcript
        </h4>
        <p>{content.transcriptText}</p>
      </div>
    </section>
  );
};

export default ContentViewer;
