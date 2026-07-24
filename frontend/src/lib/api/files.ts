import { apiRequest } from './client';
import type { FileItem } from './types';

export async function getFiles() {
  return apiRequest<FileItem[]>('/files');
}

export async function createFile(formData: FormData) {
  return apiRequest<FileItem>('/files', {
    method: 'POST',
    body: formData,
  });
}