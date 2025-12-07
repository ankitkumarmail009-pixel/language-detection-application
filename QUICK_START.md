# Quick Start Guide - Mobile App

Get your Language Detection mobile app up and running in minutes!

## Step 1: Start the Backend API

Open a terminal in the project root and run:

**Windows:**
```bash
start_api.bat
```

**Mac/Linux:**
```bash
chmod +x start_api.sh
./start_api.sh
```

**Or manually:**
```bash
python api_server.py
```

The API will start on `http://localhost:8000`

## Step 2: Set Up Mobile App

Open a new terminal and navigate to the mobile app:

```bash
cd mobile-app
npm install
```

## Step 3: Configure API URL

Edit `mobile-app/src/config/api.js`:

- **iOS Simulator**: Use `http://localhost:8000`
- **Android Emulator**: Use `http://10.0.2.2:8000`
- **Physical Device**: Use your computer's IP (e.g., `http://192.168.1.100:8000`)

To find your IP:
- **Windows**: `ipconfig` (look for IPv4 Address)
- **Mac/Linux**: `ifconfig` or `ip addr`

## Step 4: Run the App

```bash
npm start
```

Then:
- Press `i` for iOS Simulator
- Press `a` for Android Emulator
- Scan QR code with Expo Go app on your phone

## Troubleshooting

### "Cannot connect to API"
- Make sure the backend is running
- Check the API URL in `src/config/api.js`
- For physical devices, ensure phone and computer are on the same WiFi

### "Model not loaded"
- Make sure you've trained the model first
- Check that these files exist:
  - `language_detection_model.pkl`
  - `count_vectorizer.pkl`
  - `label_encoder.pkl`

### "Module not found"
- Run `npm install` again in the `mobile-app` directory
- Clear cache: `expo start -c`

## Testing

1. Open the app
2. Go to "Detect" tab
3. Type: "Hello, how are you?"
4. Tap "Detect Language"
5. You should see: **English** with high confidence!

## Next Steps

- Try the Translation feature
- Test Batch Analysis with multiple texts
- Check your History

Enjoy your mobile language detection app! 🎉

