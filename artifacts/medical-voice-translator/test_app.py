"""
Medical Voice Translator — Automated System Test Suite
=======================================================
Run before every deployment to verify all functionality.

Usage:
    cd ~/Desktop/medical-voice-translator
    source venv/bin/activate
    python3 artifacts/medical-voice-translator/test_app.py

Exit codes:
    0 = all tests passed — safe to deploy
    1 = one or more tests failed — do not deploy
"""

import os
import sys
import io
import wave
import base64
import traceback

APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

passed = 0
failed = 0
total  = 0

def header(msg):
    print(f"\n{BLUE}{BOLD}{msg}{RESET}")

def ok(msg):
    print(f"  {GREEN}✅ {msg}{RESET}")

def fail(msg):
    print(f"  {RED}❌ {msg}{RESET}")

def warn(msg):
    print(f"  {YELLOW}⚠️  {msg}{RESET}")

def test(name, fn):
    global passed, failed, total
    total += 1
    print(f"\n[{total}] Testing {name}...")
    try:
        result = fn()
        if result:
            print(f"  {GREEN}{BOLD}PASSED ✅{RESET}")
            passed += 1
        else:
            print(f"  {RED}{BOLD}FAILED ❌{RESET}")
            failed += 1
    except Exception as e:
        print(f"  {RED}{BOLD}FAILED ❌ — {e}{RESET}")
        traceback.print_exc()
        failed += 1

# ── TEST 1: Dictionary Import ─────────────────────────────────────────────────
def test_dictionary_import():
    from regional_medical_spanish import (
        REGIONAL_VARIANTS,
        get_regional_translation,
        get_regional_translation_fuzzy,
        find_best_match
    )
    count = len(REGIONAL_VARIANTS)
    ok(f"Dictionary loaded — {count} phrases found")
    assert count >= 30, f"Expected at least 30 phrases, got {count}"
    return True

# ── TEST 2: All Phrase Categories Present ────────────────────────────────────
def test_phrase_categories():
    from regional_medical_spanish import REGIONAL_VARIANTS
    required_phrases = [
        "Do you have a fever?",
        "Do you have diabetes?",
        "Where does it hurt?",
        "Are you nauseous?",
        "Do not eat or drink anything",
        "Are you pregnant?",
    ]
    for phrase in required_phrases:
        assert phrase in REGIONAL_VARIANTS, f"Missing phrase: {phrase}"
        ok(f"Found: '{phrase}'")
    return True

# ── TEST 3: Critical Regional Variants ───────────────────────────────────────
def test_critical_regional_variants():
    from regional_medical_spanish import get_regional_translation
    critical_tests = [
        ("Do you have a fever?",        "dominican",    "calentura",  "Dominican fever"),
        ("Do you have diabetes?",        "dominican",    "azúcar",     "Dominican diabetes"),
        ("Do you have diabetes?",        "puerto_rican", "azúcar",     "Puerto Rican diabetes"),
        ("Are you nauseous?",            "dominican",    "vomitar",    "Dominican nausea"),
        ("Do not eat or drink anything", "dominican",    "tome",       "Dominican NPO"),
        ("Do not eat or drink anything", "puerto_rican", "tome",       "Puerto Rican NPO"),
    ]
    all_passed = True
    for phrase, region, expected_fragment, label in critical_tests:
        translation, notes = get_regional_translation(phrase, region)
        if translation and expected_fragment.lower() in translation.lower():
            ok(f"{label}: '{translation}'")
        else:
            fail(f"{label}: expected '{expected_fragment}' in '{translation}'")
            all_passed = False
    return all_passed

# ── TEST 4: All Six Regions ───────────────────────────────────────────────────
def test_all_regions():
    from regional_medical_spanish import get_regional_translation
    regions = ["neutral","dominican","puerto_rican","mexican","colombian","cuban"]
    phrase  = "Do you have a fever?"
    all_passed = True
    for region in regions:
        translation, _ = get_regional_translation(phrase, region)
        if translation:
            ok(f"{region}: '{translation}'")
        else:
            fail(f"{region}: no translation returned")
            all_passed = False
    return all_passed

