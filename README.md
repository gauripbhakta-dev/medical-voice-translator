# 🩺 Medical Voice Translator

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21879051.svg)](https://doi.org/10.5281/zenodo.21879051)


A free, browser-based bilingual clinical communication tool for English-Spanish translation in emergency department and hospital settings, designed for use with limited English proficiency (LEP) patients.

**Live App:** [medvoice-translator.streamlit.app](https://medvoice-translator.streamlit.app)

---

## About

Built by **Gauri Bhakta**, a Phillips Academy Andover student and Lawrence General Hospital Emergency Department volunteer, after observing firsthand that language barriers between clinical staff and Spanish-speaking patients created preventable communication failures and health equity gaps.

The app provides instant point-of-care translation with community-specific regional Spanish variants — recognizing that a Dominican patient may not recognize "diabetes" but responds to "azúcar," and that a Puerto Rican patient uses "el servicio" for bathroom rather than "el baño."

---

## Features

- 🌎 **Regional Spanish variants** — 6 community-specific dialects: Dominican Republic, Puerto Rico, Mexico, Colombia, Cuba, and General Spanish
- 🔄 **Bidirectional translation** — English → Spanish and Spanish → English
- 🎙️ **Self-hosted voice input** — OpenAI Whisper (tiny model) transcribes speech within the app, without sending audio to a cloud speech service
- 🔊 **Self-hosted audio playback** — Piper TTS (es_MX-claude-high) generates natural Spanish audio within the app, without external API calls
- 🔒 **Privacy-first design** — core processing runs within the app instead of third-party translation services (see note below on the public demo)
- 📱 **Zero installation** — works on any phone or tablet browser, no app download required
- 🏥 **53 clinical phrases** across 7 categories

## Phrase Categories

| Category | Phrases |
|---|---|
| 🛏️ Comfort & Care | 13 |
| 🩹 Pain Assessment | 7 |
| 🤒 Symptoms | 8 |
| 💊 Medications & Allergies | 2 |
| 📋 Medical History | 6 |
| ✅ Consent & Instructions | 11 |
| 🚨 Emergency | 6 |

---

## Architecture — Self-Hosted Processing

| Component | Library | License | Replaces |
|---|---|---|---|
| UI Framework | Streamlit 1.35 | Apache 2.0 | — |
| Translation | Argos Translate 1.9.1 | MIT | Google Translate API |
| Text-to-Speech | Piper TTS (es_MX-claude-high) | MIT | Google gTTS |
| Speech Recognition | OpenAI Whisper tiny | MIT | Web Speech API |
| Regional Routing | Custom Jaccard fuzzy matching | — | None |

All four core components run inside the app on its host server, rather than through third-party translation or speech APIs. For the public demo, that server is Streamlit Community Cloud, not the user's device.

**Public demo note:** Piper generates Spanish audio only; English audio playback uses Google text-to-speech. If a local component fails to load, the app also falls back to Google Translate or Google speech recognition, and it uses Google Analytics for anonymous usage statistics. For these reasons, the public demo is **not HIPAA-compliant** and should not be used with real patient information. The design is intended to support a fully self-hosted deployment in a clinical setting in the future.

---

## Intellectual Property

A provisional patent application (USPTO Application No. 64/105,618, filed July 6, 2026) is pending covering the language community lexical routing system described in this project.

Inventor: Gauri P. Bhakta. Legal Guardian: Prashant Kumar.

---

## Research

A peer-reviewed research paper is in preparation in collaboration with **Dr. Diana Rojas-Soto, MD** (Dartmouth Geisel School of Medicine, Co-Director, Medical Spanish Pathway of Distinction). Target journal: JAMIA Open.

The Comfort & Care phrase category was developed based on clinical feedback from **Dr. Alisa Khan, MD, MPH** (Director, Program for Language Equity, Boston Children's Hospital; Harvard Medical School).

---

## Clinical Context

Language barriers affect approximately 25 million Americans with limited English proficiency and represent a persistent source of health inequity and preventable clinical error. This tool was developed through direct observation at Lawrence General Hospital Emergency Department and clinical consultation with Harvard Medical School and Dartmouth Geisel School of Medicine faculty.

---

## How to Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/gauripbhakta-dev/medical-voice-translator.git
cd medical-voice-translator
```

**2. Install dependencies**
```bash
pip install -r artifacts/medical-voice-translator/requirements.txt
apt-get install espeak-ng
```

**3. Run the app**
```bash
streamlit run artifacts/medical-voice-translator/app.py
```

---

## Project Structure

```
medical-voice-translator/
├── artifacts/
│   └── medical-voice-translator/
│       ├── app.py                        # Main Streamlit app
│       ├── regional_medical_spanish.py   # Regional variant dictionary
│       ├── test_app.py                   # Automated test suite (15 tests)
│       ├── requirements.txt              # Python dependencies
│       ├── packages.txt                  # System dependencies (espeak-ng)
│       ├── es_MX-claude-high.onnx        # Piper TTS voice model
│       └── es_MX-claude-high.onnx.json   # Piper TTS voice config
└── README.md
```

---

## Deployment

Deployed on **Streamlit Community Cloud** with automatic redeployment on push to `main`. UptimeRobot monitors availability.

---

## Disclaimer

For communication assistance only. Not a substitute for a certified medical interpreter for complex clinical conversations.

---


## Citation

Bhakta, G. P. (2026). Precision Communication: A Lexical Routing Approach to
Community-Specific Clinical Translation for Spanish-Speaking Patients (Version v1).
Zenodo. https://doi.org/10.5281/zenodo.21879051



*Built by **Gauri P Bhakta** · Phillips Academy Andover · Class of 2028 · gauripbhakta@gmail.com*

