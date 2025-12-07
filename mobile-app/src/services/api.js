import axios from 'axios';
import { API_BASE_URL, API_ENDPOINTS } from '../config/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Detect language of text
 */
export const detectLanguage = async (text) => {
  try {
    const response = await api.post(API_ENDPOINTS.DETECT, { text });
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || error.message || 'Failed to detect language',
    };
  }
};

/**
 * Translate text
 */
export const translateText = async (text, sourceLang = 'auto', targetLang = 'en') => {
  try {
    const response = await api.post(API_ENDPOINTS.TRANSLATE, {
      text,
      source_lang: sourceLang,
      target_lang: targetLang,
    });
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || error.message || 'Translation failed',
    };
  }
};

/**
 * Batch detect languages for multiple texts
 */
export const batchDetect = async (texts) => {
  try {
    const response = await api.post(API_ENDPOINTS.BATCH_DETECT, { texts });
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || error.message || 'Batch detection failed',
    };
  }
};

/**
 * Get supported languages
 */
export const getSupportedLanguages = async () => {
  try {
    const response = await api.get(API_ENDPOINTS.LANGUAGES);
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || error.message || 'Failed to fetch languages',
    };
  }
};

/**
 * Health check
 */
export const healthCheck = async () => {
  try {
    const response = await api.get(API_ENDPOINTS.HEALTH);
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || error.message || 'API is not available',
    };
  }
};