# ── TEST 5: Fuzzy Matching ────────────────────────────────────────────────────
def test_fuzzy_matching():
    from regional_medical_spanish import find_best_match
    fuzzy_tests = [
        ("do you have a fever",    "Do you have a fever?",    "lowercase no punctuation"),
        ("DO YOU HAVE A FEVER",    "Do you have a fever?",    "uppercase"),
        ("do you have diabetes",   "Do you have diabetes?",   "diabetes lowercase"),
        ("where does it hurt",     "Where does it hurt?",     "pain lowercase"),
        ("are you nauseous",       "Are you nauseous?",       "nauseous lowercase"),
        ("do you have a fever?",   "Do you have a fever?",    "exact with punctuation"),
    ]
    all_passed = True
    for input_text, expected_key, label in fuzzy_tests:
        matched = find_best_match(input_text)
        if matched == expected_key:
            ok(f"{label}: '{input_text}' → '{matched}'")
        else:
            fail(f"{label}: '{input_text}' → got '{matched}', expected '{expected_key}'")
            all_passed = False
    garbage_match = find_best_match("xyzzy nonsense words")
    if garbage_match is None:
        ok("Garbage input correctly returns None")
    else:
        fail(f"Garbage input matched: '{garbage_match}'")
        all_passed = False
    return all_passed

# ── TEST 6: Fuzzy Regional Translation End-to-End ────────────────────────────
def test_fuzzy_regional_translation():
    from regional_medical_spanish import get_regional_translation_fuzzy
    tests = [
        ("do you have a fever",  "dominican",    "calentura"),
        ("do you have diabetes", "dominican",    "azúcar"),
        ("DO YOU HAVE DIABETES", "puerto_rican", "azúcar"),
        ("are you nauseous",     "dominican",    "vomitar"),
    ]
    all_passed = True
    for input_text, region, expected in tests:
        translation, _ = get_regional_translation_fuzzy(input_text, region)
        if translation and expected.lower() in translation.lower():
            ok(f"'{input_text}' [{region}] → '{translation}'")
        else:
            fail(f"'{input_text}' [{region}] → got '{translation}', expected '{expected}'")
            all_passed = False
    return all_passed

# ── TEST 7: Piper TTS ─────────────────────────────────────────────────────────
def test_piper_tts():
    try:
        from piper.voice import PiperVoice
        onnx_path = os.path.join(APP_DIR, "es_MX-claude-high.onnx")
        json_path = os.path.join(APP_DIR, "es_MX-claude-high.onnx.json")
        if not os.path.exists(onnx_path):
            warn("Piper model not found — skipping")
            return True
        voice = PiperVoice.load(onnx_path, config_path=json_path)
        ok("Piper model loaded successfully")
        test_phrases = ["¿Tiene fiebre?", "¿Tiene azúcar?", "¿Dónde le duele?"]
        all_passed = True
        for phrase in test_phrases:
            buf      = io.BytesIO()
            wav_file = wave.open(buf, "wb")
            voice.synthesize_wav(phrase, wav_file)
            wav_file.close()
            buf.seek(0)
            size = len(buf.read())
            if size > 1000:
                ok(f"'{phrase}' — {size:,} bytes")
            else:
                fail(f"'{phrase}' — audio too small: {size} bytes")
                all_passed = False
        return all_passed
    except ImportError:
        warn("piper-tts not installed — skipping")
        return True

# ── TEST 8: Argos Translation ─────────────────────────────────────────────────
def test_argos_translation():
    """
    Tests local Argos translation is installed and working.
    Used as fallback when regional dictionary has no match.
    """
    try:
        import argostranslate.translate
        installed = argostranslate.translate.get_installed_languages()
        codes = [lang.code for lang in installed]
        if "en" not in codes or "es" not in codes:
            warn("Argos EN/ES packages not installed — run setup: see README")
            warn("Free text translation will fall back to Google Translate")
            return True  # Not blocking — app still works with Google fallback
        result_es = argostranslate.translate.translate("Do you have a fever?", "en", "es")
        if result_es and len(result_es) > 3:
            ok(f"EN→ES working: 'Do you have a fever?' → '{result_es}'")
        else:
            fail(f"EN→ES failed: '{result_es}'")
            return False
        result_en = argostranslate.translate.translate("¿Tiene fiebre?", "es", "en")
        if result_en and len(result_en) > 3:
            ok(f"ES→EN working: '¿Tiene fiebre?' → '{result_en}'")
        else:
            fail(f"ES→EN failed: '{result_en}'")
            return False
        ok("Argos local translation fully operational — no Google Translate needed for free text")
        return True
    except ImportError:
        warn("argostranslate not installed — Google Translate will be used as fallback")
        return True  # Not blocking

# ── TEST 9: Whisper Model ─────────────────────────────────────────────────────
def test_whisper():
    try:
        import whisper
        model = whisper.load_model("tiny")
        ok("Whisper tiny model loaded successfully")
        assert hasattr(model, "transcribe"), "Whisper model missing transcribe method"
        ok("Whisper transcribe method available")
        return True
    except ImportError:
        warn("openai-whisper not installed — skipping")
        return True
    except Exception as e:
        fail(f"Whisper error: {e}")
        return False

