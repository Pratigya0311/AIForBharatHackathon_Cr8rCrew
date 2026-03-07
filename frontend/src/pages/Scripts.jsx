import React, { useMemo, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Editor from '../components/ScriptEditor/Editor';
import { mockScripts } from '../data/mockData';

const ScriptsPage = () => {
  const location = useLocation();
  const selectedTrend = location.state?.selectedTrend || null;

  const scripts = useMemo(() => {
    if (!selectedTrend) return mockScripts;

    const trendBasedScript = {
      ...mockScripts[0],
      scriptId: `trend-${selectedTrend.trendId}`,
      title: `Script Draft - ${selectedTrend.title}`,
      status: 'draft',
    };

    return [trendBasedScript, ...mockScripts];
  }, [selectedTrend]);

  const [selectedScript, setSelectedScript] = useState(() =>
    selectedTrend
      ? {
          ...mockScripts[0],
          scriptId: `trend-${selectedTrend.trendId}`,
          title: `Script Draft - ${selectedTrend.title}`,
          status: 'draft',
        }
      : mockScripts[0]
  );

  const handleScriptChange = (updatedScript) => {
    setSelectedScript(updatedScript);
  };

  return (
    <div className="scripts-page">
      <h1>My Scripts</h1>
      {selectedTrend && (
        <p className="scripts-subtitle">
          Generated from trend: <strong>{selectedTrend.title}</strong>
        </p>
      )}
      <div className="scripts-list">
        {scripts.map((script) => (
          <div
            key={script.scriptId}
            className={`script-item ${selectedScript.scriptId === script.scriptId ? 'active' : ''}`}
            onClick={() => setSelectedScript(script)}
          >
            <h3>{script.title}</h3>
            <p>{script.metadata.estimatedDuration} • {script.language.toUpperCase()}</p>
          </div>
        ))}
      </div>
      <Editor script={selectedScript} onChange={handleScriptChange} />
    </div>
  );
};

export default ScriptsPage;
