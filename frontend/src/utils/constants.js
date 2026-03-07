// Application constants

export const SCRIPT_LENGTHS = {
  SHORT: 'short',
  MEDIUM: 'medium',
  LONG: 'long',
};

export const SCRIPT_TONES = {
  CASUAL: 'casual',
  FORMAL: 'formal',
  HUMOROUS: 'humorous',
  EDUCATIONAL: 'educational',
};

export const SCRIPT_STRUCTURES = {
  EDUCATIONAL: 'educational',
  ENTERTAINMENT: 'entertainment',
  REVIEW: 'review',
  TUTORIAL: 'tutorial',
};

export const SUPPORTED_LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'hi', name: 'Hindi' },
  { code: 'ta', name: 'Tamil' },
  { code: 'te', name: 'Telugu' },
  { code: 'mr', name: 'Marathi' },
  { code: 'bn', name: 'Bengali' },
  { code: 'kn', name: 'Kannada' },
  { code: 'ml', name: 'Malayalam' },
  { code: 'gu', name: 'Gujarati' },
  { code: 'pa', name: 'Punjabi' },
];

export const FILE_TYPES = {
  ALLOWED: ['text/plain', 'application/pdf', 'application/json', 'text/csv'],
  MAX_SIZE_MB: 10,
};

export const API_ENDPOINTS = {
  CONTENT_UPLOAD: '/api/v1/content/upload',
  CONTENT_LIST: '/api/v1/content/list',
  TRENDS_LIST: '/api/v1/trends/list',
  SCRIPTS_GENERATE: '/api/v1/scripts/generate',
  SCRIPTS_LIST: '/api/v1/scripts/list',
};

export const RELEVANCE_THRESHOLD = 70;

export const NOTIFICATION_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info',
};
