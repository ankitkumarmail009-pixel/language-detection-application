"""
Utility functions for language detection project.
"""

import re
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def preprocess_text(text):
    """
    Clean and preprocess text data:
    - Convert to lowercase
    - Remove special characters and numbers
    - Keep only letters and spaces
    
    Note: This preprocessing removes non-Latin characters (e.g., Hindi, Arabic scripts).
    The model was trained with this preprocessing, so it works best with Latin scripts.
    
    Parameters:
    -----------
    text : str
        Input text to preprocess
    
    Returns:
    --------
    str : Preprocessed text
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters, numbers, and extra spaces
    # Keep only letters and spaces (Latin alphabet only)
    # Note: This matches the training preprocessing
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def predict_language(text, model, vectorizer, label_encoder, min_text_length=3):
    """
    Predict the language of a given text.
    
    Parameters:
    -----------
    text : str
        Input text to predict language for
    model : sklearn model
        Trained classification model
    vectorizer : sklearn vectorizer
        Fitted vectorizer (CountVectorizer or TfidfVectorizer)
    label_encoder : sklearn LabelEncoder
        Fitted label encoder
    min_text_length : int
        Minimum length of cleaned text required for prediction (default: 3)
    
    Returns:
    --------
    str : Predicted language (or "Unknown" if text is too short/empty)
    float : Prediction probability (confidence)
    dict : All language probabilities (empty dict if Unknown)
    str : Warning message (empty if no warning)
    """
    warning = ""
    
    # Validate input
    if not text or not isinstance(text, str):
        return "Unknown", 0.0, {}, "Input text is empty or invalid."
    
    original_length = len(text.strip())
    if original_length == 0:
        return "Unknown", 0.0, {}, "Input text is empty."
    
    # Preprocess the text
    cleaned_text = preprocess_text(text)
    
    # Check if text is empty after preprocessing
    if not cleaned_text:
        return "Unknown", 0.0, {}, "Text contains no Latin alphabet characters. This model works best with Latin scripts (English, French, Spanish, etc.)."
    
    # Check minimum length
    if len(cleaned_text) < min_text_length:
        warning = f"Text is very short ({len(cleaned_text)} characters). Results may be less accurate."
    
    # Check if significant content was removed
    if len(cleaned_text) < original_length * 0.3:
        warning = "Much of the original text was removed during preprocessing. The model works best with Latin alphabet text."
    
    try:
        # Transform text to features
        text_vectorized = vectorizer.transform([cleaned_text])
        
        # Predict
        prediction_encoded = model.predict(text_vectorized)[0]
        prediction_proba = model.predict_proba(text_vectorized)[0]
        
        # Decode prediction
        predicted_language = label_encoder.inverse_transform([prediction_encoded])[0]
        confidence = max(prediction_proba)
        
        # Get all language probabilities
        all_languages = label_encoder.classes_
        language_probs = {
            lang: prob for lang, prob in zip(all_languages, prediction_proba)
        }
        # Sort by probability
        language_probs = dict(sorted(language_probs.items(), key=lambda x: x[1], reverse=True))
        
        return predicted_language, confidence, language_probs, warning
        
    except Exception as e:
        return "Unknown", 0.0, {}, f"Error during prediction: {str(e)}"


def load_model_components(model_path='language_detection_model.pkl',
                         vectorizer_path='count_vectorizer.pkl',
                         label_encoder_path='label_encoder.pkl'):
    """
    Load saved model components.
    
    Parameters:
    -----------
    model_path : str
        Path to saved model file
    vectorizer_path : str
        Path to saved vectorizer file
    label_encoder_path : str
        Path to saved label encoder file
    
    Returns:
    --------
    tuple : (model, vectorizer, label_encoder)
    
    Raises:
    -------
    FileNotFoundError : If any of the model files are not found
    """
    import os
    
    # Check if files exist
    missing_files = []
    if not os.path.exists(model_path):
        missing_files.append(model_path)
    if not os.path.exists(vectorizer_path):
        missing_files.append(vectorizer_path)
    if not os.path.exists(label_encoder_path):
        missing_files.append(label_encoder_path)
    
    if missing_files:
        raise FileNotFoundError(
            f"Model files not found: {', '.join(missing_files)}. "
            f"Please run 'python train_model.py' to train the model first."
        )
    
    try:
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        label_encoder = joblib.load(label_encoder_path)
        
        return model, vectorizer, label_encoder
    except Exception as e:
        raise RuntimeError(f"Error loading model components: {str(e)}")


def batch_predict(texts, model, vectorizer, label_encoder):
    """
    Predict languages for multiple texts at once.
    
    Parameters:
    -----------
    texts : list of str
        List of input texts
    model : sklearn model
        Trained classification model
    vectorizer : sklearn vectorizer
        Fitted vectorizer
    label_encoder : sklearn LabelEncoder
        Fitted label encoder
    
    Returns:
    --------
    list of tuples : [(predicted_language, confidence, warning), ...]
    """
    results = []
    for text in texts:
        predicted_lang, confidence, _, warning = predict_language(text, model, vectorizer, label_encoder)
        results.append((predicted_lang, confidence, warning))
    return results


def translate_text(text, source_lang='auto', target_lang='en'):
    """
    Translate text from source language to target language.
    
    Parameters:
    -----------
    text : str
        Text to translate
    source_lang : str
        Source language code (default: 'auto' for auto-detection)
    target_lang : str
        Target language code (default: 'en' for English)
    
    Returns:
    --------
    str : Translated text
    str : Error message (empty if successful)
    """
    try:
        from deep_translator import GoogleTranslator
        
        if not text or not text.strip():
            return "", "Text is empty."
        
        # Map language names to language codes - use the full supported languages list
        language_code_map = get_supported_languages()
        
        # Convert language names to codes if needed
        if source_lang in language_code_map:
            source_lang = language_code_map[source_lang]
        if target_lang in language_code_map:
            target_lang = language_code_map[target_lang]
        
        # Use 'auto' for source if not a valid code
        if source_lang not in ['auto'] and len(source_lang) != 2:
            source_lang = 'auto'
        
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated_text = translator.translate(text)
        
        return translated_text, ""
    
    except Exception as e:
        return "", f"Translation error: {str(e)}"


def get_supported_languages():
    """
    Get list of supported languages for translation.
    
    Returns:
    --------
    dict : Dictionary mapping language names to language codes
    """
    return {
        # Major European Languages
        'English': 'en', 'French': 'fr', 'Spanish': 'es', 'German': 'de',
        'Italian': 'it', 'Portuguese': 'pt', 'Russian': 'ru', 'Dutch': 'nl',
        'Swedish': 'sv', 'Turkish': 'tr', 'Greek': 'el', 'Danish': 'da',
        'Polish': 'pl', 'Czech': 'cs', 'Romanian': 'ro', 'Hungarian': 'hu',
        'Finnish': 'fi', 'Norwegian': 'no', 'Ukrainian': 'uk', 'Bulgarian': 'bg',
        'Croatian': 'hr', 'Serbian': 'sr', 'Slovak': 'sk', 'Slovenian': 'sl',
        'Lithuanian': 'lt', 'Latvian': 'lv', 'Estonian': 'et', 'Icelandic': 'is',
        'Irish': 'ga', 'Welsh': 'cy', 'Maltese': 'mt', 'Luxembourgish': 'lb',
        
        # Asian Languages
        'Hindi': 'hi', 'Japanese': 'ja', 'Chinese': 'zh', 'Korean': 'ko',
        'Tamil': 'ta', 'Malayalam': 'ml', 'Kannada': 'kn', 'Telugu': 'te',
        'Bengali': 'bn', 'Marathi': 'mr', 'Gujarati': 'gu', 'Punjabi': 'pa',
        'Urdu': 'ur', 'Nepali': 'ne', 'Sinhala': 'si', 'Thai': 'th',
        'Vietnamese': 'vi', 'Indonesian': 'id', 'Malay': 'ms', 'Filipino': 'tl',
        'Burmese': 'my', 'Khmer': 'km', 'Lao': 'lo', 'Mongolian': 'mn',
        
        # Middle Eastern & African Languages
        'Arabic': 'ar', 'Hebrew': 'he', 'Persian': 'fa', 'Pashto': 'ps',
        'Kurdish': 'ku', 'Amharic': 'am', 'Swahili': 'sw', 'Afrikaans': 'af',
        'Zulu': 'zu', 'Xhosa': 'xh', 'Yoruba': 'yo', 'Hausa': 'ha',
        
        # Other Languages
        'Esperanto': 'eo', 'Basque': 'eu', 'Catalan': 'ca', 'Galician': 'gl',
        'Armenian': 'hy', 'Georgian': 'ka', 'Azerbaijani': 'az', 'Kazakh': 'kk',
        'Uzbek': 'uz', 'Tajik': 'tg', 'Belarusian': 'be', 'Macedonian': 'mk',
        'Albanian': 'sq', 'Bosnian': 'bs', 'Moldovan': 'ro', 'Kyrgyz': 'ky',
        
        # Additional Popular Languages
        'Tagalog': 'tl', 'Hawaiian': 'haw', 'Maori': 'mi', 'Samoan': 'sm',
        'Tongan': 'to', 'Fijian': 'fj', 'Tahitian': 'ty', 'Guarani': 'gn',
        'Quechua': 'qu', 'Aymara': 'ay', 'Inuktitut': 'iu', 'Cree': 'cr',
        
        # More European Languages
        'Breton': 'br', 'Cornish': 'kw', 'Manx': 'gv', 'Scots': 'sco',
        'Occitan': 'oc', 'Corsican': 'co', 'Sardinian': 'sc', 'Friulian': 'fur',
        'Ladino': 'lad', 'Romansh': 'rm', 'Walloon': 'wa', 'Limburgish': 'li',
        
        # More Asian Languages
        'Javanese': 'jv', 'Sundanese': 'su', 'Balinese': 'ban', 'Acehnese': 'ace',
        'Minangkabau': 'min', 'Bhojpuri': 'bho', 'Odia': 'or', 'Assamese': 'as',
        'Kashmiri': 'ks', 'Sindhi': 'sd', 'Sanskrit': 'sa', 'Tibetan': 'bo',
        'Dzongkha': 'dz', 'Maldivian': 'dv', 'Dhivehi': 'dv',
        'Uyghur': 'ug', 'Tatar': 'tt', 'Bashkir': 'ba', 'Chuvash': 'cv',
        'Chechen': 'ce', 'Ingush': 'inh', 'Avar': 'av', 'Lezgian': 'lez',
        
        # More Middle Eastern Languages
        'Turkmen': 'tk', 'Dari': 'prs',
        'Balochi': 'bal', 'Gilaki': 'glk', 'Mazanderani': 'mzn',
        
        # More African Languages
        'Igbo': 'ig', 'Fulani': 'ff', 'Wolof': 'wo', 'Mandinka': 'mnk',
        'Bambara': 'bm',         'Kinyarwanda': 'rw', 'Kirundi': 'rn', 'Luganda': 'lg',
        'Kikuyu': 'ki', 'Oromo': 'om', 'Somali': 'so', 'Tigrinya': 'ti',
        'Lingala': 'ln', 'Kongo': 'kg',
        'Shona': 'sn', 'Chewa': 'ny',
        'Malagasy': 'mg', 'Seychellois Creole': 'crs', 'Mauritian Creole': 'mfe',
        
        # More Languages from Americas
        'Haitian Creole': 'ht', 'Jamaican Patois': 'jam', 'Papiamento': 'pap',
        'Greenlandic': 'kl', 'Navajo': 'nv', 'Cherokee': 'chr', 'Ojibwe': 'oj',
        'Yupik': 'esu', 'Aleut': 'ale',
        
        # More Pacific Languages
        'Chamorro': 'ch', 'Marshallese': 'mh', 'Palauan': 'pau', 'Gilbertese': 'gil',
        'Tok Pisin': 'tpi', 'Bislama': 'bi', 'Hiri Motu': 'ho', 'Tetum': 'tet',
        
        # Additional Regional Languages
        'Sicilian': 'scn', 'Venetian': 'vec', 'Lombard': 'lmo', 'Piedmontese': 'pms',
        'Neapolitan': 'nap', 'Asturian': 'ast', 'Aragonese': 'an',
        'Mirandese': 'mwl', 'Extremaduran': 'ext', 'Leonese': 'ast',
        
        # Constructed Languages
        'Interlingua': 'ia', 'Ido': 'io', 'Volapuk': 'vo', 'Lojban': 'jbo',
        
        # Historical/Classical Languages
        'Latin': 'la', 'Ancient Greek': 'grc', 'Old English': 'ang', 'Old Norse': 'non',
        'Sanskrit': 'sa', 'Classical Arabic': 'arq', 'Old Church Slavonic': 'cu',
        
        # Sign Languages (text representation)
        'American Sign Language': 'ase', 'British Sign Language': 'bfi',
        
        # Additional Regional Variants
        'Cantonese': 'yue', 'Hakka': 'hak', 'Hokkien': 'nan', 'Wu Chinese': 'wuu',
        'Shanghainese': 'wuu', 'Hmong': 'hmn', 'Lao': 'lo', 'Shan': 'shn',
        'Karen': 'kar', 'Mon': 'mnw', 'Chin': 'cnh', 'Kachin': 'kac',
        
        # More Languages
        'Venda': 've', 'Tsonga': 'ts', 'Northern Sotho': 'nso',
        'Swati': 'ss', 'Khoekhoe': 'naq', 'Herero': 'hz',
        
        # Additional European Regional & Minority Languages
        'Faroese': 'fo', 'Greenlandic': 'kl', 'Sami': 'se', 'Karelian': 'krl',
        'Veps': 'vep', 'Livonian': 'liv', 'Votic': 'vot', 'Ingrian': 'izh',
        'Mari': 'chm', 'Mordvin': 'myv', 'Udmurt': 'udm', 'Komi': 'kv',
        'Chuvash': 'cv', 'Bashkir': 'ba', 'Tatar': 'tt', 'Yakut': 'sah',
        'Buryat': 'bua', 'Kalmyk': 'xal', 'Tuvan': 'tyv', 'Altai': 'alt',
        'Khakas': 'kjh', 'Shor': 'cjs', 'Tofalar': 'kim', 'Dolgan': 'dlg',
        
        # More Asian Regional Languages
        'Konkani': 'kok', 'Manipuri': 'mni', 'Mizo': 'lus', 'Khasi': 'kha',
        'Garo': 'grt', 'Bodo': 'brx', 'Santali': 'sat', 'Ho': 'hoc',
        'Mundari': 'unr', 'Kurukh': 'kru', 'Gondi': 'gon', 'Tulu': 'tcy',
        'Kodava': 'kfa', 'Beary': 'beq', 'Coorgi': 'kfa', 'Saurashtra': 'saz',
        'Meitei': 'mni', 'Lepcha': 'lep', 'Limbu': 'lif', 'Newari': 'new',
        'Rai': 'raj', 'Tamang': 'taj', 'Gurung': 'gvr', 'Magar': 'mgp',
        'Tharu': 'thr', 'Chepang': 'cdm', 'Sunwar': 'suz', 'Yakkha': 'ybh',
        'Athpare': 'ath', 'Bantawa': 'bap', 'Chamling': 'rab', 'Dumi': 'dus',
        'Dzongkha': 'dz', 'Ladakhi': 'lbj', 'Balti': 'bft', 'Burushaski': 'bsk',
        'Shina': 'scl', 'Khowar': 'khw', 'Kalasha': 'kls', 'Wakhi': 'wbl',
        'Yidgha': 'ydg', 'Dameli': 'dml', 'Gawar-Bati': 'gwt', 'Nuristani': 'ask',
        
        # More Southeast Asian Languages
        'Acehnese': 'ace', 'Banjar': 'bjn', 'Buginese': 'bug', 'Cebuano': 'ceb',
        'Ilocano': 'ilo', 'Kapampangan': 'pam', 'Pangasinan': 'pag', 'Waray': 'war',
        'Bikol': 'bcl', 'Hiligaynon': 'hil', 'Maguindanao': 'mdh', 'Maranao': 'mrw',
        'Tausug': 'tsg', 'Chavacano': 'cbk', 'Ibanag': 'ibg', 'Ivatan': 'ivv',
        'Kankanaey': 'knk', 'Kinaray-a': 'krj', 'Maguindanao': 'mdh', 'Maranao': 'mrw',
        'Pangasinan': 'pag', 'Surigaonon': 'sgd', 'Tboli': 'tbl', 'Tausug': 'tsg',
        'Yakan': 'yka', 'Zamboangueño': 'cbk',
        
        # More African Languages
        'Akan': 'ak', 'Ewe': 'ee', 'Ga': 'gaa', 'Fante': 'fat',
        'Twi': 'tw', 'Yoruba': 'yo', 'Igbo': 'ig', 'Hausa': 'ha',
        'Fulani': 'ff', 'Wolof': 'wo', 'Mandinka': 'mnk', 'Bambara': 'bm',
        'Soninke': 'snk', 'Songhay': 'ses', 'Tamasheq': 'tmh', 'Kanuri': 'kr',
        'Hausa': 'ha', 'Fulfulde': 'ff', 'Kanuri': 'kr', 'Tiv': 'tiv',
        'Ibibio': 'ibb', 'Efik': 'efi', 'Annang': 'anv', 'Edo': 'bin',
        'Urhobo': 'urh', 'Isoko': 'iso', 'Ijaw': 'ijc', 'Tiv': 'tiv',
        'Nupe': 'nup', 'Gbagyi': 'gbr', 'Ebira': 'igb', 'Idoma': 'idu',
        'Tiv': 'tiv', 'Jukun': 'dyu', 'Berom': 'bom', 'Tarok': 'yer',
        'Goemai': 'ank', 'Mwaghavul': 'sur', 'Ngas': 'anc', 'Ron': 'cla',
        'Bura': 'bwr', 'Margi': 'mrt', 'Kilba': 'kib', 'Hwana': 'hwo',
        'Kamwe': 'hig', 'Bachama': 'bcy', 'Bata': 'bta', 'Gude': 'gde',
        'Mafa': 'maf', 'Mofu': 'mof', 'Muyang': 'muy', 'Zulgo': 'zul',
        'Giziga': 'giz', 'Mbuko': 'mbu', 'Mada': 'mda', 'Mofu-Gudur': 'mof',
        'Ouldeme': 'udl', 'Muyang': 'muy', 'Zulgo': 'zul', 'Giziga': 'giz',
        'Mbuko': 'mbu', 'Mada': 'mda', 'Mofu-Gudur': 'mof', 'Ouldeme': 'udl',
        
        # More Indigenous Languages of Americas
        'Quechua': 'qu', 'Aymara': 'ay', 'Guarani': 'gn', 'Nahuatl': 'nah',
        'Mapudungun': 'arn', 'Araucanian': 'arn', 'Guarani': 'gn', 'Tupi': 'tpn',
        'Wayuu': 'guc', 'Aymara': 'ay', 'Quechua': 'qu', 'Shipibo': 'shp',
        'Ashaninka': 'cni', 'Awajun': 'agr', 'Cocama': 'cod', 'Matsés': 'mcf',
        'Yagua': 'yad', 'Bora': 'boa', 'Witoto': 'hto', 'Ticuna': 'tca',
        'Huitoto': 'hto', 'Ocaina': 'oca', 'Andoque': 'ano', 'Bora': 'boa',
        'Muinane': 'bmr', 'Nonuya': 'noj', 'Resigaro': 'rgr', 'Andoque': 'ano',
        
        # More Pacific & Austronesian Languages
        'Fijian': 'fj', 'Tongan': 'to', 'Samoan': 'sm', 'Tahitian': 'ty',
        'Maori': 'mi', 'Hawaiian': 'haw', 'Chamorro': 'ch', 'Palauan': 'pau',
        'Marshallese': 'mh', 'Gilbertese': 'gil', 'Nauruan': 'na', 'Rotuman': 'rtm',
        'Tuvaluan': 'tvl', 'Tokelauan': 'tkl', 'Niuean': 'niu', 'Cook Islands Maori': 'rar',
        'Rapa Nui': 'rap', 'Marquesan': 'mrq', 'Mangarevan': 'mrv', 'Tahitian': 'ty',
        'Austral': 'aut', 'Rapa': 'ray', 'Rurutu': 'rut', 'Tubuai': 'tbu',
        'Ma\'ohi': 'ty', 'Tahitian': 'ty', 'Tuamotuan': 'pmt', 'Gambier': 'mva',
        
        # More Creole & Pidgin Languages
        'Haitian Creole': 'ht', 'Jamaican Patois': 'jam', 'Papiamento': 'pap',
        'Seychellois Creole': 'crs', 'Mauritian Creole': 'mfe', 'Réunion Creole': 'rcf',
        'Guadeloupean Creole': 'gcf', 'Martinican Creole': 'gcf', 'Louisiana Creole': 'lou',
        'Gullah': 'gul', 'Sranan Tongo': 'srn', 'Tok Pisin': 'tpi', 'Bislama': 'bi',
        'Hiri Motu': 'ho', 'Pitcairn-Norfolk': 'pih', 'Norfolk': 'pih',
        
        # More Constructed & Auxiliary Languages
        'Esperanto': 'eo', 'Ido': 'io', 'Interlingua': 'ia', 'Volapuk': 'vo',
        'Lojban': 'jbo', 'Toki Pona': 'tok', 'Klingon': 'tlh', 'Na\'vi': 'nv',
        'Dothraki': 'doth', 'Valyrian': 'val', 'Quenya': 'qya', 'Sindarin': 'sjn',
        
        # More Historical & Classical Languages
        'Latin': 'la', 'Ancient Greek': 'grc', 'Classical Arabic': 'arq',
        'Old English': 'ang', 'Old Norse': 'non', 'Old Church Slavonic': 'cu',
        'Gothic': 'got', 'Old High German': 'goh', 'Old French': 'fro',
        'Old Spanish': 'osp', 'Old Italian': 'roa', 'Medieval Latin': 'la',
        'Byzantine Greek': 'grc', 'Koine Greek': 'grc', 'Attic Greek': 'grc',
        'Classical Chinese': 'lzh', 'Literary Chinese': 'lzh', 'Old Japanese': 'ojp',
        'Middle Korean': 'okm', 'Old Korean': 'oko', 'Classical Tibetan': 'xct',
        'Old Persian': 'peo', 'Avestan': 'ae', 'Pali': 'pi', 'Sanskrit': 'sa',
        'Prakrit': 'pra', 'Apabhramsha': 'apa', 'Old Gujarati': 'gu',
        
        # Additional Regional Languages
        'Ladino': 'lad', 'Yiddish': 'yi', 'Judeo-Arabic': 'jrb', 'Judeo-Persian': 'jpr',
        'Karaim': 'kdr', 'Krymchak': 'jct', 'Juhuri': 'jdt', 'Bukharian': 'bhh',
        'Tat': 'ttt', 'Judeo-Tat': 'jdt', 'Judeo-Georgian': 'ka', 'Judeo-Greek': 'yej',
        
        # More Sign Languages (text representation)
        'American Sign Language': 'ase', 'British Sign Language': 'bfi',
        'French Sign Language': 'fsl', 'German Sign Language': 'gsg',
        'Spanish Sign Language': 'ssp', 'Italian Sign Language': 'ise',
        'Russian Sign Language': 'rsl', 'Japanese Sign Language': 'jsl',
        'Chinese Sign Language': 'csl', 'Korean Sign Language': 'kvk',
        'Brazilian Sign Language': 'bzs', 'Mexican Sign Language': 'mfs',
        'Australian Sign Language': 'asf', 'New Zealand Sign Language': 'nzs',
        'South African Sign Language': 'sfs', 'Kenyan Sign Language': 'xki',
        'Ugandan Sign Language': 'ugn', 'Tanzanian Sign Language': 'tza',
        'Ghanaian Sign Language': 'gse', 'Nigerian Sign Language': 'nsi',
        'Ethiopian Sign Language': 'eth', 'Moroccan Sign Language': 'xms',
        'Algerian Sign Language': 'asp', 'Tunisian Sign Language': 'tse',
        'Egyptian Sign Language': 'esl', 'Iraqi Sign Language': 'ads',
        'Israeli Sign Language': 'isr', 'Turkish Sign Language': 'tsm',
        'Greek Sign Language': 'gss', 'Polish Sign Language': 'pso',
        'Czech Sign Language': 'cse', 'Hungarian Sign Language': 'hsh',
        'Romanian Sign Language': 'rms', 'Bulgarian Sign Language': 'bqn',
        'Croatian Sign Language': 'csq', 'Serbian Sign Language': 'srp',
        'Slovenian Sign Language': 'sls', 'Slovak Sign Language': 'svk',
        'Lithuanian Sign Language': 'lls', 'Latvian Sign Language': 'lsl',
        'Estonian Sign Language': 'eso', 'Finnish Sign Language': 'fse',
        'Swedish Sign Language': 'swl', 'Norwegian Sign Language': 'nsl',
        'Danish Sign Language': 'dsl', 'Icelandic Sign Language': 'icl',
        'Irish Sign Language': 'isg', 'Welsh Sign Language': 'wls',
        'Scottish Sign Language': 'bfi', 'Northern Ireland Sign Language': 'nid',
        
        # Additional Regional & Minority Languages
        'Romansh': 'rm', 'Ladin': 'lld', 'Friulian': 'fur', 'Lombard': 'lmo',
        'Piedmontese': 'pms', 'Venetian': 'vec', 'Emilian-Romagnol': 'eml',
        'Ligurian': 'lij', 'Sardinian': 'sc', 'Corsican': 'co', 'Sicilian': 'scn',
        'Neapolitan': 'nap', 'Calabrian': 'roa', 'Abruzzese': 'roa', 'Molise Croatian': 'svm',
        'Arbëresh': 'aae', 'Griko': 'ell', 'Italkian': 'itk', 'Judeo-Italian': 'itk',
        'Ladino': 'lad', 'Yiddish': 'yi', 'Karaim': 'kdr', 'Krymchak': 'jct',
        'Crimean Tatar': 'crh', 'Gagauz': 'gag', 'Karachay-Balkar': 'krc',
        'Kumyk': 'kum', 'Nogai': 'nog', 'Karaim': 'kdr', 'Krymchak': 'jct',
        'Crimean Tatar': 'crh', 'Gagauz': 'gag', 'Karachay-Balkar': 'krc',
        'Kumyk': 'kum', 'Nogai': 'nog', 'Kalmyk': 'xal', 'Buryat': 'bua',
        'Tuvan': 'tyv', 'Altai': 'alt', 'Khakas': 'kjh', 'Shor': 'cjs',
        'Yakut': 'sah', 'Dolgan': 'dlg', 'Evenki': 'evn', 'Even': 'eve',
        'Nanai': 'gld', 'Udege': 'ude', 'Oroch': 'oac', 'Orok': 'oaa',
        'Negidal': 'neg', 'Ulch': 'ulc', 'Nivkh': 'niv', 'Ainu': 'ain',
        'Yukaghir': 'yux', 'Chukchi': 'ckt', 'Koryak': 'kpy', 'Itelmen': 'itl',
        'Aleut': 'ale', 'Eskimo': 'esx', 'Inuit': 'iu', 'Yupik': 'esu',
        'Greenlandic': 'kl', 'Inupiaq': 'ik', 'Central Alaskan Yup\'ik': 'esu',
        'Siberian Yupik': 'ess', 'Alutiiq': 'ems', 'Sugpiaq': 'ems',
        'Central Siberian Yupik': 'ess', 'Naukan Yupik': 'ynk', 'Sirenik': 'ysr'
    }


