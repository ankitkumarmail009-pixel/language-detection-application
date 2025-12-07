@echo off
echo Starting Language Detection API Server...
echo.
echo Make sure you have:
echo 1. Installed all dependencies: pip install -r requirements.txt
echo 2. Trained the model (language_detection_model.pkl exists)
echo.
echo Starting server on http://localhost:8000
echo.
python api_server.py
pause

