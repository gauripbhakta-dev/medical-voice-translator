"""
Medical Voice Translator
Translates medical phrases between English and Spanish,
generates audio with gTTS, and optionally accepts voice input.
Mobile-optimized for iOS and Android.
"""

import io
import base64
import tempfile
import os
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
    tts = gTTS(text=text, lang=lang)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


def play_audio(text: str, lang: str):
    if not text.strip():
        st.warning("No text to play.")
        return
    b64 = generate_audio_b64(text, lang)
    # autoplay is blocked on iOS Safari — use controls only
    audio_html = f"""
    <audio controls style="width:100%; margin-top:8px;">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    <script>
        // Try autoplay after user gesture (works on Android, may be blocked on iOS)
        var audios = document.querySelectorAll('audio');
        var latest = audios[audios.length - 1];
        latest.play().catch(function() {{}});
    </script>
    """
    st.markdown(audio_html, unsafe_allow_html=True)


# ─── Process audio from st.audio_input ──────────────────────────────────────

def process_audio_input(audio, mic_lang_code):
    if not VOICE_INPUT_AVAILABLE:
        st.error("Speech recognition not available.")
        return
    recognizer = sr.Recognizer()
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio.getvalue())
            tmp_path = tmp.name
        with sr.AudioFile(tmp_path) as source:
            audio_data = recognizer.record(source)
        os.unlink(tmp_path)
        spoken = recognizer.recognize_google(audio_data, language=mic_lang_code)
        st.session_state.input_text = spoken
        st.rerun()
    except sr.UnknownValueError:
        st.error("Could not understand audio, please try again.")
    except sr.RequestError as e:
        st.error(f"Speech recognition service unavailable: {e}")
    except Exception as e:
        st.error(f"Audio processing error: {e}")


# ─── Preset medical phrases ──────────────────────────────────────────────────

MEDICAL_PHRASES = [
    "Where is your pain?",
    "Do you have allergies?",
    "Rate your pain from 1 to 10",
    "Are you taking any medication?",
]


# ─── App layout ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Medical Voice Translator",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Mobile-responsive CSS ────────────────────────────────────────────────────
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<style>
    /* Global mobile fixes */
    html, body, [class*="css"] {
        font-size: 16px !important;
        -webkit-text-size-adjust: 100%;
    }

    /* Main container padding on mobile */
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
        max-width: 100% !important;
    }

    /* Bigger touch targets for buttons */
    .stButton > button {
        min-height: 52px !important;
        font-size: 16px !important;
        border-radius: 10px !important;
        width: 100% !important;
        touch-action: manipulation;
    }

    /* Text area bigger on mobile */
    .stTextArea textarea {
        font-size: 16px !important;
        min-height: 100px !important;
        border-radius: 10px !important;
    }

    /* Make columns stack better on small screens */
    @media (max-width: 640px) {
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 0 !important;
        }
        .stButton > button {
            min-height: 56px !important;
            font-size: 17px !important;
        }
    }

    /* Audio input widget */
    [data-testid="stAudioInput"] {
        width: 100% !important;
    }

    /* Success/info/warning boxes */
    .stAlert {
        border-radius: 10px !important;
        font-size: 16px !important;
    }

    /* Title sizing on mobile */
    h1 {
        font-size: 1.6rem !important;
        line-height: 1.3 !important;
    }
    h2, h3 {
        font-size: 1.2rem !important;
    }

    /* Audio player full width */
    audio {
        width: 100% !important;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🩺 Medical Voice Translator")
st.caption("Translate medical phrases between English and Spanish — with audio playback.")

# ── Direction selector ──────────────────────────────────────────────────────
st.subheader("Translation Direction")
col1, col2 = st.columns(2)
with col1:
    en_to_es = st.button("🇺🇸 EN → ES", use_container_width=True)
with col2:
    es_to_en = st.button("🇪🇸 ES → EN", use_container_width=True)

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

# ── Voice input ───────────────────────────────────────────────────────────────
if VOICE_INPUT_AVAILABLE:
    st.markdown("**🎙️ Voice Input**")

    # iOS/Safari detection note
    st.markdown("""
    <div style="font-size:13px; color:#666; margin-bottom:8px;">
        📱 <b>iPhone/iPad users:</b> Tap the microphone below, allow microphone access, 
        record your phrase, then tap stop. If recording doesn't work, use the text box above.
    </div>
    """, unsafe_allow_html=True)

    audio = st.audio_input("Tap to record")
    if audio:
        with st.spinner("Processing audio..."):
            process_audio_input(audio, mic_lang_code)

# ── Translate button ─────────────────────────────────────────────────────────
st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
if st.button("🔄 Translate", type="primary", use_container_width=True):
    if user_input.strip():
        with st.spinner("Translating..."):
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

    if st.button("🔊 Play Audio", use_container_width=True):
        with st.spinner("Generating audio..."):
            play_audio(st.session_state.translated, st.session_state.tgt_lang)

st.divider()

# ── Preset medical phrases ────────────────────────────────────────────────────
st.subheader("⚕️ Common Medical Phrases")
st.caption("Tap a phrase to translate it and hear the audio.")

for phrase in MEDICAL_PHRASES:
    if st.button(phrase, use_container_width=True):
        direction  = "en->es" if st.session_state.direction == "en->es" else "es->en"
        src_phrase = phrase if direction == "en->es" else translate_text(phrase, "en->es")
        with st.spinner("Translating..."):
            translated = translate_text(src_phrase, direction)

        st.session_state.input_text = src_phrase
        st.session_state.translated = translated
        st.session_state.tgt_lang   = tgt_lang_code

        st.markdown(f"**Original:** {src_phrase}")
        st.success(f"**Translation:** {translated}")
        play_audio(translated, tgt_lang_code)
