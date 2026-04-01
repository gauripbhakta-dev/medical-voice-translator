"""
Medical Voice Translator - Fixed version
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
        return GoogleTranslator(source=src, target=tgt).translate(text)
    except Exception as e:
        return f"Translation error: {e}"


def generate_audio_b64(text: str, lang: str):
    try:
        tts = gTTS(text=text, lang=lang)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        data = buf.read()
        if len(data) < 100:
            return None
        return base64.b64encode(data).decode()
    except Exception as e:
        st.warning(f"Audio generation failed: {e}")
        return None


def process_audio_input(audio, mic_lang_code):
    if not VOICE_INPUT_AVAILABLE:
        return None
    recognizer = sr.Recognizer()
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio.getvalue())
            tmp_path = tmp.name
        with sr.AudioFile(tmp_path) as source:
            audio_data = recognizer.record(source)
        os.unlink(tmp_path)
        return recognizer.recognize_google(audio_data, language=mic_lang_code)
    except sr.UnknownValueError:
        st.error("Could not understand audio, please try again.")
        return None
    except sr.RequestError as e:
        st.error(f"Speech recognition unavailable: {e}")
        return None
    except Exception as e:
        st.error(f"Audio error: {e}")
        return None


def do_translate(text):
    direction  = st.session_state.direction
    tgt_lang   = "es" if direction == "en->es" else "en"
    translated = translate_text(text, direction)
    audio_b64  = generate_audio_b64(translated, tgt_lang)
    st.session_state.translated = translated
    st.session_state.tgt_lang   = tgt_lang
    st.session_state.audio_b64  = audio_b64


def render_audio(b64: str):
    # Use audio/mpeg for iOS compatibility, mp3 as fallback for others
    st.markdown(f"""
    <div style="margin-top:8px;">
        <p style="font-size:13px; color:#666; margin-bottom:6px;">🔊 Translation Audio</p>
        <audio controls preload="auto"
               style="width:100%; min-height:40px; border-radius:8px; display:block;">
            <source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        <p style="font-size:11px; color:#aaa; margin-top:4px;">
            iPhone: tap the play button above to hear audio.
        </p>
    </div>
    """, unsafe_allow_html=True)


MEDICAL_PHRASES_EN = [
    "Where is your pain?",
    "Do you have allergies?",
    "Rate your pain from 1 to 10",
    "Are you taking any medication?",
]

MEDICAL_PHRASES_ES = [
    "¿Dónde le duele?",
    "¿Tiene alergias?",
    "Califique su dolor del 1 al 10",
    "¿Está tomando algún medicamento?",
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
    h1 { display: none !important; }
    h2, h3 { font-size: 1.2rem !important; }
    audio { width: 100% !important; border-radius: 8px; display: block; }
</style>
""", unsafe_allow_html=True)

for key, default in {
    "direction": "en->es",
    "translated": "",
    "tgt_lang": "es",
    "last_audio_id": None,
    "audio_b64": None,
    "input_text": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Custom title — single line on all screen sizes
st.markdown("""
<div style="padding: 0.5rem 0 1rem 0;">
    <div style="font-size: clamp(1.1rem, 5.5vw, 1.75rem); font-weight: 700; white-space: nowrap; letter-spacing: -0.3px; line-height: 1.2; color: inherit;">
        🩺 Medical Voice Translator
    </div>
    <div style="font-size: 13px; color: #888; margin-top: 4px;">
        Translate medical phrases between English and Spanish — with audio playback.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Direction selector ───────────────────────────────────────────────────────
st.subheader("Translation Direction")
col1, col2 = st.columns(2)
with col1:
    en_to_es = st.button("🇺🇸 EN → ES", use_container_width=True)
with col2:
    es_to_en = st.button("🇪🇸 ES → EN", use_container_width=True)

if en_to_es:
    st.session_state.update({"direction":"en->es","translated":"","audio_b64":None,"input_text":""})
if es_to_en:
    st.session_state.update({"direction":"es->en","translated":"","audio_b64":None,"input_text":""})

direction      = st.session_state.direction
src_lang_label = "English" if direction == "en->es" else "Spanish"
mic_lang_code  = "en-US"   if direction == "en->es" else "es-ES"

st.info(f"**Mode:** {'English → Spanish' if direction == 'en->es' else 'Spanish → English'}")

# ── Voice input ───────────────────────────────────────────────────────────────
if VOICE_INPUT_AVAILABLE:
    st.markdown("**🎙️ Voice Input**")
    st.markdown("""
    <div style="font-size:13px; color:#666; margin-bottom:8px;">
        📱 <b>iPhone/Android:</b> Tap the microphone, speak, tap stop — translation happens automatically.
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
                with st.spinner("Translating..."):
                    do_translate(spoken)
                st.success(f"✅ Heard: *{spoken}*")

# ── Text input ───────────────────────────────────────────────────────────────
st.subheader("Enter Text")
typed_text = st.text_area(
    f"Type in {src_lang_label}:",
    value=st.session_state.input_text,
    height=120,
    placeholder=f"Enter {src_lang_label} text here…",
    key="text_area_widget",
)
st.session_state.input_text = typed_text

# ── Translate button ─────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
if st.button("🔄 Translate", type="primary", use_container_width=True):
    if st.session_state.input_text.strip():
        with st.spinner("Translating..."):
            do_translate(st.session_state.input_text.strip())
    else:
        st.warning("Please type or record some text before translating.")

# ── Translation result + audio ────────────────────────────────────────────────
st.subheader("Translation")
if st.session_state.translated:
    st.success(st.session_state.translated)
if st.session_state.audio_b64:
    render_audio(st.session_state.audio_b64)

st.divider()

# ── Preset medical phrases ────────────────────────────────────────────────────
st.subheader("⚕️ Common Medical Phrases")

if direction == "en->es":
    phrases = MEDICAL_PHRASES_EN
    st.caption("Tap a phrase to translate it to Spanish and hear the audio.")
else:
    phrases = MEDICAL_PHRASES_ES
    st.caption("Toca una frase para traducirla al inglés y escuchar el audio.")

for phrase in phrases:
    if st.button(phrase, use_container_width=True):
        with st.spinner("Translating..."):
            do_translate(phrase)
        st.session_state.input_text = phrase
        st.markdown(f"**Original:** {phrase}")
        st.success(f"**Translation:** {st.session_state.translated}")
        if st.session_state.audio_b64:
            render_audio(st.session_state.audio_b64)
