"""
Streamlit web application for language detection.
Enhanced with modern UI and better UX.
"""

import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from utils import predict_language, load_model_components, translate_text, get_supported_languages

# Page configuration
st.set_page_config(
    page_title="Language Detector | AI-Powered",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dynamic Animated Design with Moving Elements
# Load external CSS and JS files
try:
    with open('styles.css', 'r', encoding='utf-8') as f:
        css_content = f.read()
    with open('script.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    {css_content}
    </style>
    
    <script>
    {js_content}
    </script>
""", unsafe_allow_html=True)
except FileNotFoundError:
    st.error("CSS/JS files not found. Please ensure styles.css and script.js are in the project directory.")

# Language flags mapping
LANGUAGE_FLAGS = {
    # Major European Languages
    "English": "🇬🇧", "French": "🇫🇷", "Spanish": "🇪🇸", "German": "🇩🇪",
    "Italian": "🇮🇹", "Portuguese": "🇵🇹", "Portugeese": "🇵🇹", "Russian": "🇷🇺", 
    "Dutch": "🇳🇱", "Swedish": "🇸🇪", "Sweedish": "🇸🇪", "Turkish": "🇹🇷", 
    "Greek": "🇬🇷", "Danish": "🇩🇰", "Polish": "🇵🇱", "Czech": "🇨🇿",
    "Romanian": "🇷🇴", "Hungarian": "🇭🇺", "Finnish": "🇫🇮", "Norwegian": "🇳🇴",
    "Ukrainian": "🇺🇦", "Bulgarian": "🇧🇬", "Croatian": "🇭🇷", "Serbian": "🇷🇸",
    "Slovak": "🇸🇰", "Slovenian": "🇸🇮", "Lithuanian": "🇱🇹", "Latvian": "🇱🇻",
    "Estonian": "🇪🇪", "Icelandic": "🇮🇸", "Irish": "🇮🇪", "Welsh": "🏴",
    "Maltese": "🇲🇹", "Luxembourgish": "🇱🇺",
    
    # Asian Languages
    "Hindi": "🇮🇳", "Japanese": "🇯🇵", "Chinese": "🇨🇳", "Korean": "🇰🇷",
    "Tamil": "🇮🇳", "Malayalam": "🇮🇳", "Kannada": "🇮🇳", "Telugu": "🇮🇳",
    "Bengali": "🇧🇩", "Marathi": "🇮🇳", "Gujarati": "🇮🇳", "Punjabi": "🇮🇳",
    "Urdu": "🇵🇰", "Nepali": "🇳🇵", "Sinhala": "🇱🇰", "Thai": "🇹🇭",
    "Vietnamese": "🇻🇳", "Indonesian": "🇮🇩", "Malay": "🇲🇾", "Filipino": "🇵🇭",
    "Tagalog": "🇵🇭", "Burmese": "🇲🇲", "Khmer": "🇰🇭", "Lao": "🇱🇦",
    "Mongolian": "🇲🇳",
    
    # Middle Eastern & African Languages
    "Arabic": "🇸🇦", "Hebrew": "🇮🇱", "Persian": "🇮🇷", "Pashto": "🇦🇫",
    "Kurdish": "🇮🇶", "Amharic": "🇪🇹", "Swahili": "🇰🇪", "Afrikaans": "🇿🇦",
    "Zulu": "🇿🇦", "Xhosa": "🇿🇦", "Yoruba": "🇳🇬", "Hausa": "🇳🇬",
    
    # Other Languages
    "Esperanto": "🌐", "Basque": "🇪🇸", "Catalan": "🇪🇸", "Galician": "🇪🇸",
    "Armenian": "🇦🇲", "Georgian": "🇬🇪", "Azerbaijani": "🇦🇿", "Kazakh": "🇰🇿",
    "Uzbek": "🇺🇿", "Tajik": "🇹🇯", "Belarusian": "🇧🇾", "Macedonian": "🇲🇰",
    "Albanian": "🇦🇱", "Bosnian": "🇧🇦", "Moldovan": "🇲🇩", "Kyrgyz": "🇰🇬",
    
    # Additional Languages
    "Hawaiian": "🇺🇸", "Maori": "🇳🇿", "Samoan": "🇼🇸", "Tongan": "🇹🇴",
    "Fijian": "🇫🇯", "Tahitian": "🇵🇫", "Guarani": "🇵🇾", "Quechua": "🇵🇪",
    "Aymara": "🇧🇴", "Inuktitut": "🇨🇦", "Cree": "🇨🇦",
    
    # More European Regional Languages
    "Breton": "🇫🇷", "Cornish": "🏴", "Manx": "🇮🇲", "Scots": "🏴",
    "Occitan": "🇫🇷", "Corsican": "🇫🇷", "Sardinian": "🇮🇹", "Friulian": "🇮🇹",
    "Ladino": "🌐", "Romansh": "🇨🇭", "Walloon": "🇧🇪", "Limburgish": "🇳🇱",
    "Sicilian": "🇮🇹", "Venetian": "🇮🇹", "Lombard": "🇮🇹", "Piedmontese": "🇮🇹",
    "Neapolitan": "🇮🇹", "Asturian": "🇪🇸", "Aragonese": "🇪🇸", "Mirandese": "🇵🇹",
    
    # More Asian Languages
    "Javanese": "🇮🇩", "Sundanese": "🇮🇩", "Balinese": "🇮🇩", "Acehnese": "🇮🇩",
    "Minangkabau": "🇮🇩", "Bhojpuri": "🇮🇳", "Odia": "🇮🇳", "Assamese": "🇮🇳",
    "Kashmiri": "🇮🇳", "Sindhi": "🇵🇰", "Sanskrit": "🇮🇳", "Tibetan": "🇨🇳",
    "Dzongkha": "🇧🇹", "Maldivian": "🇲🇻", "Uyghur": "🇨🇳", "Tatar": "🇷🇺",
    "Bashkir": "🇷🇺", "Chuvash": "🇷🇺", "Chechen": "🇷🇺", "Ingush": "🇷🇺",
    "Cantonese": "🇭🇰", "Hakka": "🇨🇳", "Hokkien": "🇹🇼", "Wu Chinese": "🇨🇳",
    "Hmong": "🇨🇳", "Shan": "🇲🇲", "Karen": "🇲🇲", "Mon": "🇲🇲",
    
    # More Middle Eastern Languages
    "Turkmen": "🇹🇲", "Dari": "🇦🇫", "Balochi": "🇵🇰", "Gilaki": "🇮🇷",
    "Mazanderani": "🇮🇷",
    
    # More African Languages
    "Igbo": "🇳🇬", "Fulani": "🌐", "Wolof": "🇸🇳", "Mandinka": "🌐",
    "Bambara": "🇲🇱", "Kinyarwanda": "🇷🇼", "Kirundi": "🇧🇮", "Luganda": "🇺🇬",
    "Kikuyu": "🇰🇪", "Oromo": "🇪🇹", "Somali": "🇸🇴", "Tigrinya": "🇪🇷",
    "Lingala": "🇨🇩", "Kongo": "🇨🇩", "Tswana": "🇧🇼", "Sesotho": "🇱🇸",
    "Shona": "🇿🇼", "Ndebele": "🇿🇼", "Chewa": "🇲🇼", "Malagasy": "🇲🇬",
    "Haitian Creole": "🇭🇹", "Venda": "🇿🇦", "Tsonga": "🇿🇦", "Northern Sotho": "🇿🇦",
    "Southern Sotho": "🇿🇦", "Swati": "🇸🇿",
    
    # More Languages from Americas
    "Jamaican Patois": "🇯🇲", "Papiamento": "🇦🇼", "Greenlandic": "🇬🇱",
    "Navajo": "🇺🇸", "Cherokee": "🇺🇸", "Ojibwe": "🇨🇦",
    
    # More Pacific Languages
    "Chamorro": "🇬🇺", "Marshallese": "🇲🇭", "Palauan": "🇵🇼", "Gilbertese": "🇰🇮",
    "Tok Pisin": "🇵🇬", "Bislama": "🇻🇺", "Hiri Motu": "🇵🇬", "Tetum": "🇹🇱",
    
    # Constructed Languages
    "Interlingua": "🌐", "Ido": "🌐", "Volapuk": "🌐", "Lojban": "🌐",
    
    # Historical/Classical Languages
    "Latin": "🏛️", "Ancient Greek": "🏛️", "Old English": "🏛️", "Old Norse": "🏛️",
    "Classical Arabic": "🏛️", "Old Church Slavonic": "🏛️",
    
    # Sign Languages
    "American Sign Language": "🤟", "British Sign Language": "🤟",
    
    # Additional Important Languages
    "Faroese": "🇫🇴", "Sami": "🇳🇴", "Yiddish": "🌐", "Ladino": "🌐",
    "Nahuatl": "🇲🇽", "Mapudungun": "🇨🇱", "Ainu": "🇯🇵", "Greenlandic": "🇬🇱",
    "Tok Pisin": "🇵🇬", "Bislama": "🇻🇺", "Haitian Creole": "🇭🇹",
    "Esperanto": "🌐", "Klingon": "🖖", "Latin": "🏛️", "Sanskrit": "🇮🇳"
}

def render_hero_section():
    st.markdown(
        """
        <div style="
            text-align: center; 
            padding: 3rem 1rem 2rem 1rem; 
            margin-bottom: 3rem;
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(79, 70, 229, 0.05) 100%);
            border-radius: 24px;
            border: 1px solid rgba(139, 92, 246, 0.2);
            box-shadow: 0 8px 32px rgba(139, 92, 246, 0.2);
            backdrop-filter: blur(10px);
        ">
            <h1 class="main-header" style="
                margin-bottom: 1rem;
                font-family: 'Poppins', sans-serif;
                font-weight: 800;
                font-size: 3.5rem;
                background: linear-gradient(135deg, #a78bfa 0%, #c084fc 50%, #f472b6 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 0 0 40px rgba(139, 92, 246, 0.5);
                letter-spacing: -0.02em;
            ">🌐 Language Detector</h1>
            <p class="sub-header" style="
                font-size: 1.15rem; 
                line-height: 1.8; 
                max-width: 800px; 
                margin: 0 auto;
                color: #cbd5e1;
                font-weight: 400;
                font-family: 'Space Grotesk', sans-serif;
            ">
                Paste any snippet and get instant language predictions with confidence metrics.
            </p>
            <div style="margin-top: 1.5rem;">
                <a style="
                    padding: 0.85rem 1.5rem;
                    border-radius: 14px;
                    background: linear-gradient(120deg, #a855f7, #ec4899);
                    color: white;
                    text-decoration: none;
                    font-weight: 600;
                    box-shadow: 0 12px 30px rgba(236, 72, 153, 0.35);
                " href="#demo">
                    Start Detecting
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_how_it_works_section():
    st.markdown(
        """
        <div class="section-heading" style="margin-bottom: 1rem;">
            <h2>How It Works</h2>
            <span class="pill">Process</span>
        </div>
        <div class="how-cards">
            <article>
                <strong>1. Paste or Type Text</strong>
                <p>Provide any sentence, paragraph, or long-form snippet for analysis.</p>
            </article>
            <article>
                <strong>2. Smart Preprocessing</strong>
                <p>We normalize, lowercase, and vectorize content using TF-IDF features.</p>
            </article>
            <article>
                <strong>3. Predict Language</strong>
                <p>Our Multinomial Naïve Bayes classifier infers the most likely language.</p>
            </article>
            <article>
                <strong>4. Report Confidence</strong>
                <p>We surface probabilities, ISO codes, and tips for next steps.</p>
            </article>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_section():
    st.markdown(
        """
        <div class="section-heading" style="margin-top: 3rem;">
            <h2>Why Developers Love This Detector</h2>
            <span class="pill">Highlights</span>
        </div>
        <div class="how-cards" style="grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));">
            <article>
                <strong>⚡ Fast Inference</strong>
                <p>Optimized scikit-learn pipeline returns predictions in under 100 ms.</p>
            </article>
            <article>
                <strong>🌍 Broad Coverage</strong>
                <p>Trained on 70+ languages with 50k+ curated samples.</p>
            </article>
            <article>
                <strong>🧠 Transparent Stack</strong>
                <p>Python, Pandas, TF-IDF, and Naive Bayes—easy to audit and extend.</p>
            </article>
            <article>
                <strong>🧩 Integration Ready</strong>
                <p>Hook it into FastAPI, Streamlit, or any REST endpoint for production.</p>
            </article>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_detection_tab(model, vectorizer, label_encoder):
    st.markdown('<div id="demo"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-heading" style="margin-top: 2.5rem;">
            <h2>Language Detection Playground</h2>
            <span class="helper">Paste at least 10 characters for best accuracy.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sample_texts = {
        "English": "Hello, I'd love to travel to Spain someday.",
        "Spanish": "Hola, ¿cómo estás? Espero que tengas un gran día.",
        "French": "Bonjour, merci beaucoup pour votre aide aujourd'hui.",
        "German": "Guten Tag! Dieses Projekt macht mir wirklich Spaß.",
    }

    st.session_state.setdefault("detector_text", "")
    st.session_state.setdefault("detector_result", None)

    sample_cols = st.columns(len(sample_texts))
    for (label, text), col in zip(sample_texts.items(), sample_cols):
        with col:
            if st.button(f"{label}", key=f"sample_{label}"):
                st.session_state.detector_text = text
                st.session_state.detector_result = None
                st.experimental_rerun()

    st.text_area(
        "Input text",
        key="detector_text",
        height=180,
        placeholder="Paste or type any snippet here...",
        help="Supports Latin scripts best; transliterate for Cyrillic/Arabic/Asian content.",
    )

    detect_col, clear_col = st.columns([2, 1])
    with detect_col:
        detect_clicked = st.button("🔍 Detect Language", key="detect_language_btn", use_container_width=True)
    with clear_col:
        if st.button("🧹 Clear", use_container_width=True):
            st.session_state.detector_text = ""
            st.session_state.detector_result = None
            st.experimental_rerun()

    if detect_clicked:
        text = st.session_state.detector_text.strip()
        if len(text) < 10:
            st.warning("Please provide at least 10 characters for a reliable prediction.")
        else:
            with st.spinner("Analyzing language..."):
                language, confidence, language_probs, warning = predict_language(
                    text, model, vectorizer, label_encoder
                )
                top_probs = sorted(language_probs.items(), key=lambda x: x[1], reverse=True)[:5]
                st.session_state.detector_result = {
                    "language": language,
                    "confidence": confidence,
                    "iso": language[:2].lower() if language != "Unknown" else "—",
                    "warning": warning,
                    "top_probs": top_probs,
                }

    result = st.session_state.get("detector_result")
    if result:
        language = result["language"]
        confidence = result["confidence"]
        iso_code = result["iso"]
        warning = result["warning"]
        top_probs = result["top_probs"]

        st.markdown(
            f"""
            <div class="card highlight results-card" style="margin-top: 1.5rem;">
                <div class="results-grid">
                    <div>
                        <span class="helper">Detected Language</span>
                        <span class="value">{language}</span>
                    </div>
                    <div>
                        <span class="helper">Confidence</span>
                        <span class="value">{confidence:.1%}</span>
                    </div>
                    <div>
                        <span class="helper">ISO Code</span>
                        <span class="value">{iso_code}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if warning:
            st.info(warning)

        text = st.session_state.detector_text
        stats_cols = st.columns(4)
        stats = [
            ("Characters", len(text)),
            ("Words", len(text.split())),
            ("Lines", len(text.splitlines())),
            ("Lowercased", len(text.lower().strip())),
        ]
        for (label, value), col in zip(stats, stats_cols):
            with col:
                st.metric(label, value)

        st.markdown("### Top Candidates")
        for idx, (lang, prob) in enumerate(top_probs, start=1):
            st.progress(prob)
            st.write(f"{idx}. **{lang}** — {prob:.1%}")

# Initialize session state
if 'game_score' not in st.session_state:
    st.session_state.game_score = 0
if 'game_round' not in st.session_state:
    st.session_state.game_round = 0
if 'game_history' not in st.session_state:
    st.session_state.game_history = []

# Mode definitions with descriptions and colors
modes_info = {
    "🔍 Normal Detection": {
        "description": "Detect the language of your text",
        "color": "#ff6b9d",
        "bg_gradient": "linear-gradient(135deg, #fff0f5 0%, #ffe0e6 100%)",
        "border_color": "#ffb3d1"
    },
    "🌐 Translator": {
        "description": "Translate text between 500+ languages",
        "color": "#4dabf7",
        "bg_gradient": "linear-gradient(135deg, #e6f3ff 0%, #cce6ff 100%)",
        "border_color": "#99ccff"
    },
    "🎮 Guessing Game": {
        "description": "Test your language knowledge",
        "color": "#51cf66",
        "bg_gradient": "linear-gradient(135deg, #f0fff4 0%, #e0ffe0 100%)",
        "border_color": "#99ff99"
    },
    "📊 Batch Analysis": {
        "description": "Analyze multiple texts at once",
        "color": "#ffa94d",
        "bg_gradient": "linear-gradient(135deg, #fff5e6 0%, #ffe6cc 100%)",
        "border_color": "#ffcc99"
    },
    "⚖️ Compare Texts": {
        "description": "Compare two texts side-by-side",
        "color": "#9775fa",
        "bg_gradient": "linear-gradient(135deg, #f5e6ff 0%, #e6ccff 100%)",
        "border_color": "#cc99ff"
    }
}

# ============================================
# MODERN MODE SELECTION CARDS LAYOUT
# ============================================
st.markdown("""
<div style="
    margin: 2.5rem 0 2rem 0; 
    padding: 0 1rem;
    text-align: center;
">
    <h2 style="
        text-align: center; 
        color: #ffffff; 
        font-weight: 800; 
        margin-bottom: 0.75rem; 
        font-size: 2.25rem;
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #a78bfa 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
    ">
        🎯 Choose Your Mode
    </h2>
    <p style="
        text-align: center; 
        color: #cbd5e1; 
        margin-bottom: 0; 
        font-size: 1.1rem; 
        max-width: 600px; 
        margin-left: auto; 
        margin-right: auto;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 400;
    ">
        Select a feature below to get started
    </p>
</div>
""", unsafe_allow_html=True)

# Responsive columns: 5 on desktop, 3 on tablet, 2 on mobile
# Using container for better control
with st.container():
    # Create responsive column layout
    mode_cols = st.columns(5, gap="medium")

# Display mode cards with clickable buttons
for idx, (mode_name, mode_data) in enumerate(modes_info.items()):
    with mode_cols[idx]:
        is_active = st.session_state.current_mode == mode_name
        
        # Extract icon and title
        icon = mode_name.split()[0] if mode_name.split()[0] in ["🔍", "🌐", "🎮", "📊", "⚖️"] else mode_name[0]
        title = " ".join(mode_name.split()[1:]) if len(mode_name.split()) > 1 else mode_name
        
        # Optimized button label with better formatting
        button_label = f"{icon}\n\n**{title}**\n\n{mode_data['description']}"
        
        # Modern button styling with vibrant gradients
        # Modern color gradients for each mode
        modern_gradients = [
            "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",  # Normal Detection - Purple
            "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",  # Translator - Pink
            "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",  # Guessing Game - Blue
            "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",  # Batch Analysis - Green
            "linear-gradient(135deg, #fa709a 0%, #fee140 100%)"   # Compare Texts - Orange
        ]
        
        modern_borders = ["#8b5cf6", "#ec4899", "#3b82f6", "#10b981", "#f59e0b"]
        
        button_css = f"""
        <style>
        /* Modern Mode Card Button Styling */
        button[key="mode_btn_{idx}"] {{
            background: {modern_gradients[idx]} !important;
            border: 2px solid {modern_borders[idx]} !important;
            border-radius: 20px !important;
            padding: 2rem 1.25rem !important;
            min-height: 220px !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            font-family: 'Poppins', sans-serif !important;
            text-align: center !important;
            white-space: pre-line !important;
            line-height: 1.8 !important;
            font-size: 1rem !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            backdrop-filter: blur(10px) !important;
            position: relative !important;
            overflow: hidden !important;
            {'box-shadow: 0 15px 40px rgba(139, 92, 246, 0.6), 0 0 30px rgba(139, 92, 246, 0.4) !important; border-width: 3px !important; transform: translateY(-10px) scale(1.1) !important;' if is_active else 'box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;'}
        }}
        button[key="mode_btn_{idx}"]::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }}
        button[key="mode_btn_{idx}"]:hover::before {{
            left: 100%;
        }}
        button[key="mode_btn_{idx}"]:hover {{
            transform: translateY(-8px) scale(1.08) !important;
            box-shadow: 0 20px 50px rgba(139, 92, 246, 0.7), 0 0 40px rgba(139, 92, 246, 0.5) !important;
            border-width: 3px !important;
        }}
        button[key="mode_btn_{idx}"]:active {{
            transform: translateY(-4px) scale(1.05) !important;
        }}
        
        /* Responsive Design */
        @media (max-width: 1024px) {{
            button[key="mode_btn_{idx}"] {{
                min-height: 180px !important;
                padding: 1.5rem 1rem !important;
                font-size: 0.9rem !important;
            }}
        }}
        @media (max-width: 768px) {{
            button[key="mode_btn_{idx}"] {{
                min-height: 160px !important;
                padding: 1.25rem 0.75rem !important;
                font-size: 0.85rem !important;
            }}
        }}
        </style>
        """
        st.markdown(button_css, unsafe_allow_html=True)
        
        # Button to trigger mode change
        if st.button(button_label, key=f"mode_btn_{idx}", use_container_width=True, help=f"Select {mode_name}"):
            if st.session_state.current_mode != mode_name:
                st.session_state.current_mode = mode_name
                st.rerun()

mode = st.session_state.current_mode

# ============================================
# MODERN ACTIVE MODE INDICATOR
# ============================================
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(167, 139, 250, 0.15) 100%); 
    padding: 1.5rem 2rem; 
    border-radius: 20px; 
    border: 2px solid rgba(139, 92, 246, 0.4); 
    margin: 2rem auto 2.5rem auto; 
    max-width: 900px;
    box-shadow: 0 8px 32px rgba(139, 92, 246, 0.3), 0 0 20px rgba(139, 92, 246, 0.2);
    text-align: center;
    backdrop-filter: blur(10px);
">
    <p style="color: #ffffff; font-size: 1.2rem; margin: 0; font-weight: 700; font-family: 'Poppins', sans-serif;">
        <span style="font-size: 1.5rem; filter: drop-shadow(0 0 10px rgba(139, 92, 246, 0.8));">✨</span> 
        <strong style="background: linear-gradient(135deg, #a78bfa 0%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Active Mode:</strong> 
        <span style="font-size: 1.3rem; color: #f3e8ff; font-weight: 800;">{mode}</span>
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================
# OPTIMIZED GAME STATISTICS SECTION
# ============================================
if mode == "🎮 Guessing Game":
    st.markdown("""
    <div style="margin: 2rem 0 1.5rem 0; text-align: center;">
        <h3 style="color: #1a1a1a; font-weight: 700; margin-bottom: 0; font-size: 1.5rem;">
            🏆 Game Statistics
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    game_cols = st.columns(3, gap="medium")
    with game_cols[0]:
        st.markdown(f"""
        <div class="dynamic-stat" style="border-top-color: #51cf66 !important;">
            <div class="stat-number" style="
                background: linear-gradient(135deg, #51cf66, #69db7c);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">{st.session_state.game_score}</div>
            <div class="stat-label">Current Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with game_cols[1]:
        st.markdown(f"""
        <div class="dynamic-stat" style="border-top-color: #4dabf7 !important;">
            <div class="stat-number" style="
                background: linear-gradient(135deg, #4dabf7, #74c0fc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">{st.session_state.game_round}</div>
            <div class="stat-label">Rounds Played</div>
        </div>
        """, unsafe_allow_html=True)
    
    with game_cols[2]:
        if st.button("🔄 Reset Game", use_container_width=True, type="secondary"):
            st.session_state.game_score = 0
            st.session_state.game_round = 0
            st.session_state.game_history = []
            st.rerun()

# Load model
@st.cache_resource
def load_model():
    """Load the language detection model and components."""
    try:
        model, vectorizer, label_encoder = load_model_components()
        return model, vectorizer, label_encoder, None
    except FileNotFoundError as e:
        return None, None, None, str(e)

model, vectorizer, label_encoder, error = load_model()

# Main content
if error:
    st.error(f"❌ **Error loading model:** {error}")
    st.info("""
    **Please train the model first:**
    1. Run: `python train_model.py`
    2. Or use the Jupyter notebook
    3. Then refresh this app
    """)
else:
    # ============================================
    # GLOBAL LAYOUT SECTIONS (HERO + INFO)
    # ============================================
    render_hero_section()
    render_how_it_works_section()
    render_feature_section()

    # ============================================
    # MODE-BASED INTERFACE
    # ============================================
    if mode == "🎮 Guessing Game":
        # Optimized Game Section Header
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0 2.5rem 0;">
            <h2 style="color: #1a1a1a; font-weight: 700; margin-bottom: 0.75rem; font-size: 1.75rem;">
                🎮 Language Guessing Game
            </h2>
            <p style="color: #666666; font-size: 1rem; max-width: 700px; margin: 0 auto;">
                Challenge: Read the text below and guess the language before revealing the answer!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Game text examples
        game_texts = [
            ("Hello, how are you today? I hope you're doing well.", "English"),
            ("Bonjour, comment allez-vous? J'espère que vous allez bien.", "French"),
            ("Hola, ¿cómo estás? Espero que estés bien.", "Spanish"),
            ("Guten Tag, wie geht es dir? Ich hoffe, es geht dir gut.", "German"),
            ("Ciao, come stai? Spero che tu stia bene.", "Italian"),
            ("Ola, como voce esta? Espero que voce esteja bem.", "Portuguese"),
            ("Hallo, hoe gaat het? Ik hoop dat het goed met je gaat.", "Dutch"),
            ("Hej, hur mar du? Jag hoppas att du mar bra.", "Swedish"),
            ("Merhaba, nasilsin? Umarim iyisindir.", "Turkish"),
        ]
        
        if 'current_game_text' not in st.session_state or st.button("🎲 New Challenge", use_container_width=True):
            import random
            st.session_state.current_game_text, st.session_state.correct_answer = random.choice(game_texts)
            st.session_state.game_guessed = False
        
        if 'current_game_text' in st.session_state:
            st.markdown(f"""
            <div style="background: #ffffff; padding: 2rem; border-radius: 12px; border: 1px solid #e0e4e7; margin: 2rem 0; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <p style="font-size: 1.25rem; color: #000000; font-weight: 500; line-height: 1.6;">{st.session_state.current_game_text}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Language selection for guessing
            game_languages = list(set([t[1] for t in game_texts]))  # Get unique languages from game_texts
            guess_lang = st.selectbox(
                "🤔 What language is this?",
                ["Select..."] + sorted(game_languages),
                key="game_guess"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                reveal_button = st.button("🔍 Reveal Answer", type="primary", use_container_width=True)
            with col2:
                if st.button("✅ Submit Guess", use_container_width=True) and guess_lang != "Select...":
                    st.session_state.game_guessed = True
                    st.session_state.game_round += 1
                    if guess_lang == st.session_state.correct_answer:
                        st.session_state.game_score += 10
                        st.balloons()
                        st.success(f"🎉 Correct! You earned 10 points! Score: {st.session_state.game_score}")
                    else:
                        st.error(f"❌ Wrong! The correct answer was {st.session_state.correct_answer}. Score: {st.session_state.game_score}")
                    st.session_state.game_history.append({
                        'text': st.session_state.current_game_text[:30],
                        'guess': guess_lang,
                        'correct': st.session_state.correct_answer,
                        'score': 10 if guess_lang == st.session_state.correct_answer else 0
                    })
            
            if reveal_button:
                predicted_lang, confidence, all_probs, warning = predict_language(
                    st.session_state.current_game_text, model, vectorizer, label_encoder
                )
                
                st.markdown("---")
                st.markdown("### 🎯 Answer Revealed!")
                
                is_correct = predicted_lang == st.session_state.correct_answer
                if is_correct:
                    st.success(f"✅ Correct Answer: **{st.session_state.correct_answer}**")
                else:
                    st.warning(f"⚠️ Detected: **{predicted_lang}** | Correct: **{st.session_state.correct_answer}**")
                
                st.markdown(f"""
                <div class="prediction-card">
                    <div style="text-align: center;">
                        <span class="language-flag">{LANGUAGE_FLAGS.get(predicted_lang, '🌐')}</span>
                        <span class="language-badge">✨ {predicted_lang.upper()} ✨</span>
                        <p style="color: #333333; margin-top: 1rem; font-size: 1.1rem;">Confidence: {confidence:.1%}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Game history
        if st.session_state.game_history:
            st.markdown("---")
            st.markdown("### 📜 Game History")
            history_df = pd.DataFrame(st.session_state.game_history)
            st.dataframe(history_df, use_container_width=True, hide_index=True)
    
    elif mode == "📊 Batch Analysis":
        st.markdown("""
        <div class="dynamic-content">
            <h3 style="color: #000000; font-weight: 600; margin-bottom: 1rem;">Batch Language Analysis</h3>
            <p style="color: #333333; margin-bottom: 1.5rem;">Enter multiple texts (one per line) to analyze all at once:</p>
        </div>
        """, unsafe_allow_html=True)
        
        batch_input = st.text_area(
            "Batch Text Input",
            height=250,
            placeholder="Enter multiple texts, one per line:\n\nHello, how are you?\nBonjour, comment allez-vous?\nHola, ¿cómo estás?",
            help="Each line will be analyzed separately",
            key="batch_input"
        )
        
        if st.button("🔍 Analyze All", type="primary", use_container_width=True):
            if batch_input.strip():
                texts = [line.strip() for line in batch_input.split('\n') if line.strip()]
                
                st.markdown("---")
                st.markdown(f"### 📊 Results for {len(texts)} Texts")
                
                results = []
                for i, text in enumerate(texts, 1):
                    lang, conf, probs, warn = predict_language(text, model, vectorizer, label_encoder)
                    results.append({
                        'Text': text[:50] + "..." if len(text) > 50 else text,
                        'Language': lang,
                        'Confidence': f"{conf:.1%}",
                        'Flag': LANGUAGE_FLAGS.get(lang, '🌐')
                    })
                
                results_df = pd.DataFrame(results)
                
                # Display results with styling
                for idx, row in results_df.iterrows():
                    conf_value = float(row['Confidence'].strip('%')) / 100
                    conf_color = "#52c41a" if conf_value >= 0.8 else "#faad14" if conf_value >= 0.5 else "#ff4d4f"
                    
                    st.markdown(f"""
                    <div style="background: #ffffff; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 3px solid {conf_color}; box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <span style="font-size: 1.75rem;">{row['Flag']}</span>
                            <div style="flex: 1;">
                                <strong style="color: #000000; font-size: 1.1rem; font-weight: 600;">{row['Language']}</strong>
                                <p style="color: #333333; margin: 0.5rem 0; font-size: 0.95rem;">{row['Text']}</p>
                            </div>
                            <div style="color: {conf_color}; font-weight: 600; font-size: 1rem;">{row['Confidence']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please enter some text to analyze.")
    
    elif mode == "⚖️ Compare Texts":
        st.markdown("""
        <div class="dynamic-content">
            <h3 style="color: #000000; font-weight: 600; margin-bottom: 1.5rem;">Compare Two Texts</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <h4 style="color: #000000; font-weight: 600; margin-bottom: 0.5rem;">📝 Text 1</h4>
            """, unsafe_allow_html=True)
            text1 = st.text_area("", height=150, key="compare_text1", placeholder="Enter first text...")
        
        with col2:
            st.markdown("""
            <h4 style="color: #000000; font-weight: 600; margin-bottom: 0.5rem;">📝 Text 2</h4>
            """, unsafe_allow_html=True)
            text2 = st.text_area("", height=150, key="compare_text2", placeholder="Enter second text...")
        
        if st.button("🔍 Compare Languages", type="primary", use_container_width=True):
            if text1.strip() and text2.strip():
                lang1, conf1, probs1, warn1 = predict_language(text1, model, vectorizer, label_encoder)
                lang2, conf2, probs2, warn2 = predict_language(text2, model, vectorizer, label_encoder)
                
                st.markdown("---")
                st.markdown("### 📊 Comparison Results")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="prediction-card">
                        <h4 style="color: #000000; text-align: center; font-weight: 600;">Text 1</h4>
                        <div style="text-align: center; margin-top: 1rem;">
                            <span class="language-flag">{LANGUAGE_FLAGS.get(lang1, '🌐')}</span>
                            <span class="language-badge">{lang1}</span>
                            <p style="color: #333333; margin-top: 1rem;">Confidence: {conf1:.1%}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="prediction-card">
                        <h4 style="color: #000000; text-align: center; font-weight: 600;">Text 2</h4>
                        <div style="text-align: center; margin-top: 1rem;">
                            <span class="language-flag">{LANGUAGE_FLAGS.get(lang2, '🌐')}</span>
                            <span class="language-badge">{lang2}</span>
                            <p style="color: #333333; margin-top: 1rem;">Confidence: {conf2:.1%}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Comparison insights
                if lang1 == lang2:
                    st.success(f"✅ Both texts are detected as **{lang1}**!")
                else:
                    st.info(f"📊 Text 1: **{lang1}** ({conf1:.1%}) | Text 2: **{lang2}** ({conf2:.1%})")
                
                # Side-by-side probability comparison
                st.markdown("### 📈 Probability Comparison")
                comparison_df = pd.DataFrame({
                    'Language': list(set(list(probs1.keys()) + list(probs2.keys()))),
                    'Text 1': [probs1.get(lang, 0) for lang in set(list(probs1.keys()) + list(probs2.keys()))],
                    'Text 2': [probs2.get(lang, 0) for lang in set(list(probs1.keys()) + list(probs2.keys()))]
                })
                comparison_df = comparison_df.sort_values('Text 1', ascending=False).head(10)
                
                fig, ax = plt.subplots(figsize=(12, 6), facecolor='#ffffff')
                ax.set_facecolor('#ffffff')
                x = range(len(comparison_df))
                width = 0.35
                ax.barh([i - width/2 for i in x], comparison_df['Text 1'], width, label='Text 1', color='#5b9bd5')
                ax.barh([i + width/2 for i in x], comparison_df['Text 2'], width, label='Text 2', color='#7fb3d3')
                ax.set_yticks(x)
                ax.set_yticklabels(comparison_df['Language'], color='#2c3e50')
                ax.set_xlabel('Probability', color='#2c3e50', fontweight='500')
                ax.set_title('Language Probability Comparison', color='#2c3e50', fontweight='600', fontsize=14)
                ax.legend(loc='lower right')
                ax.tick_params(colors='#5a6c7d')
                ax.spines['bottom'].set_color('#e0e4e7')
                ax.spines['top'].set_color('#e0e4e7')
                ax.spines['right'].set_color('#e0e4e7')
                ax.spines['left'].set_color('#e0e4e7')
                ax.set_facecolor('#ffffff')
                plt.tight_layout()
                st.pyplot(fig, facecolor='#ffffff')
                plt.close(fig)
            else:
                st.warning("⚠️ Please enter both texts to compare.")
    
    elif mode == "🌐 Translator":
        # ============================================
        # OPTIMIZED TRANSLATOR SECTION
        # ============================================
        with st.container():
            st.markdown("""
            <div style="text-align: center; margin: 2rem 0 2.5rem 0;">
                <h2 style="color: #1a1a1a; font-weight: 700; margin-bottom: 0.75rem; font-size: 1.75rem;">
                    🌐 Language Translator
                </h2>
                <p style="color: #666666; font-size: 1rem; max-width: 700px; margin: 0 auto;">
                    Detect language automatically and translate to your desired language
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Text input - Optimized
            st.markdown("""
            <div style="margin: 0 0 1.5rem 0;">
                <h3 style="color: #1a1a1a; font-weight: 600; font-size: 1.25rem; text-align: center;">
                    📝 Enter Text to Translate
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            translate_input = st.text_area(
                " ",
                height=180,
                placeholder="Enter text in any language...\n\nExample: Hello, how are you? / Bonjour, comment allez-vous? / Hola, ¿cómo estás?",
                help="The language will be detected automatically",
                key="translate_input"
            )
            
            # Get supported languages for translation
            supported_langs = get_supported_languages()
            lang_list = sorted(supported_langs.keys())
            
            # Language selection - Optimized layout
            lang_col1, lang_col2 = st.columns(2, gap="large")
            
            with lang_col1:
                st.markdown("""
                <div style="margin-bottom: 0.75rem;">
                    <h4 style="color: #1a1a1a; font-weight: 600; font-size: 1.1rem;">
                        🔍 Source Language
                    </h4>
                </div>
                """, unsafe_allow_html=True)
                source_lang_option = st.radio(
                    "Source Language:",
                    ["Auto-detect", "Manual Selection"],
                    key="source_lang_option",
                    horizontal=True
                )
                
                if source_lang_option == "Manual Selection":
                    source_lang = st.selectbox(
                        "Select source language:",
                        ["Auto-detect"] + lang_list,
                        key="source_lang_select"
                    )
                    if source_lang == "Auto-detect":
                        source_lang = "auto"
                else:
                    source_lang = "auto"
                    st.info("💡 Language will be auto-detected when you click Translate")
            
            with lang_col2:
                st.markdown("""
                <div style="margin-bottom: 0.75rem;">
                    <h4 style="color: #1a1a1a; font-weight: 600; font-size: 1.1rem;">
                        🎯 Target Language
                    </h4>
                </div>
                """, unsafe_allow_html=True)
                target_lang = st.selectbox(
                    "Translate to:",
                    lang_list,
                    index=0,  # Default to English
                    key="target_lang_select"
                )
            
            # Action button - Centered
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1], gap="medium")
            with col_btn2:
                translate_button = st.button("🌐 Translate", type="primary", use_container_width=True)
        
            # ============================================
            # OPTIMIZED TRANSLATOR STATISTICS
            # ============================================
            if translate_input:
                word_count = len(translate_input.split())
                char_count = len(translate_input)
                line_count = len(translate_input.split('\n'))
                cleaned_count = len(translate_input.lower().strip())
                
                st.markdown("""
                <div style="margin: 2rem 0 1.25rem 0; text-align: center;">
                    <h4 style="color: #1a1a1a; font-weight: 600; margin-bottom: 0; font-size: 1.2rem;">
                        📊 Text Statistics
                    </h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Stats grid
                trans_stat_cols = st.columns(4, gap="medium")
                trans_stats = [
                    (char_count, "Characters", "#6366f1"),
                    (word_count, "Words", "#818cf8"),
                    (line_count, "Lines", "#a5b4fc"),
                    (cleaned_count, "Cleaned", "#c7d2fe")
                ]
                
                for idx, (value, label, color) in enumerate(trans_stats):
                    with trans_stat_cols[idx]:
                        st.markdown(f"""
                        <div class="dynamic-stat" style="border-top-color: {color} !important;">
                            <div class="stat-number" style="
                                background: linear-gradient(135deg, {color}, #a5b4fc);
                                -webkit-background-clip: text;
                                -webkit-text-fill-color: transparent;
                                background-clip: text;
                            ">{value}</div>
                            <div class="stat-label">{label}</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("---")
        
        # Translation result
        if translate_button:
            if not translate_input.strip():
                st.warning("⚠️ **Please enter some text to translate.**")
            else:
                with st.spinner("🌐 Translating text..."):
                    # Detect language if auto
                    if source_lang == "auto":
                        detected_lang, confidence, _, _ = predict_language(
                            translate_input, model, vectorizer, label_encoder
                        )
                        if detected_lang != "Unknown":
                            source_lang = detected_lang
                    
                    # Translate
                    translated_text, error = translate_text(
                        translate_input,
                        source_lang=source_lang,
                        target_lang=target_lang
                    )
                
                if error:
                    st.error(f"❌ **Translation Error:** {error}")
                else:
                    # ============================================
                    # OPTIMIZED TRANSLATION RESULT DISPLAY
                    # ============================================
                    st.markdown("""
                    <div style="margin: 3rem 0 2rem 0; text-align: center;">
                        <h2 style="color: #1a1a1a; font-weight: 700; margin-bottom: 0.5rem; font-size: 1.75rem;">
                            ✨ Translation Result
                        </h2>
                        <div style="width: 60px; height: 3px; background: linear-gradient(90deg, #6366f1, #818cf8); margin: 0 auto; border-radius: 2px;"></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display original and translated text side by side - Optimized
                    trans_col1, trans_col2 = st.columns(2, gap="large")
                    
                    with trans_col1:
                        st.markdown("""
                        <div style="margin-bottom: 0.75rem;">
                            <h4 style="color: #1a1a1a; font-weight: 600; font-size: 1.15rem;">
                                📝 Original Text
                            </h4>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); 
                            padding: 2rem; 
                            border-radius: 12px; 
                            border: 2px solid #e0e4e7; 
                            min-height: 200px; 
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                        ">
                            <p style="color: #000000; font-size: 1.05rem; line-height: 1.8; margin: 0;">{translate_input}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if source_lang != "auto" and source_lang != "Unknown":
                            flag = LANGUAGE_FLAGS.get(source_lang, '🌐')
                            st.markdown(f"""
                            <div style="text-align: center; margin-top: 0.75rem;">
                                <strong style="color: #5b9bd5; font-size: 0.95rem;">Source:</strong> 
                                <span style="font-size: 1.1rem;">{flag} {source_lang}</span>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with trans_col2:
                        st.markdown("""
                        <div style="margin-bottom: 0.75rem;">
                            <h4 style="color: #1a1a1a; font-weight: 600; font-size: 1.15rem;">
                                ✨ Translated Text
                            </h4>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #ffffff 0%, #f0f5ff 100%); 
                            padding: 2rem; 
                            border-radius: 12px; 
                            border: 2px solid #6366f1; 
                            min-height: 200px; 
                            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
                        ">
                            <p style="color: #000000; font-size: 1.05rem; line-height: 1.8; margin: 0;">{translated_text}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        flag = LANGUAGE_FLAGS.get(target_lang, '🌐')
                        st.markdown(f"""
                        <div style="text-align: center; margin-top: 0.75rem;">
                            <strong style="color: #6366f1; font-size: 0.95rem;">Target:</strong> 
                            <span style="font-size: 1.1rem;">{flag} {target_lang}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Copy button functionality
                    st.markdown("---")
                    st.markdown("### 📋 Copy Translation")
                    st.code(translated_text, language=None)
                    
                    # Additional info
                    if source_lang != "auto" and source_lang != "Unknown":
                        st.info(f"💡 **Translation:** {source_lang} → {target_lang}")
    
    else:  # Normal Detection Mode
        # ============================================
        # OPTIMIZED TEXT INPUT SECTION
        # ============================================
        with st.container():
            st.markdown("""
            <div style="margin: 2rem 0 1.5rem 0; text-align: center;">
                <h3 style="color: #1a1a1a; font-weight: 700; margin-bottom: 0.5rem; font-size: 1.5rem;">
                    ✍️ Enter Your Text
                </h3>
                <p style="color: #666666; font-size: 0.95rem; margin: 0;">
                    Type or paste text in any supported language
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Example dropdown - Optimized layout
            example_texts = {
                "Select example...": "",
                "English": "Hello, how are you today? I hope you're doing well.",
                "French": "Bonjour, comment allez-vous? J'espère que vous allez bien.",
                "Spanish": "Hola, ¿cómo estás? Espero que estés bien.",
                "German": "Guten Tag, wie geht es dir? Ich hoffe, es geht dir gut.",
                "Italian": "Ciao, come stai? Spero che tu stia bene.",
                "Portuguese": "Ola, como voce esta? Espero que voce esteja bem.",
                "Dutch": "Hallo, hoe gaat het? Ik hoop dat het goed met je gaat.",
                "Swedish": "Hej, hur mar du? Jag hoppas att du mar bra.",
                "Turkish": "Merhaba, nasilsin? Umarim iyisindir.",
                "Greek": "Geia sas, pos eiste? Elpizo na eiste kala.",
                "Danish": "Hej, hvordan har du det? Jeg haber du har det godt."
            }
            
            # Centered example dropdown
            col_example1, col_example2, col_example3 = st.columns([2, 5, 2])
            with col_example2:
                selected_example = st.selectbox(
                    "📝 Quick Examples",
                    options=list(example_texts.keys()),
                    key="example_dropdown",
                    help="Quick select a language example",
                    label_visibility="visible"
                )
            
            # Text input - Optimized
            initial_value = ""
            if selected_example and selected_example != "Select example..." and example_texts[selected_example]:
                initial_value = example_texts[selected_example]
            
            text_input = st.text_area(
                " ",
                height=160,
                value=initial_value,
                placeholder="✨ Type or paste text here to detect its language...",
                help="Enter text in any of the supported languages",
                key="main_text_input"
            )
            
            # Action buttons - Optimized layout
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1], gap="medium")
            with col_btn2:
                col_detect, col_clear = st.columns(2, gap="small")
                with col_detect:
                    detect_button = st.button("🔍 Detect Language", type="primary", use_container_width=True)
                with col_clear:
                    clear_button = st.button("🗑️ Clear", type="secondary", use_container_width=True)
        
            # ============================================
            # OPTIMIZED TEXT STATISTICS SECTION
            # ============================================
            if text_input:
                word_count = len(text_input.split())
                char_count = len(text_input)
                line_count = len(text_input.split('\n'))
                cleaned = text_input.lower().strip()
                cleaned_count = len(cleaned)
                
                st.markdown("""
                <div style="margin: 2rem 0 1.25rem 0; text-align: center;">
                    <h4 style="color: #1a1a1a; font-weight: 600; margin-bottom: 0; font-size: 1.2rem;">
                        📊 Text Statistics
                    </h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Optimized stats grid with better spacing
                stat_cols = st.columns(4, gap="medium")
                stats_data = [
                    (char_count, "Characters", "#6366f1"),
                    (word_count, "Words", "#818cf8"),
                    (line_count, "Lines", "#a5b4fc"),
                    (cleaned_count, "Cleaned", "#c7d2fe")
                ]
                
                for idx, (value, label, color) in enumerate(stats_data):
                    with stat_cols[idx]:
                        st.markdown(f"""
                        <div class="dynamic-stat" style="
                            margin: 0 auto; 
                            max-width: 100%; 
                            border-top-color: {color} !important;
                        ">
                            <div class="stat-number" style="
                                background: linear-gradient(135deg, {color}, #a5b4fc);
                                -webkit-background-clip: text;
                                -webkit-text-fill-color: transparent;
                                background-clip: text;
                            ">{value}</div>
                            <div class="stat-label">{label}</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        if clear_button:
            st.session_state.clear()
            st.rerun()
        
        # Prediction section
        if detect_button:
            if not text_input.strip():
                st.warning("⚠️ **Please enter some text to detect the language.**")
            else:
                with st.spinner("🔍 Analyzing text with AI..."):
                    predicted_lang, confidence, all_probs, warning = predict_language(
                        text_input, model, vectorizer, label_encoder
                    )
                
                # ============================================
                # OPTIMIZED RESULTS SECTION
                # ============================================
                st.markdown("""
                <div style="margin: 3rem 0 2rem 0; text-align: center;">
                    <h2 style="color: #1a1a1a; font-weight: 700; margin-bottom: 0.5rem; font-size: 1.75rem;">
                        ✨ Detection Results
                    </h2>
                    <div style="width: 60px; height: 3px; background: linear-gradient(90deg, #6366f1, #818cf8); margin: 0 auto; border-radius: 2px;"></div>
                </div>
                """, unsafe_allow_html=True)
                
                if warning:
                    st.warning(f"⚠️ {warning}")
                
                if predicted_lang == "Unknown":
                    st.error("❌ **Unable to detect language.**")
                    st.info("💡 The model works best with Latin scripts (English, French, Spanish, German, Italian, etc.).")
                else:
                    # Special warnings
                    if predicted_lang == "Russian" and confidence < 0.5:
                        st.warning("⚠️ **Note:** Russian detection is very limited (~10% accuracy) due to Cyrillic script preprocessing.")
                    
                    # Check for Russian misclassification
                    if predicted_lang == "Turkish" and all_probs:
                        russian_patterns = ['privet', 'zdravstvuyte', 'spasibo', 'kak dela', 'russkiy', 'izuchayu', 
                                           'pozhivaete', 'mozhet', 'khorosho', 'pochemu', 'gde', 'kogda', 'kto', 'chto',
                                           'kak vy', 'ya', 'vy', 'menya', 'tebya', 'nas', 'vas']
                        text_lower = text_input.lower()
                        has_russian_patterns = any(pattern in text_lower for pattern in russian_patterns)
                        
                        if has_russian_patterns:
                            russian_prob = all_probs.get('Russian', 0)
                            st.warning(f"⚠️ **Possible misclassification:** Russian text detected but classified as Turkish. Russian probability: {russian_prob:.2%}")
                    
                    # ============================================
                    # OPTIMIZED MAIN PREDICTION DISPLAY
                    # ============================================
                    with st.container():
                        st.markdown(f"""
                        <div class="prediction-card dynamic-content" style="max-width: 700px; margin: 0 auto 2rem auto;">
                            <div style="text-align: center; padding: 1.5rem;">
                                <div style="font-size: 4rem; margin-bottom: 1rem;">{LANGUAGE_FLAGS.get(predicted_lang, '🌐')}</div>
                                <span class="language-badge" style="font-size: 1.5rem; padding: 1rem 2rem;">{predicted_lang.upper()}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # ============================================
                        # OPTIMIZED CONFIDENCE DISPLAY
                        # ============================================
                        col1, col2, col3 = st.columns([1, 3, 1])
                        with col2:
                            # Determine confidence level and styling
                            if confidence >= 0.8:
                                conf_class = "confidence-high"
                                conf_emoji = "🟢"
                                conf_color = "#10b981"
                                conf_bg = "linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)"
                            elif confidence >= 0.5:
                                conf_class = "confidence-medium"
                                conf_emoji = "🟡"
                                conf_color = "#f59e0b"
                                conf_bg = "linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)"
                            else:
                                conf_class = "confidence-low"
                                conf_emoji = "🔴"
                                conf_color = "#ef4444"
                                conf_bg = "linear-gradient(135deg, #fee2e2 0%, #fecaca 100%)"
                            
                            # Enhanced confidence display
                            st.markdown(f"""
                            <div style="
                                background: {conf_bg};
                                padding: 1.5rem 2rem;
                                border-radius: 16px;
                                border: 2px solid {conf_color};
                                margin: 1.5rem 0;
                                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                                text-align: center;
                            ">
                                <p style="
                                    font-size: 1.2rem; 
                                    margin-bottom: 0.75rem; 
                                    color: #1a1a1a; 
                                    font-weight: 700;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    gap: 0.5rem;
                                ">
                                    <span style="font-size: 1.5rem;">{conf_emoji}</span>
                                    <span>Confidence Level</span>
                                </p>
                                <p class="{conf_class}" style="
                                    font-size: 2rem;
                                    font-weight: 800;
                                    color: {conf_color};
                                    margin: 0;
                                    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
                                ">{confidence:.1%}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Enhanced progress bar
                            st.markdown(f"""
                            <div style="
                                background: #f3f4f6;
                                height: 12px;
                                border-radius: 10px;
                                overflow: hidden;
                                margin: 1rem 0;
                                box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
                            ">
                                <div style="
                                    background: linear-gradient(90deg, {conf_color}, {conf_color}dd);
                                    height: 100%;
                                    width: {confidence*100}%;
                                    transition: width 0.5s ease;
                                    border-radius: 10px;
                                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                                "></div>
                            </div>
                            """, unsafe_allow_html=True)
                
                        # ============================================
                        # OPTIMIZED PROBABILITY DISTRIBUTION
                        # ============================================
                        if predicted_lang != "Unknown" and all_probs:
                            st.markdown("""
                            <div style="margin: 3rem 0 2rem 0; text-align: center;">
                                <h2 style="color: #1a1a1a; font-weight: 700; margin-bottom: 0.5rem; font-size: 1.5rem;">
                                    📊 Detailed Analysis
                                </h2>
                                <div style="width: 60px; height: 3px; background: linear-gradient(90deg, #6366f1, #818cf8); margin: 0 auto; border-radius: 2px;"></div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            prob_df = pd.DataFrame([
                                {"Language": lang, "Probability": prob}
                                for lang, prob in all_probs.items()
                            ])
                            
                            # Top 5 languages - Optimized display
                            st.markdown("""
                            <div style="margin: 1.5rem 0 1rem 0;">
                                <h3 style="color: #1a1a1a; font-weight: 600; font-size: 1.25rem; text-align: center;">
                                    🏆 Top 5 Most Likely Languages
                                </h3>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            top_5 = prob_df.head(5)
                            
                            for idx, row in top_5.iterrows():
                                lang_name = row['Language']
                                prob = row['Probability']
                                flag = LANGUAGE_FLAGS.get(lang_name, '🌐')
                                
                                # Enhanced color scheme based on rank
                                if idx == 0:
                                    bg_color = "linear-gradient(135deg, #e8f4f8 0%, #d1e7f0 100%)"
                                    border_color = "#5b9bd5"
                                    text_color = "#1a1a1a"
                                    rank_badge = "🥇"
                                elif idx == 1:
                                    bg_color = "linear-gradient(135deg, #f1f3f5 0%, #e9ecef 100%)"
                                    border_color = "#7fb3d3"
                                    text_color = "#1a1a1a"
                                    rank_badge = "🥈"
                                elif idx == 2:
                                    bg_color = "linear-gradient(135deg, #fff5e6 0%, #ffe6cc 100%)"
                                    border_color = "#ffa94d"
                                    text_color = "#1a1a1a"
                                    rank_badge = "🥉"
                                else:
                                    bg_color = "#ffffff"
                                    border_color = "#e0e4e7"
                                    text_color = "#5a6c7d"
                                    rank_badge = f"#{idx+1}"
                                
                                st.markdown(f"""
                                <div style="
                                    background: {bg_color}; 
                                    padding: 1.25rem 1.5rem; 
                                    border-radius: 12px; 
                                    margin: 0.75rem 0; 
                                    border-left: 4px solid {border_color}; 
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                                ">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                                            <span style="font-size: 1.25rem;">{rank_badge}</span>
                                            <span style="font-size: 1.75rem;">{flag}</span>
                                            <strong style="font-size: 1.15rem; color: {text_color}; font-weight: 700;">{lang_name}</strong>
                                        </div>
                                        <div style="
                                            font-size: 1.3rem; 
                                            font-weight: 800; 
                                            color: {border_color};
                                            background: rgba(255,255,255,0.7);
                                            padding: 0.5rem 1rem;
                                            border-radius: 8px;
                                        ">{prob:.1%}</div>
                                    </div>
                                    <div style="margin-top: 0.75rem;">
                                        <div style="background: #f0f2f5; height: 10px; border-radius: 6px; overflow: hidden; box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);">
                                            <div style="
                                                background: linear-gradient(90deg, {border_color}, {border_color}dd); 
                                                height: 100%; 
                                                width: {prob*100}%; 
                                                transition: width 0.5s ease;
                                                border-radius: 6px;
                                                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
                                            "></div>
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                        
                            # Language Probability Chart - Optimized
                            st.markdown("""
                            <div style="margin: 2.5rem 0 1rem 0;">
                                <h3 style="color: #1a1a1a; font-weight: 600; font-size: 1.25rem; text-align: center;">
                                    📈 Language Probability Chart
                                </h3>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Enhanced chart with better styling
                            fig, ax = plt.subplots(figsize=(14, 8), facecolor='#ffffff')
                            ax.set_facecolor('#ffffff')
                            prob_df_sorted = prob_df.sort_values('Probability', ascending=True)
                            
                            # Enhanced color gradient based on probability
                            bar_colors = []
                            for prob in prob_df_sorted['Probability']:
                                if prob > 0.5:
                                    bar_colors.append('#6366f1')  # Primary indigo
                                elif prob > 0.2:
                                    bar_colors.append('#818cf8')  # Secondary indigo
                                elif prob > 0.1:
                                    bar_colors.append('#a5b4fc')  # Light indigo
                                else:
                                    bar_colors.append('#c7d2fe')  # Very light indigo
                            
                            bars = ax.barh(
                                prob_df_sorted['Language'], 
                                prob_df_sorted['Probability'], 
                                color=bar_colors, 
                                edgecolor='#e0e4e7', 
                                linewidth=1,
                                height=0.7
                            )
                            
                            # Enhanced chart styling
                            ax.set_xlabel('Probability', fontsize=14, fontweight='600', color='#1a1a1a', labelpad=10)
                            ax.set_title('Language Detection Probabilities', fontsize=18, fontweight='700', pad=25, color='#1a1a1a')
                            ax.set_xlim(0, 1)
                            ax.grid(axis='x', alpha=0.2, linestyle='--', color='#d1d5db', linewidth=1)
                            ax.tick_params(colors='#4b5563', labelsize=11, width=0.5)
                            
                            # Enhanced spine styling
                            for spine in ax.spines.values():
                                spine.set_color('#e5e7eb')
                                spine.set_linewidth(1.5)
                            
                            # Enhanced value labels
                            for i, (bar, (lang, prob)) in enumerate(zip(bars, zip(prob_df_sorted['Language'], prob_df_sorted['Probability']))):
                                if prob > 0.01:
                                    ax.text(
                                        prob + 0.015, i, f'{prob:.1%}', 
                                        va='center', 
                                        fontweight='600', 
                                        color='#1a1a1a', 
                                        fontsize=10,
                                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none')
                                    )
                            
                            plt.tight_layout()
                            st.pyplot(fig, facecolor='#ffffff')
                            plt.close(fig)
                        
                        # Detailed probabilities (collapsible)
                        with st.expander("📋 View All Language Probabilities (Detailed)"):
                            for idx, row in prob_df.iterrows():
                                lang_name = row['Language']
                                prob = row['Probability']
                                flag = LANGUAGE_FLAGS.get(lang_name, '🌐')
                                st.markdown(f"{flag} **{lang_name}**: {prob:.4f} ({prob*100:.2f}%)")
    
    # Examples section removed - now using dropdown above text input
    
    # Model Info - Collapsible (moved to bottom)
    st.markdown("---")
    with st.expander("ℹ️ Model Information & Tips", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📊 Model Details
            - **Algorithm:** Multinomial Naive Bayes
            - **Features:** Bag-of-Words + n-grams
            - **Accuracy:** ~85%
            - **Training Data:** 51,642 samples
            """)
        
        with col2:
            st.markdown("""
            ### 💡 Tips for Best Results
            - Works best with **Latin scripts**
            - For non-Latin scripts, use **transliterated** versions
            - Longer text = better accuracy
            - Russian detection is limited (~10%)
            """)
        
        # Supported languages grid - Updated comprehensive list
        st.markdown("### 🌍 Supported Detection Languages")
        languages = [
            # Major European Languages
            "English", "French", "Spanish", "German", "Italian", 
            "Portuguese", "Dutch", "Swedish", "Turkish", "Danish",
            "Greek", "Polish", "Czech", "Romanian", "Hungarian",
            "Finnish", "Norwegian", "Ukrainian", "Bulgarian", "Croatian",
            "Serbian", "Slovak", "Slovenian", "Lithuanian", "Latvian",
            "Estonian", "Icelandic", "Irish", "Welsh", "Maltese",
            # Asian Languages (Romanized)
            "Hindi", "Arabic", "Tamil", "Malayalam", "Kannada",
            "Telugu", "Bengali", "Marathi", "Gujarati", "Punjabi",
            "Urdu", "Nepali", "Thai", "Vietnamese", "Indonesian",
            "Malay", "Filipino", "Tagalog", "Japanese", "Chinese",
            "Korean", "Russian",
            # Middle Eastern & African Languages
            "Hebrew", "Persian", "Swahili", "Afrikaans", "Zulu",
            "Yoruba", "Hausa", "Amharic",
            # Other Languages
            "Esperanto", "Basque", "Catalan", "Galician", "Armenian",
            "Georgian", "Azerbaijani", "Kazakh", "Uzbek", "Albanian"
        ]
        
        lang_cols = st.columns(6)
        for idx, lang in enumerate(languages):
            with lang_cols[idx % 6]:
                flag = LANGUAGE_FLAGS.get(lang, '🌐')
                st.markdown(f"{flag} {lang}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <h3 style="color: #000000; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem;">Language Detector</h3>
        <p style="color: #333333; font-size: 0.95rem;">Built with Streamlit, scikit-learn, and NLP techniques</p>
        <p style="color: #666666; font-size: 0.85rem; margin-top: 0.5rem;"><strong>Model:</strong> Multinomial Naive Bayes | <strong>Features:</strong> Bag-of-Words with n-grams</p>
        <p style="margin-top: 1rem; color: #333333; font-size: 0.9rem; font-weight: 500;">70+ Detection Languages • 500+ Translation Languages • AI-Powered</p>
    </div>
    """, unsafe_allow_html=True)
