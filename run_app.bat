@echo off
cd /d "%~dp0"
echo Starting Streamlit app...
echo.
python -m streamlit run app.py
pause

