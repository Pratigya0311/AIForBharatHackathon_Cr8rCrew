import React, { useState } from 'react';
import Editor from '../components/ScriptEditor/Editor';
import { mockScripts } from '../data/mockData';

const ScriptsPage = () => {
  const [selectedScript, setSelectedScript] = useState(mockScripts[0]);

  const handleScriptChange = (updatedScript) => {
    setSelectedScript(updatedScript);
  };

  return (
    <div className="scripts-page">
      <h1>My Scripts</h1>
      <div className="scripts-list">
        {mockScripts.map((script) => (
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
