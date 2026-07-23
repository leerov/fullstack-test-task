import { useEffect, useState } from 'react';
import { getFiles } from '../lib/api/files';
import type { FileItem } from '../lib/api/types';

export function useFiles() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadFiles = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getFiles();
      setFiles(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Не удалось загрузить файлы');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadFiles();
    const interval = setInterval(loadFiles, 5000);
    return () => clearInterval(interval);
  }, []);

  return { files, isLoading, error, refetch: loadFiles };
}