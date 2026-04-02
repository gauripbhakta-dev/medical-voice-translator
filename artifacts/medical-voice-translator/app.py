"""
Medical Voice Translator - Fixed version
"""

import io
import base64
import tempfile
import os
import streamlit as st
import streamlit.components.v1 as components
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
    # Use components.html() — always renders a fresh iframe, never cached by Streamlit
    components.html(f"""
    <div style="font-family: sans-serif; padding: 4px 0;">
        <p style="font-size:13px; color:#666; margin: 0 0 6px 0;">🔊 Translation Audio</p>
        <audio controls preload="auto"
               style="width:100%; border-radius:8px; display:block; min-height:40px;">
            <source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        <p style="font-size:11px; color:#aaa; margin: 4px 0 0 0;">
            iPhone: tap the play button above to hear audio.
        </p>
    </div>
    """, height=90)


MEDICAL_PHRASES = {
    "🩹 Pain Assessment": {
        "en": [
            "Where is your pain?",
            "Rate your pain from 1 to 10",
            "Is the pain sharp or dull?",
            "Is the pain constant or does it come and go?",
            "When did the pain start?",
            "Does anything make the pain better or worse?",
        ],
        "es": [
            "¿Dónde le duele?",
            "Califique su dolor del 1 al 10",
            "¿El dolor es agudo o sordo?",
            "¿El dolor es constante o va y viene?",
            "¿Cuándo empezó el dolor?",
            "¿Hay algo que mejore o empeore el dolor?",
        ]
    },
    "🤒 Symptoms": {
        "en": [
            "Do you have a fever?",
            "Are you having trouble breathing?",
            "Do you feel dizzy or lightheaded?",
            "Do you have nausea or vomiting?",
            "Do you have chest pain?",
            "Have you fainted or lost consciousness?",
        ],
        "es": [
            "¿Tiene fiebre?",
            "¿Tiene dificultad para respirar?",
            "¿Se siente mareado o con la cabeza liviana?",
            "¿Tiene náuseas o vómitos?",
            "¿Tiene dolor en el pecho?",
            "¿Se ha desmayado o perdido el conocimiento?",
        ]
    },
    "💊 Medications & Allergies": {
        "en": [
            "Do you have any allergies?",
            "Are you allergic to any medications?",
            "Are you currently taking any medications?",
            "Do you take blood thinners?",
            "Are you allergic to penicillin?",
            "Do you have a list of your medications?",
        ],
        "es": [
            "¿Tiene alguna alergia?",
            "¿Es alérgico a algún medicamento?",
            "¿Está tomando algún medicamento actualmente?",
            "¿Toma anticoagulantes?",
            "¿Es alérgico a la penicilina?",
            "¿Tiene una lista de sus medicamentos?",
        ]
    },
    "📋 Medical History": {
        "en": [
            "Do you have diabetes?",
            "Do you have high blood pressure?",
            "Have you had surgery before?",
            "Do you have any heart conditions?",
            "Are you pregnant?",
            "Do you smoke or drink alcohol?",
        ],
        "es": [
            "¿Tiene diabetes?",
            "¿Tiene presión arterial alta?",
            "¿Ha tenido cirugías antes?",
            "¿Tiene alguna condición del corazón?",
            "¿Está embarazada?",
            "¿Fuma o consume alcohol?",
        ]
    },
    "✅ Consent & Instructions": {
        "en": [
            "I need to examine you.",
            "Please sign this form.",
            "Do you understand?",
            "Do you have any questions?",
            "We need to take a blood sample.",
            "Please take this medication twice a day.",
        ],
        "es": [
            "Necesito examinarlo/a.",
            "Por favor firme este formulario.",
            "¿Entiende?",
            "¿Tiene alguna pregunta?",
            "Necesitamos tomar una muestra de sangre.",
            "Por favor tome este medicamento dos veces al día.",
        ]
    },
    "🚨 Emergency": {
        "en": [
            "Call 911 immediately.",
            "Stay calm, help is coming.",
            "Do not move.",
            "Are you having a heart attack?",
            "I am going to help you.",
            "Is there someone I can call for you?",
        ],
        "es": [
            "Llame al 911 inmediatamente.",
            "Cálmese, la ayuda está en camino.",
            "No se mueva.",
            "¿Está teniendo un ataque al corazón?",
            "Le voy a ayudar.",
            "¿Hay alguien a quien pueda llamar por usted?",
        ]
    },
}

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
    .block-container { padding-left: 1rem !important; padding-right: 1rem !important; padding-top: 2.5rem !important; max-width: 100% !important; }
    .stButton > button { min-height: 52px !important; font-size: 16px !important; border-radius: 10px !important; width: 100% !important; touch-action: manipulation; }
    .stTextArea textarea { font-size: 16px !important; min-height: 100px !important; border-radius: 10px !important; }
    @media (max-width: 640px) {
        [data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; min-width: 0 !important; }
        .stButton > button { min-height: 56px !important; font-size: 17px !important; }
    }
    [data-testid="stAudioInput"] { width: 100% !important; }
    .stAlert { border-radius: 10px !important; font-size: 16px !important; }
    h1 { font-size: clamp(1rem, 4.8vw, 1.6rem) !important; white-space: nowrap !important; overflow: hidden !important; text-overflow: ellipsis !important; }
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
st.title("🩺 Medical Voice Translator")
st.caption("Translate medical phrases between English and Spanish — with audio playback.")

# ── Disclaimer ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#fff8e1; border-left: 4px solid #f9a825; border-radius:8px; padding:10px 14px; margin-bottom:12px; font-size:13px; color:#555;">
    ⚠️ <b>Important:</b> No data is stored or recorded. For communication assistance only.
    Not a substitute for a certified medical interpreter.
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

lang_key = "en" if direction == "en->es" else "es"
caption = "Tap a phrase to translate it to Spanish and hear the audio." if direction == "en->es" else "Toca una frase para traducirla al inglés y escuchar el audio."
st.caption(caption)

for category, langs in MEDICAL_PHRASES.items():
    with st.expander(category, expanded=False):
        for phrase in langs[lang_key]:
            if st.button(phrase, use_container_width=True, key=f"phrase_{phrase}"):
                with st.spinner("Translating..."):
                    do_translate(phrase)
                st.session_state.input_text = phrase
                st.markdown(f"**Original:** {phrase}")
                st.success(f"**Translation:** {st.session_state.translated}")
                if st.session_state.audio_b64:
                    render_audio(st.session_state.audio_b64)
