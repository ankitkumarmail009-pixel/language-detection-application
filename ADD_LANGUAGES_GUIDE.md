# Guide: Adding More Languages for Detection

This guide explains how to add new languages to the language detection model.

## Overview

The language detection model is trained on a CSV dataset (`Language Detection.csv`) with two columns:
- **Text**: Sample text in the language
- **Language**: The language name

Currently, the model supports **17 languages**. You can add more languages by adding training data.

## Methods to Add Languages

### Method 1: Using the Interactive Script (Recommended)

The easiest way to add languages is using the `add_languages.py` script:

```bash
python add_languages.py
```

This script provides an interactive menu to:
1. Add language from CSV file
2. Add language from text file (one sample per line)
3. Add language manually (enter text samples)
4. View current statistics
5. Save and exit

**Example:**
```bash
python add_languages.py
# Select option 2 (Add from text file)
# Enter path: japanese_samples.txt
# Enter language name: Japanese
# Save and exit
```

### Method 2: Generate Samples from Wikipedia

Use the `generate_language_samples.py` script to automatically fetch sample text from Wikipedia:

```bash
python generate_language_samples.py
```

**Example:**
```bash
python generate_language_samples.py
# Enter language name: Japanese
# Enter Wikipedia code: ja
# Enter number of samples: 100
# This creates: Japanese_samples.csv
```

Then add the generated samples:
```bash
python add_languages.py
# Select option 1 (Add from CSV)
# Enter path: Japanese_samples.csv
# Enter language name: Japanese
```

### Method 3: Manual CSV Editing

You can manually edit `Language Detection.csv`:

1. Open `Language Detection.csv` in Excel or a text editor
2. Add new rows with:
   - **Text**: Sample text in the new language
   - **Language**: Name of the language (must be consistent)
3. Save the file
4. Retrain the model

**CSV Format:**
```csv
Text,Language
"Hello, how are you?",English
"Bonjour, comment allez-vous?",French
"こんにちは、元気ですか？",Japanese
```

## Recommended Number of Samples

For best accuracy:
- **Minimum**: 50-100 samples per language
- **Recommended**: 200-500 samples per language
- **Optimal**: 500+ samples per language

Languages with fewer than 50 samples may have lower detection accuracy.

## Language Naming

**Important**: Use consistent language names. The model is case-sensitive.

**Good examples:**
- `English`, `French`, `Spanish`, `Japanese`, `Chinese`
- `Portuguese` (not `Portugeese`)
- `Swedish` (not `Sweedish`)

**Avoid:**
- Inconsistent naming (e.g., mixing `English` and `english`)
- Typos in language names
- Special characters in language names

## Retraining the Model

After adding new languages, you **must** retrain the model:

```bash
python train_model.py
```

This will:
1. Load the updated dataset
2. Preprocess the text
3. Train a new model with all languages
4. Save the updated model files

## Testing New Languages

After retraining, test the new languages:

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Try detecting text in the new language

3. Check the confidence scores - they should be reasonable (>50% for correct detection)

## Tips for Better Accuracy

1. **Diverse Text Samples**: Include various types of text:
   - News articles
   - Conversations
   - Technical text
   - Literary text
   - Short phrases
   - Long paragraphs

2. **Character Sets**: 
   - For non-Latin scripts (Japanese, Chinese, Arabic, etc.), ensure you have enough samples
   - The current preprocessing removes non-Latin characters, which may affect accuracy for these languages

3. **Balanced Dataset**: Try to have similar numbers of samples for each language

4. **Quality over Quantity**: Better to have 100 good, diverse samples than 1000 repetitive samples

## Example: Adding Japanese

```bash
# Step 1: Generate samples
python generate_language_samples.py
# Enter: Japanese
# Enter: ja
# Enter: 200

# Step 2: Add to dataset
python add_languages.py
# Select option 1
# Enter: Japanese_samples.csv
# Enter: Japanese
# Save and exit

# Step 3: Retrain model
python train_model.py

# Step 4: Test
streamlit run app.py
```

## Troubleshooting

**Problem**: Model accuracy is low for new language
- **Solution**: Add more training samples (200+ recommended)

**Problem**: Language not detected correctly
- **Solution**: 
  - Check language name spelling matches exactly
  - Ensure you have enough diverse samples
  - Retrain the model after adding samples

**Problem**: Error during training
- **Solution**: 
  - Check CSV format (must have Text and Language columns)
  - Ensure no empty rows
  - Check for special characters in language names

**Problem**: Wikipedia samples not working
- **Solution**: 
  - Check internet connection
  - Verify language code is correct
  - Try manual method instead

## Current Supported Languages

The model currently supports these 17 languages:
- English
- French
- Spanish
- German
- Italian
- Portuguese
- Russian
- Dutch
- Swedish
- Turkish
- Greek
- Danish
- Hindi
- Arabic
- Tamil
- Malayalam
- Kannada

After adding new languages, this list will expand!

## Need Help?

If you encounter issues:
1. Check the error messages carefully
2. Verify your CSV format
3. Ensure you have enough samples
4. Try retraining the model

Good luck adding new languages! 🌍

