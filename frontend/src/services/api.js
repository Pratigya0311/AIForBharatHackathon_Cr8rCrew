// API client for backend communication
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://api.creatorai.com';

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
    const formData = new FormData();
    formData.append('file', file);
    return this.request('/api/v1/content/upload', {
      method: 'POST',
      body: formData,
      headers: {}, // Let browser set Content-Type for FormData
    });
  }

  async getContentList() {
    return this.request('/api/v1/content/list');
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
