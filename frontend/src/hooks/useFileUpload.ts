import { useState } from 'react';
import { createFile } from '../lib/api/files';

export function useFileUpload() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const upload = async (title: string, file: File, onSuccess: () => void) => {
    if (!title.trim() || !file) {
      setError('Укажите название и выберите файл');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    const formData = new FormData();
    formData.append('title', title.trim());
    formData.append('file', file);

    try {
      await createFile(formData);
      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Не удалось загрузить файл');
    } finally {
      setIsSubmitting(false);
    }
  };

  return { isSubmitting, error, upload, clearError: () => setError(null) };
}