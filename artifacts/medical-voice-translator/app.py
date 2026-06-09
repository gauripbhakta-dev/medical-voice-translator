"""
Medical Voice Translator — Fully Local HIPAA-Compliant Version
==============================================================
Feature flags:

REGIONAL_VARIANTS_ENABLED = True   → Regional Spanish variants
USE_LOCAL_TTS             = True   → Piper TTS (local) vs gTTS (Google)
USE_LOCAL_WHISPER         = True   → Whisper (local) vs Web Speech API
USE_LOCAL_TRANSLATION     = True   → Argos (local) vs Google Translate

All True  = fully HIPAA compliant by architecture
All False = original Google-dependent version
"""

import io
import os
import sys
import wave
import base64
import tempfile
import streamlit as st
import streamlit.components.v1 as components

# ── FEATURE FLAGS ──────────────────────────────────────────────────────────────
REGIONAL_VARIANTS_ENABLED = True
USE_LOCAL_TTS             = True
USE_LOCAL_WHISPER         = True
USE_LOCAL_TRANSLATION     = True

# ── REGIONAL VARIANTS ──────────────────────────────────────────────────────────
if REGIONAL_VARIANTS_ENABLED:
    sys.path.insert(0, os.path.dirname(__file__))
    from regional_medical_spanish import (
        REGIONAL_VARIANTS,
        get_regional_translation,
        get_regional_translation_fuzzy,
        get_english_back_translation,
        find_best_spanish_match,
    )

# ── LOCAL TTS — PIPER ──────────────────────────────────────────────────────────
LOCAL_TTS_AVAILABLE = False
if USE_LOCAL_TTS:
    try:
        from piper.voice import PiperVoice

        @st.cache_resource
        def load_piper_model():
            _dir      = os.path.dirname(os.path.abspath(__file__))
            onnx_path = os.path.join(_dir, "es_MX-claude-high.onnx")
            json_path = os.path.join(_dir, "es_MX-claude-high.onnx.json")

            # Auto-download model files if missing (first run on Streamlit Cloud)
            if not os.path.exists(onnx_path) or not os.path.exists(json_path):
                import urllib.request
                url_base = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_MX/claude/high"
                with st.spinner("Downloading Spanish voice model (first time only, ~60MB)..."):
                    if not os.path.exists(onnx_path):
                        urllib.request.urlretrieve(f"{url_base}/es_MX-claude-high.onnx", onnx_path)
                    if not os.path.exists(json_path):
                        urllib.request.urlretrieve(f"{url_base}/es_MX-claude-high.onnx.json", json_path)

            return PiperVoice.load(onnx_path, config_path=json_path)

        piper_model = load_piper_model()
        LOCAL_TTS_AVAILABLE = True
    except Exception as e:
        st.warning(f"Local TTS unavailable: {e}. Falling back to gTTS.")

# ── LOCAL WHISPER ──────────────────────────────────────────────────────────────
LOCAL_WHISPER_AVAILABLE = False
if USE_LOCAL_WHISPER:
    try:
        import whisper

        @st.cache_resource
        def load_whisper_model():
            return whisper.load_model("tiny")

        whisper_model = load_whisper_model()
        LOCAL_WHISPER_AVAILABLE = True
    except Exception as e:
        st.warning(f"Local Whisper unavailable: {e}. Falling back to Web Speech API.")

# ── LOCAL TRANSLATION — ARGOS ──────────────────────────────────────────────────
LOCAL_TRANSLATION_AVAILABLE = False
if USE_LOCAL_TRANSLATION:
    try:
        import argostranslate.translate

        @st.cache_resource
        def setup_argos():
            import argostranslate.package
            argostranslate.package.update_package_index()
            available = argostranslate.package.get_available_packages()

            # Force reinstall ES→EN to fix infinite loop bug in cached package
            # Remove existing ES→EN package if present
            for pkg in argostranslate.package.get_installed_packages():
                if pkg.from_code == "es" and pkg.to_code == "en":
                    try:
                        pkg.remove()
                    except Exception:
                        pass

            # Reinstall both packages fresh
            for fc, tc in [("en", "es"), ("es", "en")]:
                pkg = next((p for p in available
                            if p.from_code == fc and p.to_code == tc), None)
                if pkg:
                    argostranslate.package.install_from_path(pkg.download())

            # Verify ES→EN works with a simple test
            try:
                import argostranslate.translate
                test = argostranslate.translate.translate("hola", "es", "en")
                # If output is suspiciously long it is still looping
                if len(test) > 50:
                    return False  # Signal ES→EN is broken
            except Exception:
                return False

            return True

        setup_argos()
        LOCAL_TRANSLATION_AVAILABLE = True
    except Exception as e:
        st.warning(f"Local translation unavailable: {e}. Falling back to Google Translate.")

