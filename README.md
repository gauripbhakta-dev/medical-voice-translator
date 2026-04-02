# 🩺 Medical Voice Translator

A web app that helps hospital staff communicate with Spanish-speaking patients by translating medical phrases between English and Spanish — with voice input and audio playback.

**Live App:** [medvoice-translator.streamlit.app](https://medvoice-translator.streamlit.app)

---

## About

Built by **Gauri Bhakta**, a 10th grade student and hospital volunteer, after noticing that language barriers made it difficult for staff to communicate with Spanish-speaking patients. This app provides a fast, phone-friendly tool that any staff member can use without downloading anything.

---

## Features

- 🔄 **Bidirectional translation** — English → Spanish and Spanish → English
- 🎙️ **Voice input** — record your phrase and it auto-transcribes and translates
- 🔊 **Audio playback** — hear the translation spoken aloud for the patient
- ⚕️ **36 preset clinical phrases** across 6 categories:
  - Pain Assessment
  - Symptoms
  - Medications & Allergies
  - Medical History
  - Consent & Instructions
  - Emergency
- 🌐 **Full bilingual UI** — the entire interface switches to Spanish when in ES → EN mode
- 📱 **Mobile optimized** — works on iPhone, Android, and desktop
- 🔒 **No data stored** — nothing is recorded or saved

---

## Disclaimer

For communication assistance only. Not a substitute for a certified medical interpreter.

---

## Tech Stack

| Component | Technology |
|---|---|
| UI Framework | Streamlit |
| Translation | deep-translator (Google Translate) |
| Text-to-Speech | gTTS (Google Text-to-Speech) |
| Voice Input | SpeechRecognition + st.audio_input |
| Deployment | Streamlit Community Cloud |
| Version Control | GitHub |

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
│       ├── app.py               # Main Streamlit app
│       ├── requirements.txt     # Python dependencies
│       └── .streamlit/
│           └── config.toml      # Streamlit server config
└── README.md
```

---

## Deployment

The app is deployed on **Streamlit Community Cloud** and automatically redeploys whenever code is pushed to the `main` branch on GitHub.

---

## Background

This project was developed as part of a hospital volunteer experience where language barriers between staff and Spanish-speaking patients were a recurring challenge. The app was designed to be simple enough for any staff member to pick up and use immediately — no training required.

---

## Future Improvements

- [ ] Add more language pairs (Portuguese, French, Mandarin, Arabic)
- [ ] Expand phrase library with more clinical scenarios
- [ ] Offline mode for areas with poor connectivity
- [ ] Export translation session as PDF
- [ ] Collect staff feedback through in-app survey

---

*Built with ❤️ by Gauri Bhakta — Grade 10*
