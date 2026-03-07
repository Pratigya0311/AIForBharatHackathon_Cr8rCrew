import { mockContents } from '../data/mockData';

// API client for backend communication
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://api.creatorai.com';
const USE_MOCK_CONTENT_API = true;

const buildInitialMockContents = () => {
  return mockContents.map((item, index) => {
    const fallbackUrl = `https://www.youtube.com/watch?v=demo${index + 100}`;
    const transcript = [
      `This transcript was generated for ${item.title}.`,
      'The video explains practical lessons, examples, and clear creator-style storytelling.',
      'Use this content as source material to model tone, domain language, and recurring phrases.',
    ].join(' ');

    return {
      contentId: item.contentId,
      title: item.title,
      sourceType: 'youtube',
      sourceUrl: fallbackUrl,
      language: item.metadata?.language || 'en',
      wordCount: item.metadata?.wordCount || transcript.split(/\s+/).length,
      createdAt: item.uploadedAt,
      transcriptText: transcript,
    };
  });
};

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const getYouTubeId = (url) => {
  try {
    const parsed = new URL(url);
    if (parsed.hostname.includes('youtu.be')) {
      return parsed.pathname.replace('/', '');
    }
    return parsed.searchParams.get('v');
  } catch {
    return null;
  }
};

const buildTranscriptFromUrl = (url) => {
  const videoId = getYouTubeId(url) || 'unknown-video';
  const shortId = videoId.slice(0, 12);
  return [
    `Video ${shortId}: In this session we break down the topic into creator-friendly insights.`,
    'We cover why the trend matters right now, where the audience attention is shifting, and what examples perform best.',
    'Then we convert those points into hooks, key sections, and a practical call-to-action for your next video.',
  ].join(' ');
};

const buildManualTitle = (title, transcriptText) => {
  if (title && title.trim()) return title.trim();
  const preview = transcriptText.split(/\s+/).slice(0, 6).join(' ');
  return preview ? `Transcript - ${preview}` : 'Manual Transcript';
};

let MOCK_CONTENT_DB = buildInitialMockContents();

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Content endpoints
  async uploadContent(file) {
    if (USE_MOCK_CONTENT_API) {
      await sleep(300);
      const transcriptText = `Uploaded file transcript placeholder for ${file.name}`;
      const content = {
        contentId: `content_${Date.now()}`,
        title: file.name,
        sourceType: 'transcript',
        sourceUrl: '',
        language: 'en',
        wordCount: transcriptText.split(/\s+/).length,
        createdAt: Date.now(),
        transcriptText,
      };
      MOCK_CONTENT_DB = [content, ...MOCK_CONTENT_DB];
      return { content };
    }

    const formData = new FormData();
    formData.append('file', file);
    return this.request('/api/v1/content/upload', {
      method: 'POST',
      body: formData,
      headers: {}, // Let browser set Content-Type for FormData
    });
  }

  async getContentList() {
    if (USE_MOCK_CONTENT_API) {
      await sleep(200);
      return { contents: [...MOCK_CONTENT_DB] };
    }
    return this.request('/api/v1/content/list');
  }

  async generateTranscriptFromUrl(url) {
    if (USE_MOCK_CONTENT_API) {
      await sleep(900);
      if (!url || !url.includes('youtu')) {
        throw new Error('Please provide a valid YouTube URL.');
      }
      const transcriptText = buildTranscriptFromUrl(url);
      const content = {
        contentId: `content_${Date.now()}`,
        title: `YouTube Transcript - ${getYouTubeId(url) || 'New Video'}`,
        sourceType: 'youtube',
        sourceUrl: url,
        language: 'en',
        wordCount: transcriptText.split(/\s+/).length,
        createdAt: Date.now(),
        transcriptText,
      };
      MOCK_CONTENT_DB = [content, ...MOCK_CONTENT_DB];
      return { content };
    }

    return this.request('/api/v1/content/transcript', {
      method: 'POST',
      body: JSON.stringify({ url }),
    });
  }

  async addTranscript(payload) {
    if (USE_MOCK_CONTENT_API) {
      await sleep(400);
      const transcriptText = payload?.transcriptText?.trim();
      if (!transcriptText) {
        throw new Error('Transcript text is required.');
      }
      const content = {
        contentId: `content_${Date.now()}`,
        title: buildManualTitle(payload?.title || '', transcriptText),
        sourceType: 'transcript',
        sourceUrl: '',
        language: payload?.language || 'en',
        wordCount: transcriptText.split(/\s+/).length,
        createdAt: Date.now(),
        transcriptText,
      };
      MOCK_CONTENT_DB = [content, ...MOCK_CONTENT_DB];
      return { content };
    }

    return this.request('/api/v1/content/process', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  async deleteContent(contentId) {
    if (USE_MOCK_CONTENT_API) {
      await sleep(200);
      const before = MOCK_CONTENT_DB.length;
      MOCK_CONTENT_DB = MOCK_CONTENT_DB.filter((item) => item.contentId !== contentId);
      return { success: MOCK_CONTENT_DB.length < before };
    }

    return this.request(`/api/v1/content/${contentId}`, {
      method: 'DELETE',
    });
  }

  // Trend endpoints
  async getTrends() {
    return this.request('/api/v1/trends/list');
  }

  // Script endpoints
  async generateScript(data) {
    return this.request('/api/v1/scripts/generate', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getScripts() {
    return this.request('/api/v1/scripts/list');
  }
}

export default new ApiClient();
