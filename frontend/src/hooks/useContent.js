import { useState, useEffect } from 'react';
import apiClient from '../services/api';

const useContent = () => {
  const [contents, setContents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchContents();
  }, []);

  const fetchContents = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getContentList();
      setContents(data.contents || []);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  const uploadContent = async (file) => {
    try {
      setLoading(true);
      const result = await apiClient.uploadContent(file);
      setContents([result.content, ...contents]);
      return result;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    contents,
    loading,
    error,
    uploadContent,
    refreshContents: fetchContents,
  };
};

export default useContent;
