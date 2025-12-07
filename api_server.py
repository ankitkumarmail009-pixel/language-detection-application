"""
FastAPI backend server for Language Detection Mobile App.
Serves the ML model via REST API endpoints.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import joblib
import os
from utils import predict_language, load_model_components, translate_text, get_supported_languages

# Initialize FastAPI app
app = FastAPI(
    title="Language Detection API",
    description="REST API for language detection and translation",
    version="1.0.0"
)

# Enable CORS for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your mobile app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model components
model = None
vectorizer = None
label_encoder = None

# Request/Response models
class TextInput(BaseModel):
    text: str

class LanguageDetectionResponse(BaseModel):
    language: str
    confidence: float
    probabilities: Dict[str, float]
    warning: Optional[str] = None

class TranslationRequest(BaseModel):
    text: str
    source_lang: Optional[str] = "auto"
    target_lang: str = "en"

class TranslationResponse(BaseModel):
    translated_text: str
    source_language: Optional[str] = None
    target_language: str
    error: Optional[str] = None

class BatchDetectionRequest(BaseModel):
    texts: List[str]

class BatchDetectionResponse(BaseModel):
    results: List[Dict[str, any]]

# Load model on startup
@app.on_event("startup")
async def load_model():
    """Load the ML model and components when the server starts."""
    global model, vectorizer, label_encoder
    try:
        model, vectorizer, label_encoder = load_model_components()
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "message": "Language Detection API",
        "version": "1.0.0",
        "endpoints": {
            "/detect": "POST - Detect language of text",
            "/translate": "POST - Translate text",
            "/batch-detect": "POST - Detect languages for multiple texts",
            "/languages": "GET - Get supported languages",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if model is None or vectorizer is None or label_encoder is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}

@app.post("/detect", response_model=LanguageDetectionResponse)
async def detect_language(input_data: TextInput):
    """
    Detect the language of input text.
    
    Args:
        input_data: TextInput containing the text to analyze
    
    Returns:
        LanguageDetectionResponse with detected language, confidence, and probabilities
    """
    if model is None or vectorizer is None or label_encoder is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please check server logs.")
    
    if not input_data.text or not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        language, confidence, probabilities, warning = predict_language(
            input_data.text, model, vectorizer, label_encoder
        )
        
        return LanguageDetectionResponse(
            language=language,
            confidence=float(confidence),
            probabilities={k: float(v) for k, v in probabilities.items()},
            warning=warning if warning else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")

@app.post("/translate", response_model=TranslationResponse)
async def translate(input_data: TranslationRequest):
    """
    Translate text from source language to target language.
    
    Args:
        input_data: TranslationRequest with text, source_lang, and target_lang
    
    Returns:
        TranslationResponse with translated text
    """
    if not input_data.text or not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        # Auto-detect source language if needed
        source_lang = input_data.source_lang
        if source_lang == "auto" and model is not None:
            detected_lang, _, _, _ = predict_language(
                input_data.text, model, vectorizer, label_encoder
            )
            if detected_lang != "Unknown":
                source_lang = detected_lang
        
        translated_text, error = translate_text(
            input_data.text,
            source_lang=source_lang,
            target_lang=input_data.target_lang
        )
        
        if error:
            return TranslationResponse(
                translated_text="",
                source_language=source_lang if source_lang != "auto" else None,
                target_language=input_data.target_lang,
                error=error
            )
        
        return TranslationResponse(
            translated_text=translated_text,
            source_language=source_lang if source_lang != "auto" else None,
            target_language=input_data.target_lang,
            error=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")

@app.post("/batch-detect", response_model=BatchDetectionResponse)
async def batch_detect(input_data: BatchDetectionRequest):
    """
    Detect languages for multiple texts at once.
    
    Args:
        input_data: BatchDetectionRequest with list of texts
    
    Returns:
        BatchDetectionResponse with results for each text
    """
    if model is None or vectorizer is None or label_encoder is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if not input_data.texts:
        raise HTTPException(status_code=400, detail="Texts list cannot be empty")
    
    results = []
    for text in input_data.texts:
        try:
            language, confidence, probabilities, warning = predict_language(
                text, model, vectorizer, label_encoder
            )
            results.append({
                "text": text[:100] + "..." if len(text) > 100 else text,
                "language": language,
                "confidence": float(confidence),
                "probabilities": {k: float(v) for k, v in list(probabilities.items())[:5]},  # Top 5
                "warning": warning if warning else None
            })
        except Exception as e:
            results.append({
                "text": text[:100] + "..." if len(text) > 100 else text,
                "language": "Unknown",
                "confidence": 0.0,
                "probabilities": {},
                "warning": f"Error: {str(e)}"
            })
    
    return BatchDetectionResponse(results=results)

@app.get("/languages")
async def get_languages():
    """
    Get list of supported languages for detection and translation.
    
    Returns:
        Dictionary with supported languages for detection and translation
    """
    detection_languages = []
    if label_encoder is not None:
        detection_languages = label_encoder.classes_.tolist()
    
    translation_languages = get_supported_languages()
    
    return {
        "detection_languages": detection_languages,
        "translation_languages": list(translation_languages.keys()),
        "translation_codes": translation_languages
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

