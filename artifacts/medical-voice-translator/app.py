"""
Medical Voice Translator - Stable working version
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
    components.html(f"""
    <audio controls preload="auto"
           style="width:100%; border-radius:8px; display:block; min-height:40px; margin-top:8px;">
        <source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    <p style="font-size:11px; color:#aaa; margin:4px 0 0 0; font-family:sans-serif;">
        iPhone: tap the play button to hear the translation.
    </p>
    """, height=70)


CATEGORY_LABELS = {
    "🩹 Pain Assessment":         {"es": "🩹 Evaluación del dolor"},
    "🤒 Symptoms":                {"es": "🤒 Síntomas"},
    "💊 Medications & Allergies": {"es": "💊 Medicamentos y alergias"},
    "📋 Medical History":         {"es": "📋 Historia médica"},
    "✅ Consent & Instructions":  {"es": "✅ Consentimiento e instrucciones"},
    "🚨 Emergency":               {"es": "🚨 Emergencia"},
}

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

UI = {
    "en->es": {
        "btn1":             "🇺🇸 EN → ES",
        "btn2":             "🇪🇸 ES → EN",
        "voice_hint":       "📱 Tap the microphone, speak, tap stop — translation happens automatically.",
        "voice_btn":        "Tap to record",
        "text_label":       "Type in English:",
        "text_placeholder": "Enter English text here…",
        "translate_btn":    "🔄 Translate",
        "translate_warn":   "Please type or record some text before translating.",
        "input_section":    "Input",
        "translation":      "Translation",
        "phrases_title":    "⚕️ Quick Phrases",
        "phrases_caption":  "Tap a phrase to translate it to Spanish and hear the audio.",
        "heard":            "✅ Heard:",
        "spinner_trans":    "Transcribing...",
        "spinner_tl":       "Translating...",
        "disclaimer":       "No data stored · For communication assistance only · Not a substitute for a certified medical interpreter",
        "tl_label":         "Translation",
        "placeholder_tl":   "Translation will appear here.",
    },
    "es->en": {
        "btn1":             "🇺🇸 EN → ES",
        "btn2":             "🇪🇸 ES → EN",
        "voice_hint":       "📱 Toque el micrófono, hable, toque detener — la traducción ocurre automáticamente.",
        "voice_btn":        "Toque para grabar",
        "text_label":       "Escriba en Español:",
        "text_placeholder": "Ingrese texto en español aquí…",
        "translate_btn":    "🔄 Traducir",
        "translate_warn":   "Por favor escriba o grabe texto antes de traducir.",
        "input_section":    "Entrada",
        "translation":      "Traducción",
        "phrases_title":    "⚕️ Frases rápidas",
        "phrases_caption":  "Toca una frase para traducirla al inglés y escuchar el audio.",
        "heard":            "✅ Escuché:",
        "spinner_trans":    "Transcribiendo...",
        "spinner_tl":       "Traduciendo...",
        "disclaimer":       "Sin datos almacenados · Solo asistencia en comunicación · No sustituye a un intérprete médico certificado",
        "tl_label":         "Traducción",
        "placeholder_tl":   "La traducción aparecerá aquí.",
    }
}

st.set_page_config(
    page_title="Medical Voice Translator",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Google Analytics — inject into parent page via postMessage workaround
components.html("""
<script>
(function() {
    // Send gtag script to parent window to bypass iframe sandbox
    var script1 = document.createElement('script');
    script1.async = true;
    script1.src = 'https://www.googletagmanager.com/gtag/js?id=G-PM770KN3NX';
    
    var script2 = document.createElement('script');
    script2.innerHTML = `
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-PM770KN3NX', {
            'page_title': 'Medical Voice Translator',
            'page_location': window.location.href
        });
    `;
    
    // Try appending to parent document
    try {
        window.parent.document.head.appendChild(script1);
        window.parent.document.head.appendChild(script2);
    } catch(e) {
        // Fallback: append to current iframe
        document.head.appendChild(script1);
        document.head.appendChild(script2);
    }
})();
</script>
""", height=0)

st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<style>
    html, body, [class*="css"] { font-size: 16px !important; -webkit-text-size-adjust: 100%; }
    .block-container { padding-left: 1rem !important; padding-right: 1rem !important; padding-top: 2rem !important; max-width: 480px !important; }
    .stButton > button { min-height: 52px !important; font-size: 16px !important; border-radius: 10px !important; width: 100% !important; touch-action: manipulation; }
    .stTextArea textarea { font-size: 16px !important; border-radius: 10px !important; }
    [data-testid="stAudioInput"] { width: 100% !important; }
    .stAlert { border-radius: 10px !important; font-size: 15px !important; }
    h1 { font-size: clamp(1rem, 4.8vw, 1.5rem) !important; white-space: nowrap !important; overflow: hidden !important; text-overflow: ellipsis !important; margin-bottom: 0 !important; }
    h2, h3 { font-size: 0.85rem !important; text-transform: uppercase !important; letter-spacing: 0.6px !important; color: #999 !important; margin-bottom: 8px !important; }
    .stButton > button {
        background-color: #1F4E79 !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    .stButton > button:hover {
        background-color: #2E75B6 !important;
        color: #FFFFFF !important;
    }
    audio { width: 100% !important; border-radius: 8px; display: block; }
</style>
""", unsafe_allow_html=True)

