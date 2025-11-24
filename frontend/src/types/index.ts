export type Role = 'user' | 'assistant';

export interface Message {
  role: Role;
  content: string;
}

export interface ChatRequest {
  prompt: string;
  language: string;
  history: Message[];
}

export interface ChatResponse {
  answer: string;
  language: string;
  sources?: string[];
}
