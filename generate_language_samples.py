"""
Helper script to generate sample text data for new languages.
This script can fetch sample text from Wikipedia or other sources.
"""

import requests
import pandas as pd
import time
import random
from typing import List, Optional

def get_wikipedia_text(language_code: str, num_samples: int = 50) -> List[str]:
    """
    Fetch sample text from Wikipedia for a given language.
    
    Parameters:
    -----------
    language_code : str
        Wikipedia language code (e.g., 'en', 'fr', 'es', 'de', 'ja', 'zh')
    num_samples : int
        Number of text samples to fetch
    
    Returns:
    --------
    List[str] : List of text samples
    """
    samples = []
    
    # Common Wikipedia article titles to fetch
    common_articles = [
        'Nature', 'Science', 'Technology', 'History', 'Culture',
        'Geography', 'Mathematics', 'Physics', 'Chemistry', 'Biology',
        'Art', 'Music', 'Literature', 'Philosophy', 'Religion',
        'Politics', 'Economics', 'Education', 'Health', 'Food'
    ]
    
    base_url = f"https://{language_code}.wikipedia.org/api/rest_v1/page/summary"
    
    print(f"Fetching {num_samples} samples from {language_code}.wikipedia.org...")
    
    for i, article in enumerate(common_articles[:num_samples]):
        try:
            url = f"{base_url}/{article}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'extract' in data and data['extract']:
                    # Clean the text
                    text = data['extract'].strip()
                    if len(text) > 50:  # Only add substantial text
                        samples.append(text)
                        print(f"  [OK] Fetched sample {i+1}/{num_samples}")
            
            # Be respectful - add delay between requests
            time.sleep(0.5)
            
        except Exception as e:
            print(f"  [WARN] Error fetching {article}: {e}")
            continue
    
    return samples

def generate_sample_data(language_name: str, language_code: str, num_samples: int = 50) -> pd.DataFrame:
    """
    Generate sample data for a language.
    
    Parameters:
    -----------
    language_name : str
        Name of the language (e.g., 'Japanese', 'Chinese')
    language_code : str
        Wikipedia language code
    num_samples : int
        Number of samples to generate
    
    Returns:
    --------
    pd.DataFrame : DataFrame with Text and Language columns
    """
    print(f"\nGenerating {num_samples} samples for {language_name}...")
    
    texts = get_wikipedia_text(language_code, num_samples)
    
    if not texts:
        print(f"[ERROR] No samples could be fetched for {language_name}")
        return pd.DataFrame(columns=['Text', 'Language'])
    
    df = pd.DataFrame({
        'Text': texts,
        'Language': [language_name] * len(texts)
    })
    
    print(f"[OK] Generated {len(texts)} samples for {language_name}")
    return df

def main():
    """Main function to generate language samples."""
    print("="*60)
    print("GENERATE LANGUAGE SAMPLES FROM WIKIPEDIA")
    print("="*60)
    print("\nThis script fetches sample text from Wikipedia for training.")
    print("Note: You need internet connection and 'requests' library installed.")
    print("\nExample language codes:")
    print("  English: en, French: fr, Spanish: es, German: de")
    print("  Japanese: ja, Chinese: zh, Korean: ko, Arabic: ar")
    print("  Portuguese: pt, Italian: it, Russian: ru, Dutch: nl")
    print("  Polish: pl, Czech: cs, Romanian: ro, Hungarian: hu")
    print("  Swedish: sv, Norwegian: no, Finnish: fi, Danish: da")
    print("  Turkish: tr, Greek: el, Hebrew: he, Thai: th")
    print("  Vietnamese: vi, Indonesian: id, Malay: ms, Tagalog: tl")
    
    try:
        language_name = input("\nEnter language name (e.g., 'Japanese'): ").strip()
        language_code = input("Enter Wikipedia language code (e.g., 'ja'): ").strip().lower()
        num_samples = int(input("Enter number of samples to generate (default 50): ") or "50")
        
        df = generate_sample_data(language_name, language_code, num_samples)
        
        if len(df) > 0:
            output_file = f"{language_name}_samples.csv"
            df.to_csv(output_file, index=False)
            print(f"\n[OK] Samples saved to {output_file}")
            print(f"\nYou can now add these to the main dataset using:")
            print(f"  python add_languages.py")
            print(f"\nOr manually add to 'Language Detection.csv'")
        else:
            print("\n[ERROR] No samples were generated. Please check:")
            print("  1. Internet connection")
            print("  2. Language code is correct")
            print("  3. Wikipedia has articles in that language")
    
    except KeyboardInterrupt:
        print("\n\n[WARN] Interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")

if __name__ == "__main__":
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("[ERROR] Error: 'requests' library not installed.")
        print("Install it with: pip install requests")
        sys.exit(1)
    
    main()

