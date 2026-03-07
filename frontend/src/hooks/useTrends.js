import { useState, useEffect } from 'react';
import apiClient from '../services/api';

const useTrends = () => {
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTrends();
  }, []);

  const fetchTrends = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getTrends();
      setTrends(data.trends || []);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  const refreshTrends = () => {
    fetchTrends();
  };

  return {
    trends,
    loading,
    error,
    refreshTrends,
  };
};

export default useTrends;
