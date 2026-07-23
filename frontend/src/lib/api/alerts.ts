import { apiRequest } from './client';
import type { AlertItem } from './types';

export async function getAlerts() {
  return apiRequest<AlertItem[]>('/alerts');
}