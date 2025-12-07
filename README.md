# Language Detection Using Natural Language Processing

A machine learning project that automatically detects the language of text samples from 17 different languages using NLP techniques.

## Project Overview

This project implements a multilingual language detection model using:
- **Bag-of-Words** and **TF-IDF** vectorization
- **Label Encoding** for language classification
- **Multinomial Naive Bayes** and other ML classifiers
- Comprehensive evaluation with confusion matrices and accuracy metrics

## Features

- ✅ Exploratory Data Analysis (EDA) with visualizations
- ✅ Text preprocessing and cleaning
- ✅ Feature engineering using CountVectorizer and TfidfVectorizer
- ✅ Multiple classifier comparison (Naive Bayes, Logistic Regression, SVM, Random Forest)
- ✅ Model evaluation with confusion matrix visualization
- ✅ Language prediction function for custom text inputs
- ✅ Model persistence (save/load functionality)
- ✅ Streamlit web application for interactive language detection

## Dataset

The project uses the [Language Detection Dataset from Kaggle](https://www.kaggle.com/basilb2s/language-detection) containing text samples across 17 languages:

- English
- Malayalam
- Hindi
- Tamil
- Kannada
- French
- Spanish
- Portuguese
- Italian
- Russian
- Swedish
- Dutch
- Arabic
- Turkish
- German
- Danish
- Greek

## Installation

1. Clone the repository or download the project files.

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Download the dataset from [Kaggle](https://www.kaggle.com/basilb2s/language-detection) and place `Language Detection.csv` in the project directory.

## Usage

### Training the Model

You can train the model using either method:

**Option 1: Python Script (Recommended)**
```bash
python train_model.py
```

**Option 2: Jupyter Notebook**
1. Open the `language_detection.ipynb` notebook:
```bash
jupyter notebook language_detection.ipynb
```

2. Run all cells to:
   - Load and explore the dataset
   - Preprocess the data
   - Train the model
   - Evaluate performance
   - Make predictions

### Streamlit Web App

Run the Streamlit application for an interactive language detection interface:

```bash
streamlit run app.py
```

The web app will open in your browser where you can:
- Enter text in any language
- Get instant language detection results
- View prediction confidence scores

### Python Script

You can also use the model programmatically:

```python
import joblib
from utils import predict_language, preprocess_text

# Load saved model
model = joblib.load('language_detection_model.pkl')
vectorizer = joblib.load('count_vectorizer.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# Predict language
text = "Hello, how are you?"
predicted_lang, confidence = predict_language(text, model, vectorizer, label_encoder)
print(f"Language: {predicted_lang}, Confidence: {confidence:.2%}")
```

## Project Structure

```
.
├── language_detection.ipynb    # Main Jupyter notebook with complete implementation
├── train_model.py              # Training script to generate model files
├── app.py                      # Streamlit web application
├── utils.py                    # Helper functions and utilities
├── add_languages.py            # Script to add new languages to dataset
├── generate_language_samples.py # Script to generate samples from Wikipedia
├── ADD_LANGUAGES_GUIDE.md      # Guide for adding new languages
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── Language Detection.csv      # Dataset file (download from Kaggle)
```

## Methodology

### 1. Data Preprocessing
- Convert text to lowercase
- Remove special characters and numbers
- Clean whitespace

### 2. Feature Engineering
- **Bag-of-Words**: CountVectorizer with n-grams (1,2)
- **TF-IDF**: Term Frequency-Inverse Document Frequency vectorization

### 3. Model Training
- Train multiple classifiers and compare performance
- Use stratified train-test split (80/20)

### 4. Evaluation
- Accuracy score
- Confusion matrix visualization
- Classification report with precision, recall, and F1-score

## Results

The model achieves high accuracy in detecting languages. Typical performance:
- **Multinomial Naive Bayes**: ~95%+ accuracy
- **Logistic Regression**: ~96%+ accuracy
- **SVM**: ~97%+ accuracy
- **Random Forest**: ~98%+ accuracy

## Model Files

After training, the following files are generated:
- `language_detection_model.pkl` - Trained model
- `count_vectorizer.pkl` - Bag-of-words vectorizer
- `tfidf_vectorizer.pkl` - TF-IDF vectorizer
- `label_encoder.pkl` - Language label encoder

## Adding More Languages

You can easily add new languages to the detection model! See the detailed guide:

**[📖 ADD_LANGUAGES_GUIDE.md](ADD_LANGUAGES_GUIDE.md)**

### Quick Start

1. **Generate sample data from Wikipedia:**
   ```bash
   python generate_language_samples.py
   ```

2. **Add languages to dataset:**
   ```bash
   python add_languages.py
   ```

3. **Retrain the model:**
   ```bash
   python train_model.py
   ```

### Tools Available

- **`add_languages.py`** - Interactive script to add languages from CSV, text files, or manual input
- **`generate_language_samples.py`** - Automatically fetch sample text from Wikipedia
- **`ADD_LANGUAGES_GUIDE.md`** - Complete guide with examples and tips

## Future Improvements

- [x] Add support for more languages (tools provided!)
- [ ] Implement deep learning models (LSTM, BERT)
- [ ] Add batch prediction functionality
- [ ] Create API endpoint using Flask/FastAPI
- [ ] Improve handling of mixed-language text
- [ ] Add confidence threshold filtering

## License

This project is open source and available for educational purposes.

## References

- [Kaggle Language Detection Dataset](https://www.kaggle.com/basilb2s/language-detection)
- [scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Analytics Vidhya NLP Resources](https://www.analyticsvidhya.com/blog/category/nlp/)

## Author

Created as a portfolio project demonstrating NLP and machine learning skills.