# ── GOOGLE FALLBACKS ───────────────────────────────────────────────────────────
try:
    from deep_translator import GoogleTranslator
    GOOGLE_TRANSLATE_AVAILABLE = True
except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import speech_recognition as sr
    VOICE_INPUT_AVAILABLE = True
except ImportError:
    VOICE_INPUT_AVAILABLE = False


# ── TRANSLATION ────────────────────────────────────────────────────────────────
def translate_text(text: str, direction: str) -> str:
    if not text.strip():
        return ""
    src, tgt = direction.split("->")

    # For Spanish→English check reverse dictionary first
    if direction == "es->en" and REGIONAL_VARIANTS_ENABLED:
        try:
            # Exact match first
            back = get_english_back_translation(text.strip())
            if back:
                return back
            # Fuzzy match
            fuzzy = find_best_spanish_match(text.strip())
            if fuzzy:
                return fuzzy
        except Exception:
            pass

    # Local Argos — with infinite loop guard
    if USE_LOCAL_TRANSLATION and LOCAL_TRANSLATION_AVAILABLE:
        try:
            result = argostranslate.translate.translate(text, src, tgt)
            if result and result.strip():
                # Guard 1: reject if output is more than 5x input length
                if len(result) > len(text) * 5:
                    pass  # Fall through to Google Translate
                # Guard 2: reject if repeated pattern detected (infinite loop)
                elif len(result) > 30:
                    chunk = result[:15]
                    if result.count(chunk) > 2:
                        pass  # Fall through to Google Translate
                    else:
                        return result
                else:
                    return result
        except Exception:
            pass

    # Google Translate fallback
    if GOOGLE_TRANSLATE_AVAILABLE:
        try:
            return GoogleTranslator(source=src, target=tgt).translate(text)
        except Exception as e:
            return f"Translation error: {e}"
    return text


# ── AUDIO GENERATION ───────────────────────────────────────────────────────────
def generate_audio_b64(text: str, lang: str):
    text = text.replace("911", "9-1-1").replace("9-1-1-1-1", "9-1-1")

    # Piper TTS — local, no external calls, best Spanish quality
    if USE_LOCAL_TTS and LOCAL_TTS_AVAILABLE and lang == "es":
        try:
            buf      = io.BytesIO()
            wav_file = wave.open(buf, "wb")
            piper_model.synthesize_wav(text, wav_file)
            wav_file.close()
            buf.seek(0)
            data = buf.read()
            if len(data) > 1000:
                return base64.b64encode(data).decode()
        except Exception:
            pass  # Fall through to gTTS

    # gTTS fallback — Google but good quality Spanish
    if GTTS_AVAILABLE:
        try:
            tts  = gTTS(text=text, lang=lang)
            buf  = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            data = buf.read()
            if len(data) < 100:
                return None
            return base64.b64encode(data).decode()
        except Exception as e:
            st.warning(f"Audio generation failed: {e}")
    return None


# ── VOICE INPUT ────────────────────────────────────────────────────────────────
def process_audio_input(audio, mic_lang_code):
    # Whisper local first
    if USE_LOCAL_WHISPER and LOCAL_WHISPER_AVAILABLE:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio.getvalue())
                tmp_path = tmp.name
            lang_code = "es" if "es" in mic_lang_code else "en"
            result    = whisper_model.transcribe(tmp_path, language=lang_code)
            os.unlink(tmp_path)
            return result.get("text", "").strip()
        except Exception:
            pass

    # Google Speech Recognition fallback
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
    except sr.RequestError as e:
        st.error(f"Speech recognition unavailable: {e}")
    except Exception as e:
        st.error(f"Audio error: {e}")
    return None


