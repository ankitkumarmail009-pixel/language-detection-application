# How to Run the Streamlit App

## Quick Start

Open a terminal/command prompt in this directory and run:

```bash
python -m streamlit run app.py
```

**Note:** Use `python -m streamlit` instead of just `streamlit` if you get a "streamlit is not recognised" error.

## What to Expect

1. The app will start and show output like:
   ```
   You can now view your Streamlit app in your browser.
   
   Local URL: http://localhost:8501
   Network URL: http://192.168.x.x:8501
   ```

2. Your browser should automatically open to `http://localhost:8501`

3. If the browser doesn't open automatically, copy the Local URL from the terminal and paste it into your browser

## Troubleshooting

- **Port 8501 already in use**: Streamlit will automatically try the next available port (8502, 8503, etc.)
- **Module not found errors**: Make sure all dependencies are installed: `pip install -r requirements.txt`
- **Model files not found**: Make sure you've run the notebook to generate the `.pkl` files

## Alternative: Use the Batch File

On Windows, you can also double-click `run_app.bat` to start the app.

