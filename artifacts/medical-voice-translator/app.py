"""
Medical Voice Translator
Translates medical phrases between English and Spanish,
generates audio with gTTS, and optionally accepts voice input.
"""

import io
import base64
import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS

# ─── Optional: voice input via SpeechRecognition ───────────────────────────
try:
    import speech_recognition as sr
    VOICE_INPUT_AVAILABLE = True
except ImportError:
    VOICE_INPUT_AVAILABLE = False


# ─── Translation helpers ────────────────────────────────────────────────────

def translate_text(text: str, direction: str) -> str:
    """
    Translate text between English and Spanish.
    direction: 'en->es' or 'es->en'
    Returns the translated string, or an error message.
    """
    if not text.strip():
        return ""
    src, tgt = direction.split("->")
    try:
        result = GoogleTranslator(source=src, target=tgt).translate(text)
        return result
    except Exception as e:
        return f"Translation error: {e}"


# ─── Text-to-speech helpers ─────────────────────────────────────────────────

def generate_audio_b64(text: str, lang: str) -> str:
    """
    Convert text to speech using gTTS and return a base64-encoded MP3 string.
    lang: 'es' for Spanish, 'en' for English
    """
    tts = gTTS(text=text, lang=lang)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


def play_audio(text: str, lang: str):
    """
    Render an HTML audio player for the given text in the chosen language.
    """
    if not text.strip():
        st.warning("No text to play.")
        return
    b64 = generate_audio_b64(text, lang)
    audio_html = f"""
    <audio controls autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)


# ─── Voice input helper ──────────────────────────────────────────────────────

def listen_from_microphone(language: str) -> str:
    """
    Capture audio from the microphone and return the recognised text.
    language: 'en-US' or 'es-ES'
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening… speak now.")
        audio = recognizer.listen(source, timeout=5)
    try:
        return recognizer.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"


# ─── Preset medical phrases ──────────────────────────────────────────────────

MEDICAL_PHRASES = [
    "Where is your pain?",
    "Do you have allergies?",
    "Rate your pain from 1 to 10",
    "Are you taking any medication?",
]


# ─── App layout ──────────────────────────────────────────────────────────────

st.set_page_config(page_title="Medical Voice Translator", page_icon="🩺")
st.title("🩺 Medical Voice Translator")
st.caption("Translate medical phrases between English and Spanish — with audio playback.")

# ── Direction selector ──────────────────────────────────────────────────────
st.subheader("Translation Direction")
col1, col2 = st.columns(2)
with col1:
    en_to_es = st.button("🇺🇸 English → Spanish", use_container_width=True)
with col2:
    es_to_en = st.button("🇪🇸 Spanish → English", use_container_width=True)

# Persist direction in session state
if "direction" not in st.session_state:
    st.session_state.direction = "en->es"

if en_to_es:
    st.session_state.direction = "en->es"
if es_to_en:
    st.session_state.direction = "es->en"

src_lang_label = "English" if st.session_state.direction == "en->es" else "Spanish"
tgt_lang_label = "Spanish" if st.session_state.direction == "en->es" else "English"
tgt_lang_code  = "es"      if st.session_state.direction == "en->es" else "en"
mic_lang_code  = "en-US"   if st.session_state.direction == "en->es" else "es-ES"

st.info(f"**Mode:** {src_lang_label} → {tgt_lang_label}")

# ── Text input ───────────────────────────────────────────────────────────────
st.subheader("Enter Text")

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

user_input = st.text_area(
    f"Type in {src_lang_label}:",
    value=st.session_state.input_text,
    height=120,
    placeholder=f"Enter {src_lang_label} text here…",
)

# ── Voice input (optional) ────────────────────────────────────────────────────
if VOICE_INPUT_AVAILABLE:
    
    '''
    if st.button("🎙️ Record Voice Input"):
       spoken = listen_from_microphone(mic_lang_code)
       st.session_state.input_text = spoken
       st.rerun()

    '''
    audio = st.audio_input("Record your voice Input")
    if audio:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio) as source:
            audio_data = recognizer.record(source)
        try:
            spoken = recognizer.recognize_google(audio_data, language=mic_lang_code)
            st.session_state.input_text = spoken
            st.rerun()
        except sr.UnknownValueError:
            st.error("Could not understand audio, please try again")
        except sr.RequestError:
            st.error("Speech recognition service unavailable")

# ── Translate button ─────────────────────────────────────────────────────────
if st.button("🔄 Translate", type="primary"):
    if user_input.strip():
        translated = translate_text(user_input, st.session_state.direction)
        st.session_state.translated = translated
        st.session_state.tgt_lang   = tgt_lang_code
    else:
        st.warning("Please enter some text before translating.")

# ── Translation result ────────────────────────────────────────────────────────
st.subheader("Translation")

if "translated" not in st.session_state:
    st.session_state.translated = ""
if "tgt_lang" not in st.session_state:
    st.session_state.tgt_lang = "es"

if st.session_state.translated:
    st.success(st.session_state.translated)

    # ── Play audio button ─────────────────────────────────────────────────────
    if st.button("🔊 Play Audio"):
        play_audio(st.session_state.translated, st.session_state.tgt_lang)

st.divider()

# ── Preset medical phrases ────────────────────────────────────────────────────
st.subheader("⚕️ Common Medical Phrases")
st.caption("Click a phrase to automatically translate it and hear the audio.")

for phrase in MEDICAL_PHRASES:
    if st.button(phrase, use_container_width=True):
        # Always translate from English when using presets
        direction   = "en->es" if st.session_state.direction == "en->es" else "es->en"
        src_phrase  = phrase if direction == "en->es" else translate_text(phrase, "en->es")
        translated  = translate_text(src_phrase, direction)

        st.session_state.input_text = src_phrase
        st.session_state.translated = translated
        st.session_state.tgt_lang   = tgt_lang_code

        st.markdown(f"**Original:** {src_phrase}")
        st.success(f"**Translation:** {translated}")
        play_audio(translated, tgt_lang_code)
