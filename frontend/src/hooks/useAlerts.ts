import { useEffect, useState } from 'react';
import { getAlerts } from '../lib/api/alerts';
import type { AlertItem } from '../lib/api/types';

export function useAlerts() {
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadAlerts = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getAlerts();
      setAlerts(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Не удалось загрузить алерты');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadAlerts();
  }, []);

  return { alerts, isLoading, error, refetch: loadAlerts };
}