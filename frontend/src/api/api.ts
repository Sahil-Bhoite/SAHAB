import axios from 'axios';
import { ChatRequest, ChatResponse } from '../types';

// Assuming backend runs on 8000. In prod, this should be env var.
const API_URL = 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_URL,
});

export const sendChat = async (request: ChatRequest): Promise<ChatResponse> => {
  // Fallback for non-streaming or if needed (though backend now streams)
  // Ideally we should deprecate this or make it consume the stream
  const response = await api.post<ChatResponse>('/chat', request);
  return response.data;
};

export const sendChatStream = async (
  request: ChatRequest,
  onChunk: (chunk: string) => void
): Promise<void> => {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.body) throw new Error('No response body');

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, { stream: true });
    onChunk(chunk);
  }
};