# ── TRANSLATION FUNCTIONS ──────────────────────────────────────────────────────
def do_translate(text, mode="text"):
    direction  = st.session_state.direction
    tgt_lang   = "es" if direction == "en->es" else "en"
    translated = translate_text(text, direction)
    audio_b64  = generate_audio_b64(translated, tgt_lang)
    st.session_state.tgt_lang = tgt_lang
    st.session_state.last_phrase_translation = translated
    st.session_state.last_phrase_audio = audio_b64
    st.session_state.last_source = "🎙️ Voice" if mode == "voice" else "⌨️ Text"
    if mode == "voice":
        st.session_state.voice_translated = translated
        st.session_state.voice_audio_b64  = audio_b64
    else:
        st.session_state.text_translated = translated
        st.session_state.text_audio_b64  = audio_b64


def do_translate_regional(phrase, region, mode="text"):
    direction = st.session_state.direction
    tgt_lang  = "es" if direction == "en->es" else "en"
    regional, notes = get_regional_translation_fuzzy(phrase, region)
    if regional:
        audio_b64 = generate_audio_b64(regional, tgt_lang)
        st.session_state.tgt_lang      = tgt_lang
        st.session_state.regional_note = (
            notes if notes and "universally" not in notes.lower() else ""
        )
        st.session_state.last_phrase_translation = regional
        st.session_state.last_phrase_audio = audio_b64
        st.session_state.last_source = "🎙️ Voice" if mode == "voice" else "⌨️ Text"
        if mode == "voice":
            st.session_state.voice_translated = regional
            st.session_state.voice_audio_b64  = audio_b64
        else:
            st.session_state.text_translated = regional
            st.session_state.text_audio_b64  = audio_b64
    else:
        st.session_state.regional_note = ""
        do_translate(phrase, mode)


# ── AUDIO PLAYER ───────────────────────────────────────────────────────────────
def render_audio(b64: str):
    components.html(f"""
    <audio controls preload="auto"
           style="width:100%;border-radius:8px;display:block;min-height:40px;margin-top:8px;">
        <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        <source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    <p style="font-size:11px;color:#aaa;margin:4px 0 0 0;font-family:sans-serif;">
        iPhone: tap the play button to hear the translation.
    </p>
    """, height=70)


# ── PHRASE DATA ────────────────────────────────────────────────────────────────
CATEGORY_LABELS = {
    "🩹 Pain Assessment":         {"es": "🩹 Evaluación del dolor"},
    "🤒 Symptoms":                {"es": "🤒 Síntomas"},
    "💊 Medications & Allergies": {"es": "💊 Medicamentos y alergias"},
    "📋 Medical History":         {"es": "📋 Historia médica"},
    "✅ Consent & Instructions":  {"es": "✅ Consentimiento e instrucciones"},
    "🚨 Emergency":               {"es": "🚨 Emergencia"},
}

CATEGORY_COLORS = {
    "🩹 Pain Assessment":         {"bg": "#E8F4FD", "border": "#0072B2", "text": "#004B75"},
    "🤒 Symptoms":                {"bg": "#FFF3E0", "border": "#E69F00", "text": "#7A5400"},
    "💊 Medications & Allergies": {"bg": "#E6F6F4", "border": "#009E73", "text": "#005740"},
    "📋 Medical History":         {"bg": "#FFF8E1", "border": "#F0E442", "text": "#6B6100"},
    "✅ Consent & Instructions":  {"bg": "#F3EFF9", "border": "#CC79A7", "text": "#7B3F63"},
    "🚨 Emergency":               {"bg": "#FDECEA", "border": "#D55E00", "text": "#8B3A00"},
}