# ── TEST 10: Feature Flags ────────────────────────────────────────────────────
def test_feature_flags():
    with open(os.path.join(APP_DIR, "app.py")) as f:
        content = f.read()
    flags = [
        "REGIONAL_VARIANTS_ENABLED",
        "USE_LOCAL_TTS",
        "USE_LOCAL_WHISPER",
        "USE_LOCAL_TRANSLATION",
    ]
    all_found = True
    for flag in flags:
        if flag in content:
            for line in content.split("\n"):
                if flag in line and "=" in line and not line.strip().startswith("#") and "==" not in line:
                    parts = line.split("=")
                    if len(parts) >= 2:
                        value = parts[1].strip().split("#")[0].strip()
                        ok(f"{flag} = {value}")
                        break
        else:
            fail(f"Flag not found in app.py: {flag}")
            all_found = False
    return all_found

# ── TEST 11: App File Integrity ───────────────────────────────────────────────
def test_app_file_integrity():
    app_path = os.path.join(APP_DIR, "app.py")
    assert os.path.exists(app_path), "app.py not found"
    with open(app_path) as f:
        content = f.read()
    required_components = [
        ("import streamlit",           "Streamlit import"),
        ("REGIONAL_VARIANTS_ENABLED",  "Regional variants flag"),
        ("USE_LOCAL_TTS",              "Local TTS flag"),
        ("USE_LOCAL_WHISPER",          "Local Whisper flag"),
        ("USE_LOCAL_TRANSLATION",      "Local translation flag"),
        ("def generate_audio_b64",     "Audio generation function"),
        ("def do_translate",           "Translation function"),
        ("def do_translate_regional",  "Regional translation function"),
        ("MEDICAL_PHRASES",            "Medical phrases dictionary"),
        ("G-PM770KN3NX",               "Google Analytics tag"),
        ("phrase_{category}_{phrase}", "Duplicate key fix"),
        ("piper_model",                "Piper TTS integration"),
        ("kokoro" not in content.lower(), "Kokoro completely removed"),
    ]
    all_found = True
    for component, label in required_components:
        if isinstance(component, bool):
            if component:
                ok(f"Verified: {label}")
            else:
                fail(f"Failed: {label}")
                all_found = False
        elif component in content:
            ok(f"Found: {label}")
        else:
            fail(f"Missing: {label}")
            all_found = False

    # Verify Kokoro is NOT in audio pipeline
    if "kokoro" in content.lower():
        warn("Kokoro reference found in app.py — verify it is not in audio pipeline")
    else:
        ok("Kokoro completely removed from app")

    return all_found

# ── TEST 12: Required Model Files ─────────────────────────────────────────────
def test_model_files():
    files = {
        "es_MX-claude-high.onnx":      (50_000_000, "Piper Spanish model"),
        "es_MX-claude-high.onnx.json": (1_000,      "Piper Spanish config"),
        "regional_medical_spanish.py":  (1_000,      "Regional dictionary"),
    }
    all_found = True
    for filename, (min_size, label) in files.items():
        path = os.path.join(APP_DIR, filename)
        if os.path.exists(path):
            size = os.path.getsize(path)
            if size >= min_size:
                ok(f"{label}: {size/1_000_000:.1f}MB ✓")
            else:
                fail(f"{label}: too small ({size} bytes)")
                all_found = False
        else:
            fail(f"{label}: not found at {path}")
            all_found = False
    return all_found

# ── TEST 13: No Leftover Test Files ──────────────────────────────────────────
def test_no_test_files():
    import glob
    patterns = [
        os.path.join(APP_DIR, "test_*.wav"),
        os.path.join(APP_DIR, "test_*.html"),
        "/tmp/piper_*.html",
        "/tmp/test_piper*.wav",
    ]
    found_files = []
    for pattern in patterns:
        found_files.extend(glob.glob(pattern))
    if not found_files:
        ok("No leftover test files found")
        return True
    else:
        for f in found_files:
            fail(f"Leftover test file: {f}")
        return False

# ── TEST 14: Packages.txt Exists ─────────────────────────────────────────────
def test_packages_txt():
    # packages.txt should be in repo root (two levels up from app dir)
    repo_root    = os.path.dirname(os.path.dirname(APP_DIR))
    packages_path = os.path.join(repo_root, "packages.txt")
    if os.path.exists(packages_path):
        with open(packages_path) as f:
            content = f.read()
        if "espeak-ng" in content:
            ok(f"packages.txt found with espeak-ng at {packages_path}")
            return True
        else:
            fail(f"packages.txt found but missing espeak-ng: {packages_path}")
            return False
    else:
        fail(f"packages.txt not found at {packages_path}")
        return False


