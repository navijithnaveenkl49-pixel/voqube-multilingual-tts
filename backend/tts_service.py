import edge_tts
import uuid
import os
import asyncio
from deep_translator import GoogleTranslator

# Map combinations of Language and VoiceType (Male/Female) to Edge TTS neural voices
# Optimized for high-quality Indian and international languages.
LANGUAGE_VOICES = {
    "English": {"Female": "en-US-AriaNeural", "Male": "en-US-GuyNeural"},
    "Hindi": {"Female": "hi-IN-SwaraNeural", "Male": "hi-IN-MadhurNeural"},
    "Tamil": {"Female": "ta-IN-PallaviNeural", "Male": "ta-IN-ValluvarNeural"},
    "Malayalam": {"Female": "ml-IN-SobhanaNeural", "Male": "ml-IN-MidhunNeural"},
    "Telugu": {"Female": "te-IN-ShrutiNeural", "Male": "te-IN-MohanNeural"},
    "Kannada": {"Female": "kn-IN-SapnaNeural", "Male": "kn-IN-GaganNeural"},
    "Bengali": {"Female": "bn-IN-TanishaaNeural", "Male": "bn-IN-BashkarNeural"},
    "Marathi": {"Female": "mr-IN-AarohiNeural", "Male": "mr-IN-ManoharNeural"},
    "Gujarati": {"Female": "gu-IN-DhwaniNeural", "Male": "gu-IN-NiranjanNeural"},
    "Punjabi": {"Female": "pa-IN-OjasNeural", "Male": "pa-IN-AmanNeural"},
    "Spanish": {"Female": "es-ES-ElviraNeural", "Male": "es-ES-AlvaroNeural"},
    "French": {"Female": "fr-FR-DeniseNeural", "Male": "fr-FR-HenriNeural"},
    "German": {"Female": "de-DE-KatjaNeural", "Male": "de-DE-ConradNeural"},
    "Urdu": {"Female": "ur-PK-UzmaNeural", "Male": "ur-PK-AsadNeural"},
    "Japanese": {"Female": "ja-JP-NanamiNeural", "Male": "ja-JP-KeitaNeural"},
    "Korean": {"Female": "ko-KR-SunHiNeural", "Male": "ko-KR-InJoonNeural"},
    "Chinese": {"Female": "zh-CN-XiaoxiaoNeural", "Male": "zh-CN-YunxiNeural"},
}

# Mapping for Translation (Deep Translator / Google Translate codes)
LANG_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Malayalam": "ml",
    "Telugu": "te",
    "Kannada": "kn",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Urdu": "ur",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN",
}

STORAGE_DIR = "storage/audio"
os.makedirs(STORAGE_DIR, exist_ok=True)

async def translate_text(text: str, target_lang: str) -> str:
    """
    Translates text from English to the target language.
    Splits long text into chunks to avoid API limits (usually ~5000 chars).
    """
    if target_lang == "English" or not text.strip():
        return text
    
    dest_code = LANG_MAP.get(target_lang, "en")
    try:
        # Revert to 'auto' for source but keep target as dest_code
        translator = GoogleTranslator(source='auto', target=dest_code)
        
        # Aggressive splitting logic: by paragraphs, then sentences, then character limit
        import re
        
        sentences = re.split(r'(?<=[.!?]) +', text.replace('\n', ' '))
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # If a single sentence is too long, we must split it by length
            if len(sentence) > 700:
                # Flush current
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                # Split large sentence
                for i in range(0, len(sentence), 700):
                    chunks.append(sentence[i:i+700].strip())
            elif len(current_chunk) + len(sentence) < 700:
                current_chunk += (sentence + " ")
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        print(f"DEBUG: Translating {len(text)} chars in {len(chunks)} chunks to {target_lang} ({dest_code})")
        
        translated_chunks = []
        for i, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
            try:
                # Small delay to avoid Google rate limits
                if i > 0:
                    await asyncio.sleep(0.5)
                
                translated = await asyncio.to_thread(translator.translate, chunk)
                
                # Check for empty or failed result (Google sometimes returns original or empty)
                if not translated or (translated == chunk and target_lang != "English" and len(chunk) > 3):
                   print(f"DEBUG: Chunk {i+1} translation failed or returned original. Attempting retry...")
                   await asyncio.sleep(0.5)
                   translated = await asyncio.to_thread(GoogleTranslator(source='en', target=dest_code).translate, chunk)
                
                translated_chunks.append(translated)
                # print(f"DEBUG: Chunk {i+1} translated ({len(chunk)} -> {len(translated)})")
            except Exception as chunk_error:
                print(f"DEBUG: Chunk {i+1} failed: {chunk_error}")
                translated_chunks.append(chunk) # Fallback to original
            
        full_translation = " ".join(translated_chunks)
        print(f"DEBUG: Translation complete. Final length: {len(full_translation)}")
        return full_translation
    except Exception as e:
        print(f"Translation Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return text 

async def generate_speech(text: str, language: str, voice_type: str = "Female") -> str:
    """
    Generates high-quality neural speech using Microsoft Edge-TTS.
    """
    try:
        # Check if voice_type is already a full neural voice name (contains '-Neural')
        if "Neural" in voice_type:
            voice_name = voice_type
        # Otherwise, look it up in our language registry
        elif language in LANGUAGE_VOICES:
            voice_name = LANGUAGE_VOICES[language].get(voice_type, LANGUAGE_VOICES[language]["Female"])
        else:
            # Default to English Female if nothing matches
            voice_name = "en-US-AriaNeural"

        print(f"DEBUG: Generating speech for {len(text)} characters using voice: {voice_name}")

        # Unique filename using UUID
        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(STORAGE_DIR, filename)

        # Initialize Edge TTS Communication
        communicate = edge_tts.Communicate(text, voice_name)
        
        # Save to MP3 format
        await communicate.save(filepath)
        print(f"DEBUG: Speech generated and saved to {filepath}")

        return filepath
    except Exception as e:
        print(f"TTS Generation Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise e