for key, default in {
    "direction":     "en->es",
    "translated":    "",
    "tgt_lang":      "es",
    "last_audio_id": None,
    "audio_b64":     None,
    "input_text":    "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

direction     = st.session_state.direction
ui            = UI[direction]
mic_lang_code = "en-US" if direction == "en->es" else "es-ES"
lang_key      = "en" if direction == "en->es" else "es"

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🩺 Medical Voice Translator")
st.markdown(f"""
<p style="font-size:11px; color:#aaa; margin-top:2px; margin-bottom:16px; line-height:1.5;">
    {ui['disclaimer']}
</p>
""", unsafe_allow_html=True)

# ── Direction toggle ───────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    if st.button(ui["btn1"], use_container_width=True,
                 type="primary" if direction == "en->es" else "secondary"):
        st.session_state.update({"direction":"en->es","translated":"","audio_b64":None,"input_text":""})
        st.rerun()
with col2:
    if st.button(ui["btn2"], use_container_width=True,
                 type="primary" if direction == "es->en" else "secondary"):
        st.session_state.update({"direction":"es->en","translated":"","audio_b64":None,"input_text":""})
        st.rerun()

st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)

# ── INPUT ZONE ────────────────────────────────────────────────────────────────
st.subheader(ui["input_section"])

# Input zone
typed_text = st.text_area(
    ui["text_label"],
    value=st.session_state.input_text,
    height=100,
    placeholder=ui["text_placeholder"],
    key="text_area_widget",
    label_visibility="collapsed",
)
st.session_state.input_text = typed_text
translate_clicked = st.button(ui["translate_btn"], type="primary", use_container_width=True)

# Voice recorder
if VOICE_INPUT_AVAILABLE:
    st.markdown(f"""
    <p style="font-size:12px; color:#999; margin: 6px 0 4px 0;">{ui['voice_hint']}</p>
    """, unsafe_allow_html=True)
    audio = st.audio_input(ui["voice_btn"], key="audio_recorder")
else:
    audio = None

# Handle voice recording
if audio is not None:
    audio_id = hash(audio.getvalue())
    if audio_id != st.session_state.last_audio_id:
        st.session_state.last_audio_id = audio_id
        with st.spinner(ui["spinner_trans"]):
            spoken = process_audio_input(audio, mic_lang_code)
        if spoken:
            st.session_state.input_text = spoken
            with st.spinner(ui["spinner_tl"]):
                do_translate(spoken)
            st.success(f"{ui['heard']} *{spoken}*")

# Handle translate button
if translate_clicked:
    if st.session_state.input_text.strip():
        with st.spinner(ui["spinner_tl"]):
            do_translate(st.session_state.input_text.strip())
    else:
        st.warning(ui["translate_warn"])

st.markdown("<div style='margin-bottom:4px;'></div>", unsafe_allow_html=True)

# ── TRANSLATION + AUDIO ZONE ──────────────────────────────────────────────────
st.subheader(ui["tl_label"])
if st.session_state.translated:
    st.success(st.session_state.translated)
    if st.session_state.audio_b64:
        render_audio(st.session_state.audio_b64)
else:
    st.markdown(f"""
    <p style="font-size:14px; color:#bbb; padding: 4px 0 12px 0;">
        {ui['placeholder_tl']}
    </p>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom:4px;'></div>", unsafe_allow_html=True)

# ── QUICK PHRASES ZONE ────────────────────────────────────────────────────────
st.subheader(ui["phrases_title"])
st.caption(ui["phrases_caption"])

for category, langs in MEDICAL_PHRASES.items():
    label = CATEGORY_LABELS[category]["es"] if direction == "es->en" else category
    with st.expander(label, expanded=False):
        for phrase in langs[lang_key]:
            if st.button(phrase, use_container_width=True, key=f"phrase_{phrase}"):
                with st.spinner(ui["spinner_tl"]):
                    do_translate(phrase)
                st.session_state.input_text = phrase
                st.success(f"**{ui['tl_label']}:** {st.session_state.translated}")
                if st.session_state.audio_b64:
                    render_audio(st.session_state.audio_b64)

# ── About ─────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center; padding: 8px 0 4px 0;">
    <p style="font-size:12px; color:#aaa; margin:0;">
        Built by <b style="color:#888;">Gauri Bhakta</b>, Phillips Academy · Inspired by real patients
    </p>
</div>
""", unsafe_allow_html=True)
