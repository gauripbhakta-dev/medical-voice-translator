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

try:
    import speech_recognition as sr
    VOICE_INPUT_AVAILABLE = True
except ImportError:
    VOICE_INPUT_AVAILABLE = False


def translate_text(text: str, direction: str) -> str:
    if not text.strip():
        return ""
    src, tgt = direction.split("->")
    try:
        result = GoogleTranslator(source=src, target=tgt).translate(text)
        return result
    except Exception as e:
        return f"Translation error: {e}"


def generate_audio_b64(text: str, lang: str) -> str:
    tts = gTTS(text=text, lang=lang)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


def render_audio_player(text: str, lang: str):
    """Render audio player inline — no button needed."""
    if not text.strip():
        return
    b64 = generate_audio_b64(text, lang)
    audio_html = f"""
    <audio controls style="width:100%; margin-top:8px; border-radius:8px;">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)


def process_audio_input(audio, mic_lang_code):
    if not VOICE_INPUT_AVAILABLE:
        st.error("Speech recognition not available.")
        return None
    recognizer = sr.Recognizer()
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio.getvalue())
            tmp_path = tmp.name
        with sr.AudioFile(tmp_path) as source:
            audio_data = recognizer.record(source)
        os.unlink(tmp_path)
        spoken = recognizer.recognize_google(audio_data, language=mic_lang_code)
        return spoken
    except sr.UnknownValueError:
        st.error("Could not understand audio, please try again.")
        return None
    except sr.RequestError as e:
        st.error(f"Speech recognition service unavailable: {e}")
        return None
    except Exception as e:
        st.error(f"Audio processing error: {e}")
        return None


MEDICAL_PHRASES = [
    "Where is your pain?",
    "Do you have allergies?",
    "Rate your pain from 1 to 10",
    "Are you taking any medication?",
]

st.set_page_config(
    page_title="Medical Voice Translator",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<style>
    html, body, [class*="css"] { font-size: 16px !important; -webkit-text-size-adjust: 100%; }
    .block-container { padding-left: 1rem !important; padding-right: 1rem !important; padding-top: 1rem !important; max-width: 100% !important; }
    .stButton > button { min-height: 52px !important; font-size: 16px !important; border-radius: 10px !important; width: 100% !important; touch-action: manipulation; }
    .stTextArea textarea { font-size: 16px !important; min-height: 100px !important; border-radius: 10px !important; }
    @media (max-width: 640px) {
        [data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; min-width: 0 !important; }
        .stButton > button { min-height: 56px !important; font-size: 17px !important; }
    }
    [data-testid="stAudioInput"] { width: 100% !important; }
    .stAlert { border-radius: 10px !important; font-size: 16px !important; }
    h1 { font-size: 1.6rem !important; line-height: 1.3 !important; }
    h2, h3 { font-size: 1.2rem !important; }
    audio { width: 100% !important; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ───────────────────────────────────────────────────
if "direction" not in st.session_state:
    st.session_state.direction = "en->es"
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "translated" not in st.session_state:
    st.session_state.translated = ""
if "tgt_lang" not in st.session_state:
    st.session_state.tgt_lang = "es"
if "last_audio_id" not in st.session_state:
    st.session_state.last_audio_id = None
if "audio_b64" not in st.session_state:
    st.session_state.audio_b64 = None

st.title("🩺 Medical Voice Translator")
st.caption("Translate medical phrases between English and Spanish — with audio playback.")

# ── Direction selector ───────────────────────────────────────────────────────
st.subheader("Translation Direction")
col1, col2 = st.columns(2)
with col1:
    en_to_es = st.button("🇺🇸 EN → ES", use_container_width=True)
with col2:
    es_to_en = st.button("🇪🇸 ES → EN", use_container_width=True)

if en_to_es:
    st.session_state.direction = "en->es"
    st.session_state.translated = ""
    st.session_state.audio_b64 = None
if es_to_en:
    st.session_state.direction = "es->en"
    st.session_state.translated = ""
    st.session_state.audio_b64 = None

src_lang_label = "English" if st.session_state.direction == "en->es" else "Spanish"
tgt_lang_label = "Spanish" if st.session_state.direction == "en->es" else "English"
tgt_lang_code  = "es"      if st.session_state.direction == "en->es" else "en"
mic_lang_code  = "en-US"   if st.session_state.direction == "en->es" else "es-ES"

st.info(f"**Mode:** {src_lang_label} → {tgt_lang_label}")

# ── Text input ───────────────────────────────────────────────────────────────
st.subheader("Enter Text")

user_input = st.text_area(
    f"Type in {src_lang_label}:",
    value=st.session_state.input_text,
    height=120,
    placeholder=f"Enter {src_lang_label} text here…",
    key="text_input_area"
)

# ── Voice input ───────────────────────────────────────────────────────────────
if VOICE_INPUT_AVAILABLE:
    st.markdown("**🎙️ Voice Input**")
    st.markdown("""
    <div style="font-size:13px; color:#666; margin-bottom:8px;">
        📱 <b>iPhone/Android:</b> Tap the microphone, speak your phrase, tap stop.
        The transcribed text will appear below. Then tap Translate.
    </div>
    """, unsafe_allow_html=True)

    audio = st.audio_input("Tap to record", key="audio_recorder")

    if audio is not None:
        audio_id = hash(audio.getvalue())
        if audio_id != st.session_state.last_audio_id:
            st.session_state.last_audio_id = audio_id
            with st.spinner("Transcribing..."):
                spoken = process_audio_input(audio, mic_lang_code)
            if spoken:
                st.session_state.input_text = spoken
                user_input = spoken
                st.success(f"✅ Heard: *{spoken}*")

# ── Translate button ─────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
if st.button("🔄 Translate", type="primary", use_container_width=True):
    text_to_translate = user_input or st.session_state.input_text
    if text_to_translate.strip():
        with st.spinner("Translating..."):
            translated = translate_text(text_to_translate, st.session_state.direction)
            # Pre-generate audio immediately so no extra button needed
            audio_b64 = generate_audio_b64(translated, tgt_lang_code)
        st.session_state.translated = translated
        st.session_state.tgt_lang = tgt_lang_code
        st.session_state.audio_b64 = audio_b64
    else:
        st.warning("Please enter or record some text before translating.")

# ── Translation result + auto audio player ────────────────────────────────────
st.subheader("Translation")

if st.session_state.translated:
    st.success(st.session_state.translated)

    # Auto-render audio player — no button click needed
    if st.session_state.audio_b64:
        b64 = st.session_state.audio_b64
        audio_html = f"""
        <div style="margin-top:8px;">
            <p style="font-size:13px; color:#666; margin-bottom:4px;">🔊 Translation Audio</p>
            <audio controls style="width:100%; border-radius:8px;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        </div>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

st.divider()

# ── Preset medical phrases ────────────────────────────────────────────────────
st.subheader("⚕️ Common Medical Phrases")
st.caption("Tap a phrase to translate it and hear the audio.")

for phrase in MEDICAL_PHRASES:
    if st.button(phrase, use_container_width=True):
        direction  = st.session_state.direction
        src_phrase = phrase if direction == "en->es" else translate_text(phrase, "en->es")
        with st.spinner("Translating..."):
            translated = translate_text(src_phrase, direction)
            audio_b64  = generate_audio_b64(translated, tgt_lang_code)
        st.session_state.input_text = src_phrase
        st.session_state.translated = translated
        st.session_state.tgt_lang = tgt_lang_code
        st.session_state.audio_b64 = audio_b64
        st.markdown(f"**Original:** {src_phrase}")
        st.success(f"**Translation:** {translated}")
        b64 = audio_b64
        st.markdown(f"""
        <audio controls style="width:100%; border-radius:8px; margin-top:8px;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)
