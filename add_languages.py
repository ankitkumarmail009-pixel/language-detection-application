"""
Script to add new languages to the language detection dataset.
This script helps you add new languages by either:
1. Adding data from a CSV file
2. Adding data manually
3. Generating sample data using web scraping (optional)
"""

import pandas as pd
import os
import sys
from pathlib import Path

def load_existing_dataset():
    """Load the existing language detection dataset."""
    dataset_path = 'Language Detection.csv'
    if os.path.exists(dataset_path):
        df = pd.read_csv(dataset_path)
        print(f"[OK] Loaded existing dataset: {len(df)} samples, {df['Language'].nunique()} languages")
        return df
    else:
        print(f"[WARN] Dataset not found. Creating new dataset...")
        return pd.DataFrame(columns=['Text', 'Language'])

def add_language_from_csv(df, csv_path, language_name):
    """
    Add language data from a CSV file.
    CSV should have a 'Text' column with text samples.
    """
    try:
        new_data = pd.read_csv(csv_path)
        
        # Check if 'Text' column exists
        if 'Text' not in new_data.columns:
            print(f"[ERROR] CSV file must have a 'Text' column")
            return df
        
        # Add language column
        new_data['Language'] = language_name
        
        # Keep only Text and Language columns
        new_data = new_data[['Text', 'Language']]
        
        # Combine with existing data
        df = pd.concat([df, new_data], ignore_index=True)
        
        print(f"[OK] Added {len(new_data)} samples for {language_name}")
        return df
    
    except Exception as e:
        print(f"[ERROR] Error loading CSV: {e}")
        return df

def add_language_manually(df, language_name, texts):
    """
    Add language data manually from a list of text samples.
    """
    new_data = pd.DataFrame({
        'Text': texts,
        'Language': [language_name] * len(texts)
    })
    
    df = pd.concat([df, new_data], ignore_index=True)
    print(f"[OK] Added {len(texts)} samples for {language_name}")
    return df

def add_language_from_file(df, file_path, language_name):
    """
    Add language data from a text file (one sample per line).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            texts = [line.strip() for line in f if line.strip()]
        
        return add_language_manually(df, language_name, texts)
    
    except Exception as e:
        print(f"[ERROR] Error reading file: {e}")
        return df

def save_dataset(df, output_path='Language Detection.csv'):
    """Save the updated dataset."""
    df.to_csv(output_path, index=False)
    print(f"[OK] Dataset saved to {output_path}")
    print(f"  Total samples: {len(df)}")
    print(f"  Total languages: {df['Language'].nunique()}")
    print(f"  Languages: {', '.join(sorted(df['Language'].unique()))}")

def show_statistics(df):
    """Show statistics about the current dataset."""
    print("\n" + "="*60)
    print("DATASET STATISTICS")
    print("="*60)
    print(f"Total samples: {len(df)}")
    print(f"Total languages: {df['Language'].nunique()}")
    print("\nLanguage distribution:")
    lang_counts = df['Language'].value_counts().sort_index()
    for lang, count in lang_counts.items():
        print(f"  {lang:20s}: {count:5d} samples")
    print("="*60)

def main():
    """Main function to add languages interactively."""
    print("="*60)
    print("ADD LANGUAGES TO LANGUAGE DETECTION DATASET")
    print("="*60)
    
    # Load existing dataset
    df = load_existing_dataset()
    
    if len(df) > 0:
        show_statistics(df)
    
    print("\nOptions:")
    print("1. Add language from CSV file")
    print("2. Add language from text file (one sample per line)")
    print("3. Add language manually (enter text samples)")
    print("4. Show current statistics")
    print("5. Save and exit")
    print("6. Exit without saving")
    
    while True:
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            csv_path = input("Enter path to CSV file: ").strip()
            language_name = input("Enter language name: ").strip()
            df = add_language_from_csv(df, csv_path, language_name)
        
        elif choice == '2':
            file_path = input("Enter path to text file: ").strip()
            language_name = input("Enter language name: ").strip()
            df = add_language_from_file(df, file_path, language_name)
        
        elif choice == '3':
            language_name = input("Enter language name: ").strip()
            print("Enter text samples (one per line, type 'DONE' on a new line to finish):")
            texts = []
            while True:
                text = input()
                if text.strip().upper() == 'DONE':
                    break
                if text.strip():
                    texts.append(text.strip())
            
            if texts:
                df = add_language_manually(df, language_name, texts)
            else:
                print("[WARN] No text samples entered")
        
        elif choice == '4':
            show_statistics(df)
        
        elif choice == '5':
            save_dataset(df)
            print("\n[OK] Dataset updated! Now run 'python train_model.py' to retrain the model.")
            break
        
        elif choice == '6':
            print("Exiting without saving...")
            break
        
        else:
            print("[ERROR] Invalid option. Please select 1-6.")

if __name__ == "__main__":
    main()

