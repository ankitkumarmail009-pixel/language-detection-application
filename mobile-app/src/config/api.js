/**
 * API Configuration
 * Update API_BASE_URL to point to your backend server
 * For local development: 'http://localhost:8000'
 * For production: 'https://your-api-domain.com'
 */

// Change this to your API server URL
export const API_BASE_URL = __DEV__ 
  ? 'http://localhost:8000'  // For iOS simulator, use localhost
  : 'http://10.0.2.2:8000';  // For Android emulator, use 10.0.2.2

// For physical devices, use your computer's IP address:
// Example: 'http://192.168.1.100:8000'

export const API_ENDPOINTS = {
  DETECT: '/detect',
  TRANSLATE: '/translate',
  BATCH_DETECT: '/batch-detect',
  LANGUAGES: '/languages',
  HEALTH: '/health',
};

