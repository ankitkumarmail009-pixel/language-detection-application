"""
Script to add languages from train.csv to the language detection dataset.
Converts train.csv format (labels, text) to the required format (Language, Text).
"""

import pandas as pd
import os
import sys

# Language code to name mapping
LANGUAGE_CODE_MAP = {
    'en': 'English', 'fr': 'French', 'es': 'Spanish', 'de': 'German',
    'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'nl': 'Dutch',
    'sv': 'Swedish', 'tr': 'Turkish', 'el': 'Greek', 'da': 'Danish',
    'hi': 'Hindi', 'ar': 'Arabic', 'ta': 'Tamil', 'ml': 'Malayalam',
    'kn': 'Kannada', 'ja': 'Japanese', 'zh': 'Chinese', 'ko': 'Korean',
    'pl': 'Polish', 'cs': 'Czech', 'ro': 'Romanian', 'hu': 'Hungarian',
    'fi': 'Finnish', 'no': 'Norwegian', 'uk': 'Ukrainian', 'bg': 'Bulgarian',
    'th': 'Thai', 'vi': 'Vietnamese', 'id': 'Indonesian', 'ms': 'Malay',
    'ur': 'Urdu', 'sw': 'Swahili', 'he': 'Hebrew', 'fa': 'Persian',
    'ps': 'Pashto', 'ku': 'Kurdish', 'am': 'Amharic', 'af': 'Afrikaans',
    'zu': 'Zulu', 'xh': 'Xhosa', 'yo': 'Yoruba', 'ha': 'Hausa'
}

def load_train_csv(file_path='train.csv'):
    """Load the train.csv file."""
    try:
        print(f"Loading {file_path}...")
        df = pd.read_csv(file_path, encoding='utf-8')
        print(f"[OK] Loaded: {len(df)} samples, {df.shape[1]} columns")
        print(f"  Columns: {df.columns.tolist()}")
        return df
    except Exception as e:
        print(f"[ERROR] Error loading {file_path}: {e}")
        return None

def convert_train_to_detection_format(df):
    """
    Convert train.csv format to language detection format.
    train.csv has: labels, text
    Detection needs: Language, Text
    Also maps language codes to full names.
    """
    # Check if required columns exist
    if 'labels' not in df.columns or 'text' not in df.columns:
        print("[ERROR] train.csv must have 'labels' and 'text' columns")
        print(f"  Found columns: {df.columns.tolist()}")
        return None
    
    # Map language codes to names
    def map_language_code(code):
        """Map language code to full name."""
        if pd.isna(code):
            return None
        code_str = str(code).strip().lower()
        # If it's already a full name, return as is
        if code_str in LANGUAGE_CODE_MAP.values():
            return code_str
        # Otherwise, try to map from code
        return LANGUAGE_CODE_MAP.get(code_str, code_str.title())
    
    # Create new dataframe with correct column names
    detection_df = pd.DataFrame({
        'Text': df['text'],
        'Language': df['labels'].apply(map_language_code)
    })
    
    # Remove any rows with missing data
    detection_df = detection_df.dropna()
    
    print(f"[OK] Converted format: {len(detection_df)} samples")
    
    # Show mapping info
    unique_codes = df['labels'].unique()
    mapped_names = detection_df['Language'].unique()
    print(f"[INFO] Mapped {len(unique_codes)} language codes to {len(mapped_names)} language names")
    
    return detection_df

def merge_with_existing_dataset(new_df, existing_path='Language Detection.csv'):
    """Merge new data with existing dataset."""
    if os.path.exists(existing_path):
        print(f"\nLoading existing dataset: {existing_path}")
        existing_df = pd.read_csv(existing_path, encoding='utf-8')
        print(f"[OK] Existing dataset: {len(existing_df)} samples, {existing_df['Language'].nunique()} languages")
        
        # Show existing languages
        existing_langs = set(existing_df['Language'].unique())
        new_langs = set(new_df['Language'].unique())
        
        print(f"\nExisting languages: {len(existing_langs)}")
        print(f"New languages: {len(new_langs)}")
        
        # Find languages that are new
        truly_new_langs = new_langs - existing_langs
        if truly_new_langs:
            print(f"\n[INFO] New languages to be added: {sorted(truly_new_langs)}")
        else:
            print("\n[WARN] All languages in train.csv already exist in dataset")
            print("  They will be added anyway (duplicates allowed)")
        
        # Merge datasets
        merged_df = pd.concat([existing_df, new_df], ignore_index=True)
        print(f"\n[OK] Merged dataset: {len(merged_df)} samples, {merged_df['Language'].nunique()} languages")
        
        return merged_df
    else:
        print(f"[WARN] {existing_path} not found. Creating new dataset.")
        return new_df

def show_statistics(df):
    """Show statistics about the dataset."""
    print("\n" + "="*60)
    print("DATASET STATISTICS")
    print("="*60)
    print(f"Total samples: {len(df)}")
    print(f"Total languages: {df['Language'].nunique()}")
    
    lang_counts = df['Language'].value_counts().sort_index()
    print(f"\nLanguage distribution (top 20):")
    for lang, count in lang_counts.head(20).items():
        print(f"  {lang:20s}: {count:6d} samples")
    
    if len(lang_counts) > 20:
        print(f"  ... and {len(lang_counts) - 20} more languages")
    
    print("="*60)

def main():
    """Main function."""
    print("="*60)
    print("ADD LANGUAGES FROM TRAIN.CSV")
    print("="*60)
    
    # Step 1: Load train.csv
    train_df = load_train_csv('train.csv')
    if train_df is None:
        return
    
    # Step 2: Convert format
    print("\nConverting format...")
    detection_df = convert_train_to_detection_format(train_df)
    if detection_df is None:
        return
    
    # Show what languages are in train.csv
    print(f"\nLanguages in train.csv: {detection_df['Language'].nunique()}")
    lang_counts = detection_df['Language'].value_counts()
    print("\nSample distribution:")
    for lang, count in lang_counts.head(10).items():
        print(f"  {lang:20s}: {count:6d} samples")
    if len(lang_counts) > 10:
        print(f"  ... and {len(lang_counts) - 10} more languages")
    
    # Step 3: Merge with existing dataset
    print("\n" + "="*60)
    merged_df = merge_with_existing_dataset(detection_df)
    
    # Step 4: Show statistics
    show_statistics(merged_df)
    
    # Step 5: Ask for confirmation (or use command line argument)
    print("\n" + "="*60)
    
    # Check if --yes flag is provided
    auto_save = '--yes' in sys.argv or '-y' in sys.argv
    
    if auto_save:
        response = 'yes'
        print("[INFO] Auto-saving (--yes flag provided)")
    else:
        try:
            response = input("\nSave merged dataset to 'Language Detection.csv'? (yes/no): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n[WARN] No input available. Use --yes flag for automatic saving.")
            print("  Example: python add_from_train_csv.py --yes")
            return
    
    if response in ['yes', 'y']:
        output_path = 'Language Detection.csv'
        merged_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\n[OK] Dataset saved to {output_path}")
        print(f"  Total samples: {len(merged_df)}")
        print(f"  Total languages: {merged_df['Language'].nunique()}")
        print("\n[INFO] Next step: Run 'python train_model.py' to retrain the model")
    else:
        print("\n[WARN] Dataset not saved. Exiting...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[WARN] Interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()