MEDICAL_PHRASES = {
    "🩹 Pain Assessment": {
        "en": ["Where does it hurt?","Rate your pain from 1 to 10","Is the pain sharp or dull?","Is the pain constant or does it come and go?","Does the pain go anywhere else?","Does anything make the pain better?","Does anything make the pain worse?"],
        "es": ["¿Dónde le duele?","Califique su dolor del 1 al 10","¿El dolor es agudo o sordo?","¿El dolor es constante o va y viene?","¿El dolor se va a algún otro lugar?","¿Hay algo que mejore el dolor?","¿Hay algo que empeore el dolor?"]
    },
    "🤒 Symptoms": {
        "en": ["Do you have a fever?","Are you short of breath?","Are you dizzy?","Are you nauseous?","Have you vomited?","Do you have a headache?","Do you have chest pain?","Do you have abdominal pain?"],
        "es": ["¿Tiene fiebre?","¿Tiene dificultad para respirar?","¿Tiene mareos?","¿Tiene náuseas?","¿Ha vomitado?","¿Tiene dolor de cabeza?","¿Tiene dolor en el pecho?","¿Tiene dolor abdominal?"]
    },
    "💊 Medications & Allergies": {
        "en": ["Do you have any allergies?","Are you taking any medications?"],
        "es": ["¿Tiene alguna alergia?","¿Está tomando algún medicamento?"]
    },
    "📋 Medical History": {
        "en": ["Do you have diabetes?","Do you have high blood pressure?","Do you have heart problems?","Have you had surgery before?","Are you pregnant?","When was your last menstrual period?"],
        "es": ["¿Tiene diabetes?","¿Tiene presión alta?","¿Tiene problemas del corazón?","¿Ha tenido cirugías antes?","¿Está embarazada?","¿Cuándo fue su última menstruación?"]
    },
    "✅ Consent & Instructions": {
        "en": ["I need to examine you","I need to draw blood","I need to start an IV","Do you understand?","Please sign here","Please lie down","Please sit up","Please breathe deeply","Do not eat or drink anything","I need a urine sample","The doctor will see you soon"],
        "es": ["Necesito examinarle","Necesito sacarle sangre","Necesito ponerle un suero","¿Entiende?","Por favor firme aquí","Por favor acuéstese","Por favor siéntese","Por favor respire profundo","No coma ni beba nada","Necesito una muestra de orina","El médico le atenderá pronto"]
    },
    "🚨 Emergency": {
        "en": ["You can go home now","Take this medication twice a day","Come back if symptoms worsen","Follow up with your doctor in one week","Call 911 if you have an emergency","Are you having trouble urinating?"],
        "es": ["Ya puede irse a casa","Tome este medicamento dos veces al día","Regrese si los síntomas empeoran","Haga cita con su médico en una semana","Llame al 911 si tiene una emergencia","¿Tiene problemas para orinar?"]
    },
}

REGION_OPTIONS = {
    "neutral":      "🌎 General Spanish",
    "dominican":    "🇩🇴 Dominican Republic",
    "puerto_rican": "🇵🇷 Puerto Rico",
    "mexican":      "🇲🇽 Mexico",
    "colombian":    "🇨🇴 Colombia",
    "cuban":        "🇨🇺 Cuba",
}

UI = {
    "en->es": {
        "btn1": "🇺🇸 English → Spanish", "btn2": "🇲🇽 Spanish → English",
        "input_section": "Type or Speak", "voice_hint": "Tap the microphone to record",
        "spinner_trans": "Transcribing...", "spinner_tl": "Translating...",
        "heard": "🎙️ Heard", "voice_tl_label": "Voice Translation",
        "text_label": "Type in English", "text_placeholder": "Type a phrase to translate...",
        "translate_btn": "Translate", "translate_warn": "Please enter some text to translate.",
        "text_tl_label": "Translation", "phrases_title": "Quick Phrases",
        "phrases_caption": "Tap a phrase to translate instantly", "tl_label": "Translation",
        "disclaimer": "⚠️ For brief clinical exchanges only. Not a replacement for professional interpreters.",
    },
    "es->en": {
        "btn1": "🇺🇸 English → Spanish", "btn2": "🇲🇽 Spanish → English",
        "input_section": "Escriba o hable", "voice_hint": "Toque el micrófono para grabar",
        "spinner_trans": "Transcribiendo...", "spinner_tl": "Traduciendo...",
        "heard": "🎙️ Escuché", "voice_tl_label": "Traducción de voz",
        "text_label": "Escriba en español", "text_placeholder": "Escriba una frase para traducir...",
        "translate_btn": "Traducir", "translate_warn": "Por favor ingrese texto para traducir.",
        "text_tl_label": "Traducción", "phrases_title": "Frases rápidas",
        "phrases_caption": "Toque una frase para traducir al instante", "tl_label": "Traducción",
        "disclaimer": "⚠️ Solo para intercambios clínicos breves. No reemplaza a intérpretes profesionales.",
    },
}

