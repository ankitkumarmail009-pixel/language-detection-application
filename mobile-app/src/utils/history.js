// History storage using AsyncStorage
// Fallback to in-memory storage if AsyncStorage is not available

const HISTORY_KEY = '@language_detector_history';
const MAX_HISTORY_ITEMS = 100;

// In-memory fallback storage
let historyStorage = [];

// Try to import AsyncStorage (available in React Native)
let AsyncStorage = null;
try {
  AsyncStorage = require('@react-native-async-storage/async-storage').default;
} catch (e) {
  console.log('AsyncStorage not available, using in-memory storage');
}

/**
 * Save an item to history
 */
export const saveToHistory = async (item) => {
  try {
    const history = await getHistory();
    const newHistory = [item, ...history].slice(0, MAX_HISTORY_ITEMS);
    
    if (AsyncStorage) {
      await AsyncStorage.setItem(HISTORY_KEY, JSON.stringify(newHistory));
    } else {
      historyStorage = newHistory;
    }
  } catch (error) {
    console.error('Error saving to history:', error);
  }
};

/**
 * Get history items
 */
export const getHistory = async () => {
  try {
    if (AsyncStorage) {
      const stored = await AsyncStorage.getItem(HISTORY_KEY);
      return stored ? JSON.parse(stored) : [];
    } else {
      return historyStorage;
    }
  } catch (error) {
    console.error('Error getting history:', error);
    return [];
  }
};

/**
 * Clear history
 */
export const clearHistory = async () => {
  try {
    if (AsyncStorage) {
      await AsyncStorage.removeItem(HISTORY_KEY);
    } else {
      historyStorage = [];
    }
  } catch (error) {
    console.error('Error clearing history:', error);
  }
};

