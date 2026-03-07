import { useState, useEffect } from 'react';
import apiClient from '../services/api';

const useScripts = () => {
  const [scripts, setScripts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchScripts();
  }, []);

  const fetchScripts = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getScripts();
      setScripts(data.scripts || []);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  const generateScript = async (scriptData) => {
    try {
      setLoading(true);
      const result = await apiClient.generateScript(scriptData);
      setScripts([result.script, ...scripts]);
      return result;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    scripts,
    loading,
    error,
    generateScript,
    refreshScripts: fetchScripts,
  };
};

export default useScripts;