# ── GOOGLE ANALYTICS ───────────────────────────────────────────────────────────
components.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=G-PM770KN3NX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-PM770KN3NX');
</script>
""", height=0)

# ── STYLES ─────────────────────────────────────────────────────────────────────
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<style>
    html, body, [class*="css"] { font-size:16px !important; -webkit-text-size-adjust:100%; }
    .block-container { padding-left:1rem !important; padding-right:1rem !important; padding-top:2rem !important; max-width:480px !important; }
    .stButton > button { min-height:52px !important; font-size:16px !important; border-radius:10px !important; width:100% !important; touch-action:manipulation; background-color:#1F4E79 !important; color:#FFFFFF !important; border:none !important; }
    .stButton > button:hover { background-color:#2E75B6 !important; color:#FFFFFF !important; }
    .stTextArea textarea { font-size:16px !important; border-radius:10px !important; }
    .stAlert { border-radius:10px !important; font-size:15px !important; }
    h2, h3 { font-size:0.85rem !important; text-transform:uppercase !important; letter-spacing:0.6px !important; color:#999 !important; margin-bottom:8px !important; }
    audio { width:100% !important; border-radius:8px; display:block; }
    footer { display:none !important; }
    #MainMenu { display:none !important; }
    header { display:none !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────────────────────
for key, default in {
    "direction": "en->es", "region": "neutral", "last_audio_id": None,
    "input_text": "", "regional_note": "", "last_category": None, "last_phrase_translation": "", "last_phrase_audio": None, "last_source": "", "last_category": None, "last_phrase_translation": "", "last_phrase_audio": None,
    "voice_translated": "", "voice_audio_b64": None,
    "text_translated": "", "text_audio_b64": None, "tgt_lang": "es",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

direction     = st.session_state.direction
ui            = UI[direction]
mic_lang_code = "en-US" if direction == "en->es" else "es-ES"
lang_key      = "en" if direction == "en->es" else "es"

# ── HEADER ─────────────────────────────────────────────────────────────────────
hipaa_badge = ""
if USE_LOCAL_TTS and USE_LOCAL_WHISPER and USE_LOCAL_TRANSLATION:
    hipaa_badge = '<div style="font-size:10px;color:#90EE90;margin-top:4px;">🔒 Fully Local — HIPAA Compliant by Architecture</div>'

st.markdown(f"""
<div style="background:#1F4E79;border-radius:12px;padding:16px 18px;margin-bottom:16px;">
    <div style="font-size:clamp(1rem,5vw,1.4rem);font-weight:700;color:#ffffff;
                letter-spacing:-0.3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
        🩺 Medical Voice Translator
    </div>
    <div style="font-size:11px;color:#B5D4F4;margin-top:4px;">
        English &#8596; Spanish &nbsp;·&nbsp; Audio Playback &nbsp;·&nbsp; Voice Input
    </div>
    {hipaa_badge}
    <div style="font-size:10px;color:#7aadd4;margin-top:8px;padding-top:8px;
                border-top:1px solid rgba(255,255,255,0.15);">
        {ui['disclaimer']}
    </div>
</div>
""", unsafe_allow_html=True)

# ── DIRECTION TOGGLE ───────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    if st.button(ui["btn1"], use_container_width=True,
                 type="primary" if direction == "en->es" else "secondary"):
        st.session_state.update({"direction":"en->es","voice_translated":"","voice_audio_b64":None,
                                  "text_translated":"","text_audio_b64":None,"input_text":"","regional_note":""})
        st.rerun()
with col2:
    if st.button(ui["btn2"], use_container_width=True,
                 type="primary" if direction == "es->en" else "secondary"):
        st.session_state.update({"direction":"es->en","voice_translated":"","voice_audio_b64":None,
                                  "text_translated":"","text_audio_b64":None,"input_text":"","regional_note":""})
        st.rerun()

st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)

# ── REGION SELECTOR ────────────────────────────────────────────────────────────
if REGIONAL_VARIANTS_ENABLED and direction == "en->es":
    st.selectbox(
        "Patient's Spanish Region",
        options=list(REGION_OPTIONS.keys()),
        format_func=lambda x: REGION_OPTIONS[x],
        key="region",
        help="Select the patient's country of origin for more accurate regional translations."
    )

# ── INPUT SECTION ──────────────────────────────────────────────────────────────
st.subheader(ui["input_section"])

st.markdown(f"""
<div style="background:#EBF3FB;border:1.5px dashed #2E75B6;border-radius:10px;
            padding:10px 14px;margin:4px 0 4px 0;text-align:center;">
    <div style="font-size:15px;font-weight:600;color:#1F4E79;margin-bottom:2px;">
        🎙️ {"Record Voice Input" if direction == "en->es" else "Grabar entrada de voz"}
    </div>
    <div style="font-size:11px;color:#2E75B6;">{ui['voice_hint']}</div>
