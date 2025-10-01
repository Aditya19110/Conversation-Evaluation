import axios from 'axios';
import { API_BASE_URL } from '../config';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface EvaluationRequest {
  conversation: string;
  context?: string;
  facets?: string[];
}

export interface EvaluationResult {
  overall_score: number;
  confidence: number;
  facet_scores: Record<string, number>;
  reasoning: string;
}

export const evaluateConversation = async (data: EvaluationRequest): Promise<EvaluationResult> => {
  const response = await api.post('/evaluate', data);
  return response.data;
};

export const getHealthStatus = async () => {
  const response = await api.get('/health');
  return response.data;
};

export const getFacets = async () => {
  const response = await api.get('/facets');
  return response.data;
};