# Language Detection Mobile App

A cross-platform mobile application (iOS & Android) for language detection and translation, built with React Native and Expo.

## Features

- 🔍 **Language Detection**: Detect the language of any text with confidence scores
- 🌐 **Translation**: Translate text between 500+ languages
- 📊 **Batch Analysis**: Analyze multiple texts at once
- 📜 **History**: View your detection and translation history
- 🎨 **Modern UI**: Beautiful, intuitive interface with gradient designs

## Prerequisites

Before you begin, ensure you have:

- Node.js (v16 or higher)
- npm or yarn
- Expo CLI (`npm install -g expo-cli`)
- Python 3.8+ (for the backend API)
- iOS Simulator (for Mac) or Android Emulator

## Setup Instructions

### 1. Backend API Setup

First, set up the FastAPI backend server:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Make sure your model files exist:
# - language_detection_model.pkl
# - count_vectorizer.pkl
# - label_encoder.pkl

# Start the API server
python api_server.py
```

The API will run on `http://localhost:8000`

**For mobile devices/emulators:**
- **iOS Simulator**: Use `http://localhost:8000`
- **Android Emulator**: Use `http://10.0.2.2:8000`
- **Physical Device**: Use your computer's IP address (e.g., `http://192.168.1.100:8000`)

### 2. Mobile App Setup

```bash
# Navigate to mobile app directory
cd mobile-app

# Install dependencies
npm install

# Update API configuration
# Edit mobile-app/src/config/api.js and set API_BASE_URL to your backend URL
```

### 3. Configure API URL

Edit `mobile-app/src/config/api.js`:

```javascript
export const API_BASE_URL = __DEV__ 
  ? 'http://localhost:8000'  // iOS Simulator
  : 'http://10.0.2.2:8000';  // Android Emulator

// For physical devices, use your computer's IP:
// 'http://192.168.1.100:8000'
```

### 4. Run the Mobile App

```bash
# Start Expo development server
npm start

# Or run on specific platform
npm run ios      # iOS Simulator
npm run android  # Android Emulator
npm run web      # Web browser
```

## Project Structure

```
mobile-app/
├── App.js                 # Main app component with navigation
├── app.json              # Expo configuration
├── package.json          # Dependencies
├── babel.config.js       # Babel configuration
└── src/
    ├── config/
    │   └── api.js        # API configuration
    ├── services/
    │   └── api.js        # API service functions
    ├── screens/
    │   ├── DetectionScreen.js    # Language detection screen
    │   ├── TranslationScreen.js  # Translation screen
    │   ├── BatchScreen.js        # Batch analysis screen
    │   └── HistoryScreen.js      # History screen
    ├── theme/
    │   └── theme.js      # App theme configuration
    └── utils/
        └── history.js    # History storage utilities
```

## API Endpoints

The backend API provides the following endpoints:

- `POST /detect` - Detect language of text
- `POST /translate` - Translate text
- `POST /batch-detect` - Batch language detection
- `GET /languages` - Get supported languages
- `GET /health` - Health check

## Features in Detail

### Language Detection
- Enter text and get instant language detection
- View confidence scores and top 5 language probabilities
- Quick example texts for testing

### Translation
- Auto-detect source language or manually select
- Translate to 500+ languages
- View translation history

### Batch Analysis
- Analyze multiple texts at once (one per line)
- View results for all texts in a single view
- Useful for processing large amounts of text

### History
- View all your detection and translation history
- Clear history when needed
- Organized by type (detection/translation)

## Troubleshooting

### API Connection Issues

1. **iOS Simulator**: Make sure you're using `localhost` or `127.0.0.1`
2. **Android Emulator**: Use `10.0.2.2` instead of `localhost`
3. **Physical Device**: 
   - Find your computer's IP address: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
   - Make sure your phone and computer are on the same network
   - Update `API_BASE_URL` in `src/config/api.js`

### Model Not Loading

- Ensure all model files exist in the project root:
  - `language_detection_model.pkl`
  - `count_vectorizer.pkl`
  - `label_encoder.pkl`
- Run `python train_model.py` if files are missing

### Expo Issues

- Clear cache: `expo start -c`
- Reinstall dependencies: `rm -rf node_modules && npm install`

## Building for Production

### iOS

```bash
# Build for iOS
expo build:ios

# Or use EAS Build
eas build --platform ios
```

### Android

```bash
# Build for Android
expo build:android

# Or use EAS Build
eas build --platform android
```

## Dependencies

### Mobile App
- React Native
- Expo
- React Navigation
- React Native Paper (UI components)
- Axios (HTTP client)
- Expo Linear Gradient

### Backend
- FastAPI
- Uvicorn
- scikit-learn
- joblib
- deep-translator

## License

This project is part of the Language Detection Using Natural Language Processing project.

## Support

For issues or questions, please check:
1. API server logs
2. Expo development server logs
3. Mobile app console logs

## Next Steps

- [ ] Add offline mode with local model inference
- [ ] Implement user authentication
- [ ] Add favorites/bookmarks
- [ ] Export history to file
- [ ] Add more language examples
- [ ] Improve error handling
- [ ] Add loading animations
- [ ] Implement push notifications

