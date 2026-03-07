import React, { useState } from 'react';
import { Link, LoaderCircle, PlusCircle, Sparkles, AlertCircle, FileText } from 'lucide-react';

const ContentUploader = ({ onGenerateTranscript, onAddTranscript, loading }) => {
  const [mode, setMode] = useState('url');
  const [url, setUrl] = useState('');
  const [title, setTitle] = useState('');
  const [transcriptText, setTranscriptText] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (mode === 'url') {
      const value = url.trim();
      if (!value) {
        setError('Please paste a YouTube URL.');
        return;
      }

      setError('');
      const success = await onGenerateTranscript(value);
      if (success) {
        setUrl('');
      }
      return;
    }

    const transcript = transcriptText.trim();
    if (!transcript) {
      setError('Please paste transcript text.');
      return;
    }

    setError('');
    const success = await onAddTranscript({
      title: title.trim(),
      transcriptText: transcript,
    });
    if (success) {
      setTitle('');
      setTranscriptText('');
    }
  };

  return (
    <section className="content-uploader-card">
      <div className="content-uploader-head">
        <h3>
          <span className="content-icon-badge uploader">
            <Sparkles size={14} />
          </span>
          Generate Transcript from URL
        </h3>
        <p>Paste a YouTube URL and add it directly to your content library.</p>
      </div>

      <div className="content-input-mode">
        <button
          type="button"
          className={`content-mode-btn ${mode === 'url' ? 'active' : ''}`}
          onClick={() => setMode('url')}
        >
          <Link size={14} />
          URL
        </button>
        <button
          type="button"
          className={`content-mode-btn ${mode === 'text' ? 'active' : ''}`}
          onClick={() => setMode('text')}
          title="Direct transcript input"
        >
          <FileText size={14} />
          Transcript
        </button>
      </div>

      <form onSubmit={handleSubmit} className={`content-uploader-form ${mode === 'text' ? 'text-mode' : ''}`}>
        {mode === 'url' ? (
          <label className="content-url-input-wrap">
            <Link size={16} />
            <input
              type="url"
              value={url}
              onChange={(event) => setUrl(event.target.value)}
              placeholder="https://www.youtube.com/watch?v=..."
            />
          </label>
        ) : (
          <div className="content-transcript-inputs">
            <input
              type="text"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              placeholder="Optional title (e.g., AI Agent Breakdown)"
              className="content-transcript-title"
            />
            <textarea
              value={transcriptText}
              onChange={(event) => setTranscriptText(event.target.value)}
              placeholder="Paste full transcript text here..."
              className="content-transcript-textarea"
              rows={6}
            />
          </div>
        )}

        <button type="submit" className={`content-generate-btn ${mode === 'text' ? 'compact' : ''}`} disabled={loading}>
          {loading ? <LoaderCircle size={16} className="spin" /> : <PlusCircle size={16} />}
          {loading ? 'Extracting...' : mode === 'url' ? 'Fetch Transcript' : 'Add Transcript'}
        </button>
      </form>

      {error && (
        <div className="content-inline-error">
          <AlertCircle size={15} />
          <span>{error}</span>
        </div>
      )}
    </section>
  );
};

export default ContentUploader;
