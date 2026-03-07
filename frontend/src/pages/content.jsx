import React, { useEffect, useMemo, useState } from 'react';
import { AlertCircle, CheckCircle2, LoaderCircle, Youtube } from 'lucide-react';
import ContentUploader from '../components/ContentLibrary/ContentUploader';
import ContentList from '../components/ContentLibrary/ContentList';
import ContentViewer from '../components/ContentLibrary/ContentViewer';
import { validateUrl } from '../utils/validators';
import apiClient from '../services/api';

const ContentPage = () => {
  const [contents, setContents] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState({ type: 'idle', message: '' });
  const [pendingDelete, setPendingDelete] = useState(null);

  useEffect(() => {
    const loadContents = async () => {
      try {
        setLoading(true);
        const result = await apiClient.getContentList();
        const loadedContents = result?.contents || [];
        setContents(loadedContents);
        setSelectedId(loadedContents[0]?.contentId || null);
      } catch {
        setStatus({ type: 'error', message: 'Failed to load content library.' });
      } finally {
        setLoading(false);
      }
    };

    loadContents();
  }, []);

  const selectedContent = useMemo(
    () => contents.find((item) => item.contentId === selectedId) || null,
    [contents, selectedId]
  );

  const handleGenerateTranscript = async (url) => {
    if (!validateUrl(url) || !url.includes('youtu')) {
      setStatus({ type: 'error', message: 'Please provide a valid YouTube URL.' });
      return false;
    }

    setLoading(true);
    setStatus({ type: 'loading', message: 'Extracting transcript from YouTube URL...' });

    try {
      const result = await apiClient.generateTranscriptFromUrl(url);
      const newItem = result?.content;
      if (!newItem) throw new Error('No transcript content returned.');

      setContents((prev) => [newItem, ...prev]);
      setSelectedId(newItem.contentId);
      setStatus({ type: 'success', message: 'Transcript added to Content Library.' });
      return true;
    } catch {
      setStatus({ type: 'error', message: 'Transcript generation failed. Please try again.' });
      return false;
    } finally {
      setLoading(false);
    }
  };

  const executeDeleteContent = (contentId) => {
    const target = contents.find((item) => item.contentId === contentId);
    if (!target) return;

    const removeContent = async () => {
      try {
        setLoading(true);
        await apiClient.deleteContent(contentId);

        let nextSelectedId = selectedId;
        setContents((prev) => {
          const remaining = prev.filter((item) => item.contentId !== contentId);
          if (selectedId === contentId) {
            nextSelectedId = remaining[0]?.contentId || null;
          }
          return remaining;
        });

        if (selectedId === contentId) {
          setSelectedId(nextSelectedId);
        }

        setStatus({ type: 'success', message: 'Content deleted successfully.' });
      } catch {
        setStatus({ type: 'error', message: 'Unable to delete content.' });
      } finally {
        setLoading(false);
      }
    };

    removeContent();
  };

  const handleDeleteContent = (contentId) => {
    const target = contents.find((item) => item.contentId === contentId);
    if (!target) return;
    setPendingDelete(target);
  };

  const handleAddTranscript = async ({ title, transcriptText }) => {
    setLoading(true);
    setStatus({ type: 'loading', message: 'Adding transcript to your library...' });

    try {
      const result = await apiClient.addTranscript({ title, transcriptText });
      const newItem = result?.content;
      if (!newItem) throw new Error('No transcript content returned.');

      setContents((prev) => [newItem, ...prev]);
      setSelectedId(newItem.contentId);
      setStatus({ type: 'success', message: 'Transcript added to Content Library.' });
      return true;
    } catch {
      setStatus({ type: 'error', message: 'Unable to add transcript. Try again.' });
      return false;
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="content-page">
      <section className="content-hero">
        <div>
          <h1>
            <span className="content-icon-badge hero">
              <Youtube size={20} />
            </span>
            Content Library
          </h1>
          <p>
            Start with YouTube URL ingestion to auto-generate transcript assets for Style DNA processing.
          </p>
        </div>
      </section>

      {status.type !== 'idle' && (
        <div className={`content-status-banner ${status.type}`}>
          {status.type === 'loading' && <LoaderCircle size={16} className="spin" />}
          {status.type === 'success' && <CheckCircle2 size={16} />}
          {status.type === 'error' && <AlertCircle size={16} />}
          <span>{status.message}</span>
        </div>
      )}

      <ContentUploader
        onGenerateTranscript={handleGenerateTranscript}
        onAddTranscript={handleAddTranscript}
        loading={loading}
      />

      <div className="content-layout-grid">
        <ContentList
          contents={contents}
          selectedId={selectedId}
          onSelect={(item) => setSelectedId(item.contentId)}
          onDelete={handleDeleteContent}
        />
        <ContentViewer content={selectedContent} />
      </div>

      {pendingDelete && (
        <div className="confirm-overlay" role="dialog" aria-modal="true" aria-labelledby="delete-title">
          <div className="confirm-card">
            <h3 id="delete-title">Delete Content?</h3>
            <p>
              This will remove <strong>{pendingDelete.title}</strong> from your Content Library.
            </p>
            <div className="confirm-actions">
              <button
                type="button"
                className="confirm-btn ghost"
                onClick={() => setPendingDelete(null)}
              >
                Cancel
              </button>
              <button
                type="button"
                className="confirm-btn danger"
                onClick={() => {
                  const contentId = pendingDelete.contentId;
                  setPendingDelete(null);
                  executeDeleteContent(contentId);
                }}
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ContentPage;