# ── TEST 15: Phrase Consistency — app.py and dictionary match ────────────────
def test_phrase_consistency():
    """
    Verify every English phrase in app.py MEDICAL_PHRASES exists in the
    regional dictionary. Prevents mismatch between EN→ES and ES→EN directions.
    """
    import re
    from regional_medical_spanish import REGIONAL_VARIANTS, SPANISH_TO_ENGLISH

    app_content = open(os.path.join(APP_DIR, "app.py")).read()

    # Extract English phrases from MEDICAL_PHRASES
    matches = re.findall(r'"en":\s*\[(.*?)\]', app_content, re.DOTALL)
    app_english_phrases = []
    for match in matches:
        phrases = re.findall(r'"([^"]+)"', match)
        app_english_phrases.extend(phrases)

    # Extract Spanish phrases from MEDICAL_PHRASES
    matches = re.findall(r'"es":\s*\[(.*?)\]', app_content, re.DOTALL)
    app_spanish_phrases = []
    for match in matches:
        phrases = re.findall(r'"([^"]+)"', match)
        app_spanish_phrases.extend(phrases)

    all_passed = True

    # Check every English phrase is in dictionary
    missing_en = [p for p in app_english_phrases if p not in REGIONAL_VARIANTS]
    if missing_en:
        for p in missing_en:
            fail(f"English phrase in app.py not in dictionary: '{p}'")
            all_passed = False
    else:
        ok(f"All {len(app_english_phrases)} English phrases match dictionary keys")

    # Check every Spanish phrase has a back-translation
    missing_es = [p for p in app_spanish_phrases if p not in SPANISH_TO_ENGLISH]
    if missing_es:
        for p in missing_es:
            fail(f"Spanish phrase in app.py missing from SPANISH_TO_ENGLISH: '{p}'")
            all_passed = False
    else:
        ok(f"All {len(app_spanish_phrases)} Spanish phrases have back-translations")

    # Verify EN→ES→EN round-trip consistency for all phrases
    from regional_medical_spanish import get_english_back_translation, get_regional_translation
    inconsistent = []
    for en_phrase in app_english_phrases:
        es_translation, _ = get_regional_translation(en_phrase, "neutral")
        if es_translation:
            back = get_english_back_translation(es_translation)
            if back != en_phrase:
                inconsistent.append((en_phrase, es_translation, back))

    if inconsistent:
        for en, es, back in inconsistent:
            fail(f"Inconsistent: '{en}' → '{es}' → '{back}'")
            all_passed = False
    else:
        ok(f"All EN→ES→EN round-trips consistent")

    return all_passed

# ── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{BOLD}{'='*56}")
    print("  Medical Voice Translator — System Test Suite")
    print(f"{'='*56}{RESET}")
    print(f"  App directory: {APP_DIR}")
    print(f"  Python: {sys.version.split()[0]}")

    test("Dictionary import",                    test_dictionary_import)
    test("All phrase categories present",         test_phrase_categories)
    test("Critical regional variants",            test_critical_regional_variants)
    test("All six regions",                       test_all_regions)
    test("Fuzzy matching",                        test_fuzzy_matching)
    test("Fuzzy regional translation end-to-end", test_fuzzy_regional_translation)
    test("Piper TTS audio generation",            test_piper_tts)
    test("Argos translation EN↔ES",               test_argos_translation)
    test("Whisper model",                         test_whisper)
    test("Feature flags in app.py",               test_feature_flags)
    test("App file integrity",                    test_app_file_integrity)
    test("Required model files",                  test_model_files)
    test("No leftover test files",                test_no_test_files)
    test("packages.txt exists with espeak-ng",    test_packages_txt)
    test("Phrase consistency app↔dictionary",     test_phrase_consistency)

    print(f"\n{BOLD}{'='*56}")
    if failed == 0:
        print(f"{GREEN}  RESULTS: {passed}/{total} tests passed")
        print(f"  ✅ App is ready for deployment{RESET}{BOLD}")
    else:
        print(f"{RED}  RESULTS: {passed}/{total} passed — {failed} FAILED")
        print(f"  ❌ Do NOT deploy until all tests pass{RESET}{BOLD}")
    print(f"{'='*56}{RESET}\n")

    sys.exit(0 if failed == 0 else 1)