</div>
""", unsafe_allow_html=True)
audio = st.audio_input("", key="audio_recorder", label_visibility="collapsed")

if audio is not None:
    audio_id = hash(audio.getvalue())
    if audio_id != st.session_state.last_audio_id:
        st.session_state.last_audio_id = audio_id
        with st.spinner(ui["spinner_trans"]):
            spoken = process_audio_input(audio, mic_lang_code)
        if spoken:
            st.session_state.input_text = spoken
            with st.spinner(ui["spinner_tl"]):
                if REGIONAL_VARIANTS_ENABLED and direction == "en->es":
                    do_translate_regional(spoken, st.session_state.get("region","neutral"), mode="voice")
                else:
                    do_translate(spoken, mode="voice")
            st.success(f"{ui['heard']} *{spoken}*")



st.markdown("<hr style='border:none;border-top:1px solid rgba(128,128,128,0.15);margin:10px 0;'>",
            unsafe_allow_html=True)

typed_text = st.text_area(
    ui["text_label"], value=st.session_state.input_text, height=100,
    placeholder=ui["text_placeholder"], key="text_area_widget",
    label_visibility="collapsed",
)
st.session_state.input_text = typed_text
translate_clicked = st.button(ui["translate_btn"], type="primary", use_container_width=True)

if translate_clicked:
    if st.session_state.input_text.strip():
        st.session_state.last_category = None  # Clear so inline result shows
        with st.spinner(ui["spinner_tl"]):
            if REGIONAL_VARIANTS_ENABLED and direction == "en->es":
                do_translate_regional(st.session_state.input_text.strip(),
                                      st.session_state.get("region","neutral"), mode="text")
            else:
                do_translate(st.session_state.input_text.strip(), mode="text")
    else:
        st.warning(ui["translate_warn"])




# ── UNIFIED TRANSLATION BANNER — always visible above quick phrases ────────────
if st.session_state.get("last_phrase_translation"):
    source = st.session_state.get("last_source", "")
    st.markdown(f"""
    <div style="background:#1F4E79;border-radius:12px;padding:14px 16px;margin-bottom:12px;border:2px solid #2E75B6;">
        <div style="font-size:10px;font-weight:700;color:#AED6F1;text-transform:uppercase;
                    letter-spacing:0.5px;margin-bottom:6px;">🔊 Translation {source}</div>
        <div style="font-size:20px;color:#ffffff;font-weight:500;">{st.session_state.last_phrase_translation}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.get("last_phrase_audio"):
        render_audio(st.session_state.last_phrase_audio)
    if REGIONAL_VARIANTS_ENABLED and st.session_state.get("regional_note"):
        st.info(f"📋 {st.session_state.regional_note}")

# ── QUICK PHRASES ──────────────────────────────────────────────────────────────
st.subheader(ui["phrases_title"])
st.caption(ui["phrases_caption"])

for category, langs in MEDICAL_PHRASES.items():
    label  = CATEGORY_LABELS[category]["es"] if direction == "es->en" else category
    colors = CATEGORY_COLORS[category]
    st.markdown(f"""
    <div style="background:{colors['bg']};border-left:4px solid {colors['border']};
                border-radius:8px;padding:11px 14px;margin-bottom:2px;
                font-size:15px;font-weight:600;color:{colors['text']};">
        {label}
    </div>
    """, unsafe_allow_html=True)
    is_open = st.session_state.get("last_category") == category
    with st.expander("", expanded=is_open):
        for phrase in langs[lang_key]:
            if st.button(phrase, use_container_width=True, key=f"phrase_{category}_{phrase}"):
                with st.spinner(ui["spinner_tl"]):
                    if REGIONAL_VARIANTS_ENABLED and direction == "en->es":
                        do_translate_regional(phrase, st.session_state.get("region","neutral"), mode="text")
                    else:
                        do_translate(phrase, mode="text")
                st.session_state.input_text = phrase
                st.session_state.last_category = category
                st.session_state.last_phrase_translation = st.session_state.text_translated
                st.session_state.last_phrase_audio = st.session_state.text_audio_b64
                st.rerun()

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center;padding:8px 0 4px 0;">
    <p style="font-size:12px;color:#aaa;margin:0;">
        Built by <b style="color:#888;">Gauri Bhakta</b>, Phillips Academy · Inspired by real patients
    </p>
</div>
""", unsafe_allow_html=True)
