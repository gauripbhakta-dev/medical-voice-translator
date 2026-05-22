# =============================================================================
# Medical Voice Translator — Regional Spanish Variant Dictionary
# =============================================================================
# Purpose: Override neutral Google Translate output with clinically accurate
#          regional Spanish variants for specific patient communities.
#
# How it works:
#   1. Google Translate provides the default neutral Latin American Spanish
#   2. This dictionary overrides specific terms where regional variation
#      is clinically meaningful
#   3. If a term has no regional override, the Google Translate output is used
#
# Regions covered:
#   - neutral:      Standard Latin American Spanish (Google Translate default)
#   - dominican:    Dominican Republic (largest LEP population in Lawrence MA)
#   - puerto_rican: Puerto Rico
#   - mexican:      Mexico (largest Spanish-speaking group in US overall)
#   - colombian:    Colombia and South America broadly
#   - cuban:        Cuba
#
# Status: DRAFT — requires review by clinical experts
#         clinical expert review
#
# Last updated: April 2026
# Author: Gauri Bhakta, Phillips Academy Andover
# =============================================================================

REGIONAL_VARIANTS = {

    # =========================================================================
    # CATEGORY 1: PAIN ASSESSMENT
    # =========================================================================

    "Where does it hurt?": {
        "neutral":      "¿Dónde le duele?",
        "dominican":    "¿Dónde le duele?",
        "puerto_rican": "¿Dónde le duele?",
        "mexican":      "¿Dónde le duele?",
        "colombian":    "¿Dónde le duele?",
        "cuban":        "¿Dónde le duele?",
        "notes": "Universally consistent across all regions"
    },

    "Rate your pain from 1 to 10": {
        "neutral":      "Califique su dolor del 1 al 10",
        "dominican":    "Dígame cuánto le duele del 1 al 10",
        "puerto_rican": "¿Cuánto le duele del 1 al 10?",
        "mexican":      "Del 1 al 10, ¿cuánto le duele?",
        "colombian":    "Califique su dolor del 1 al 10",
        "cuban":        "Del 1 al 10, ¿qué tanto le duele?",
        "notes": "Minor phrasing variation — all mean the same thing clinically"
    },

    "Is the pain sharp or dull?": {
        "neutral":      "¿El dolor es agudo o sordo?",
        "dominican":    "¿El dolor es fuerte o suave?",
        "puerto_rican": "¿El dolor es punzante o leve?",
        "mexican":      "¿El dolor es agudo o leve?",
        "colombian":    "¿El dolor es agudo o sordo?",
        "cuban":        "¿El dolor es fuerte o suave?",
        "notes": "'Sordo' for dull pain is more academic — Dominican and Cuban patients may respond better to 'suave' or 'leve'"
    },

    "Is the pain constant or does it come and go?": {
        "neutral":      "¿El dolor es constante o va y viene?",
        "dominican":    "¿El dolor está siempre ahí o va y viene?",
        "puerto_rican": "¿El dolor es continuo o va y viene?",
        "mexican":      "¿El dolor es seguido o va y viene?",
        "colombian":    "¿El dolor es constante o va y viene?",
        "cuban":        "¿El dolor es constante o va y viene?",
        "notes": "'Seguido' used informally in Mexico for continuous. Dominican patients understand 'siempre ahí' better than 'constante'"
    },

    "Does the pain go anywhere else?": {
        "neutral":      "¿El dolor se va a algún otro lugar?",
        "dominican":    "¿El dolor corre para algún otro lado?",
        "puerto_rican": "¿El dolor se corre para otro lado?",
        "mexican":      "¿El dolor se va a otro lado?",
        "colombian":    "¿El dolor irradia a otra parte?",
        "cuban":        "¿El dolor se va para algún otro lugar?",
        "notes": "'Irradia' is the clinical term but most patients understand 'se corre' or 'se va' better"
    },

    "Does anything make the pain better?": {
        "neutral":      "¿Hay algo que mejore el dolor?",
        "dominican":    "¿Hay algo que le quite el dolor?",
        "puerto_rican": "¿Algo le quita el dolor?",
        "mexican":      "¿Hay algo que le alivie el dolor?",
        "colombian":    "¿Algo alivia el dolor?",
        "cuban":        "¿Algo le quita el dolor?",
        "notes": "'Quitar' is more colloquial and widely understood than 'mejorar' in this context"
    },

    "Does anything make the pain worse?": {
        "neutral":      "¿Hay algo que empeore el dolor?",
        "dominican":    "¿Hay algo que le ponga el dolor peor?",
        "puerto_rican": "¿Algo le empeora el dolor?",
        "mexican":      "¿Hay algo que le aumente el dolor?",
        "colombian":    "¿Algo empeora el dolor?",
        "cuban":        "¿Hay algo que le aumente el dolor?",
        "notes": "Minor variation — all mutually comprehensible"
    },

    # =========================================================================
    # CATEGORY 2: VITAL SIGNS AND SYMPTOMS
    # =========================================================================

    "Do you have a fever?": {
        "neutral":      "¿Tiene fiebre?",
        "dominican":    "¿Tiene calentura?",
        "puerto_rican": "¿Tiene fiebre?",
        "mexican":      "¿Tiene fiebre o calentura?",
        "colombian":    "¿Tiene fiebre?",
        "cuban":        "¿Tiene fiebre?",
        "notes": "CLINICALLY IMPORTANT: Dominican patients often say 'calentura' for fever, not 'fiebre'. Mexican patients may use both."
    },

    "Are you short of breath?": {
        "neutral":      "¿Tiene dificultad para respirar?",
        "dominican":    "¿Le falta el aire?",
        "puerto_rican": "¿Le falta el aire?",
        "mexican":      "¿Le falta el aire?",
        "colombian":    "¿Tiene dificultad para respirar?",
        "cuban":        "¿Le falta el aire?",
        "notes": "'Le falta el aire' is the most universally understood across all regions. Preferred over clinical 'dificultad para respirar'"
    },

    "Are you dizzy?": {
        "neutral":      "¿Tiene mareos?",
        "dominican":    "¿Está mareado/mareada?",
        "puerto_rican": "¿Está mareado/mareada?",
        "mexican":      "¿Está mareado/mareada?",
        "colombian":    "¿Tiene mareos?",
        "cuban":        "¿Está mareado/mareada?",
        "notes": "Consistent across regions — 'mareo' universally understood"
    },

    "Are you nauseous?": {
        "neutral":      "¿Tiene náuseas?",
        "dominican":    "¿Tiene ganas de vomitar?",
        "puerto_rican": "¿Tiene náuseas?",
        "mexican":      "¿Tiene asco o náuseas?",
        "colombian":    "¿Tiene náuseas?",
        "cuban":        "¿Tiene náuseas?",
        "notes": "CLINICALLY IMPORTANT: Dominican patients may not recognize 'náuseas' — 'ganas de vomitar' is more reliable. Mexican: 'asco' is colloquial for nausea."
    },

    "Have you vomited?": {
        "neutral":      "¿Ha vomitado?",
        "dominican":    "¿Ha vomitado?",
        "puerto_rican": "¿Ha vomitado?",
        "mexican":      "¿Ha vomitado?",
        "colombian":    "¿Ha vomitado?",
        "cuban":        "¿Ha vomitado?",
        "notes": "Universally consistent"
    },

    "Do you have a headache?": {
        "neutral":      "¿Tiene dolor de cabeza?",
        "dominican":    "¿Le duele la cabeza?",
        "puerto_rican": "¿Tiene dolor de cabeza?",
        "mexican":      "¿Tiene dolor de cabeza?",
        "colombian":    "¿Tiene dolor de cabeza?",
        "cuban":        "¿Le duele la cabeza?",
        "notes": "Both phrasings widely understood. 'Jaqueca' or 'migraña' may be used for migraine specifically."
    },

    "Do you have chest pain?": {
        "neutral":      "¿Tiene dolor en el pecho?",
        "dominican":    "¿Le duele el pecho?",
        "puerto_rican": "¿Le duele el pecho?",
        "mexican":      "¿Tiene dolor en el pecho?",
        "colombian":    "¿Tiene dolor en el pecho?",
        "cuban":        "¿Le duele el pecho?",
        "notes": "Consistent — both phrasings understood everywhere"
    },

    "Do you have abdominal pain?": {
        "neutral":      "¿Tiene dolor abdominal?",
        "dominican":    "¿Le duele la barriga?",
        "puerto_rican": "¿Le duele el estómago?",
        "mexican":      "¿Le duele el estómago?",
        "colombian":    "¿Tiene dolor en el abdomen?",
        "cuban":        "¿Le duele el estómago?",
        "notes": "IMPORTANT: 'Abdominal' is not commonly used colloquially. 'Barriga' (Dominican), 'estómago' (PR/MX) are more natural. Colombian patients may understand 'abdomen'."
    },

    "Are you having trouble urinating?": {
        "neutral":      "¿Tiene problemas para orinar?",
        "dominican":    "¿Tiene problemas para hacer pipí?",
        "puerto_rican": "¿Tiene problemas para orinar?",
        "mexican":      "¿Tiene problemas para orinar?",
        "colombian":    "¿Tiene dificultad para orinar?",
        "cuban":        "¿Tiene problemas para orinar?",
        "notes": "Dominican patients may use 'hacer pipí' or 'hacer del uno'. 'Orinar' is universally understood as the clinical term."
    },

    # =========================================================================
    # CATEGORY 3: MEDICAL HISTORY
    # =========================================================================

    "Do you have any allergies?": {
        "neutral":      "¿Tiene alguna alergia?",
        "dominican":    "¿Es alérgico/alérgica a algo?",
        "puerto_rican": "¿Tiene alguna alergia?",
        "mexican":      "¿Tiene alguna alergia?",
        "colombian":    "¿Tiene alguna alergia?",
        "cuban":        "¿Tiene alguna alergia?",
        "notes": "Consistent — 'alergia' universally understood"
    },

    "Are you taking any medications?": {
        "neutral":      "¿Está tomando algún medicamento?",
        "dominican":    "¿Está tomando alguna medicina?",
        "puerto_rican": "¿Está tomando alguna medicina?",
        "mexican":      "¿Está tomando medicamentos?",
        "colombian":    "¿Está tomando algún medicamento?",
        "cuban":        "¿Está tomando alguna medicina?",
        "notes": "'Medicina' is more colloquial than 'medicamento' in Caribbean Spanish. Both understood everywhere."
    },

    "Do you have diabetes?": {
        "neutral":      "¿Tiene diabetes?",
        "dominican":    "¿Tiene azúcar?",
        "puerto_rican": "¿Tiene azúcar?",
        "mexican":      "¿Tiene diabetes?",
        "colombian":    "¿Tiene diabetes?",
        "cuban":        "¿Tiene azúcar?",
        "notes": "CLINICALLY IMPORTANT: Caribbean patients (Dominican, PR, Cuban) commonly refer to diabetes as 'azúcar' — not 'diabetes'. A patient may say 'no' to diabetes but 'sí' to azúcar."
    },

    "Do you have high blood pressure?": {
        "neutral":      "¿Tiene presión alta?",
        "dominican":    "¿Tiene la presión alta?",
        "puerto_rican": "¿Tiene la presión alta?",
        "mexican":      "¿Tiene presión alta?",
        "colombian":    "¿Tiene la tensión alta?",
        "cuban":        "¿Tiene la presión alta?",
        "notes": "IMPORTANT: Colombian patients may say 'tensión' instead of 'presión'. Both mean blood pressure but a patient may not recognize the other term."
    },

    "Do you have heart problems?": {
        "neutral":      "¿Tiene problemas del corazón?",
        "dominican":    "¿Tiene problemas del corazón?",
        "puerto_rican": "¿Tiene problemas del corazón?",
        "mexican":      "¿Tiene problemas del corazón?",
        "colombian":    "¿Tiene problemas cardíacos?",
        "cuban":        "¿Tiene problemas del corazón?",
        "notes": "Consistent — 'corazón' universally understood"
    },

    "Have you had surgery before?": {
        "neutral":      "¿Ha tenido cirugías antes?",
        "dominican":    "¿Lo/La han operado antes?",
        "puerto_rican": "¿Lo/La han operado antes?",
        "mexican":      "¿Lo/La han operado antes?",
        "colombian":    "¿Ha tenido cirugías anteriormente?",
        "cuban":        "¿Lo/La han operado antes?",
        "notes": "'Operado' is more colloquial and better understood than 'cirugía' across most regions"
    },

    "Are you pregnant?": {
        "neutral":      "¿Está embarazada?",
        "dominican":    "¿Está embarazada?",
        "puerto_rican": "¿Está embarazada?",
        "mexican":      "¿Está embarazada?",
        "colombian":    "¿Está embarazada?",
        "cuban":        "¿Está embarazada?",
        "notes": "Universally consistent. Some Mexican patients may say 'encinta' but 'embarazada' is always understood."
    },

    "When was your last menstrual period?": {
        "neutral":      "¿Cuándo fue su última menstruación?",
        "dominican":    "¿Cuándo le vino el período?",
        "puerto_rican": "¿Cuándo le bajó?",
        "mexican":      "¿Cuándo fue su última regla?",
        "colombian":    "¿Cuándo fue su última menstruación?",
        "cuban":        "¿Cuándo fue su última regla?",
        "notes": "CLINICALLY IMPORTANT: Significant regional variation. Dominican: 'venir el período'. Puerto Rican: 'bajar'. Mexican: 'regla'. Colombian: 'menstruación'. Ask the question in the patient's regional term for clarity."
    },

    # =========================================================================
    # CATEGORY 4: CONSENT AND PROCEDURES
    # =========================================================================

    "I need to examine you": {
        "neutral":      "Necesito examinarle",
        "dominican":    "Le voy a revisar",
        "puerto_rican": "Le voy a examinar",
        "mexican":      "Le voy a revisar",
        "colombian":    "Necesito examinarlo/examinarla",
        "cuban":        "Le voy a examinar",
        "notes": "'Revisar' is more colloquial and widely understood than 'examinar' in Caribbean and Mexican Spanish"
    },

    "I need to draw blood": {
        "neutral":      "Necesito sacarle sangre",
        "dominican":    "Le voy a sacar sangre",
        "puerto_rican": "Le voy a sacar sangre",
        "mexican":      "Le voy a tomar una muestra de sangre",
        "colombian":    "Necesito tomarle una muestra de sangre",
        "cuban":        "Le voy a sacar sangre",
        "notes": "Minor variation — all understood. 'Sacar' is more direct and commonly used in Caribbean Spanish."
    },

    "I need to start an IV": {
        "neutral":      "Necesito ponerle un suero",
        "dominican":    "Le voy a poner una aguja en la vena",
        "puerto_rican": "Le voy a poner un suero",
        "mexican":      "Le voy a poner un catéter intravenoso",
        "colombian":    "Le voy a poner un suero",
        "cuban":        "Le voy a poner una vena",
        "notes": "IMPORTANT: 'Suero' widely understood for IV drip. 'Poner una vena' is Cuban slang for starting an IV line. Dominican patients may need 'aguja en la vena' to understand."
    },

    "Do you understand?": {
        "neutral":      "¿Entiende?",
        "dominican":    "¿Entiende?",
        "puerto_rican": "¿Entiende?",
        "mexican":      "¿Entiende?",
        "colombian":    "¿Comprende?",
        "cuban":        "¿Entiende?",
        "notes": "Consistent — both 'entiende' and 'comprende' universally understood"
    },

    "Please sign here": {
        "neutral":      "Por favor firme aquí",
        "dominican":    "Por favor ponga su firma aquí",
        "puerto_rican": "Por favor firme aquí",
        "mexican":      "Por favor firme aquí",
        "colombian":    "Por favor firme aquí",
        "cuban":        "Por favor firme aquí",
        "notes": "Consistent"
    },

    # =========================================================================
    # CATEGORY 5: INSTRUCTIONS AND REQUESTS
    # =========================================================================

    "Please lie down": {
        "neutral":      "Por favor acuéstese",
        "dominican":    "Por favor échese",
        "puerto_rican": "Por favor acuéstese",
        "mexican":      "Por favor recuéstese",
        "colombian":    "Por favor acuéstese",
        "cuban":        "Por favor échese",
        "notes": "IMPORTANT: Dominican and Cuban patients commonly use 'echarse'. Mexican patients may prefer 'recostarse'."
    },

    "Please sit up": {
        "neutral":      "Por favor siéntese",
        "dominican":    "Por favor siéntese",
        "puerto_rican": "Por favor siéntese",
        "mexican":      "Por favor siéntese",
        "colombian":    "Por favor siéntese",
        "cuban":        "Por favor siéntese",
        "notes": "Universally consistent"
    },

    "Please breathe deeply": {
        "neutral":      "Por favor respire profundo",
        "dominican":    "Por favor respire hondo",
        "puerto_rican": "Por favor respire hondo",
        "mexican":      "Por favor respire profundo",
        "colombian":    "Por favor respire profundo",
        "cuban":        "Por favor respire hondo",
        "notes": "'Hondo' and 'profundo' both mean deeply — Caribbean patients more commonly say 'hondo'"
    },

    "Do not eat or drink anything": {
        "neutral":      "No coma ni beba nada",
        "dominican":    "No coma ni tome nada",
        "puerto_rican": "No coma ni tome nada",
        "mexican":      "No coma ni beba nada",
        "colombian":    "No coma ni beba nada",
        "cuban":        "No coma ni tome nada",
        "notes": "IMPORTANT: Caribbean patients use 'tomar' for drinking liquids, not 'beber'. 'Beber' sounds formal in Dominican and Puerto Rican Spanish."
    },

    "I need a urine sample": {
        "neutral":      "Necesito una muestra de orina",
        "dominican":    "Necesito que haga del uno en este vasito",
        "puerto_rican": "Necesito una muestra de orina",
        "mexican":      "Necesito una muestra de orina",
        "colombian":    "Necesito una muestra de orina",
        "cuban":        "Necesito una muestra de orina",
        "notes": "Dominican patients may respond better to 'hacer del uno' — highly colloquial but widely understood in Dominican communities"
    },

    "The doctor will see you soon": {
        "neutral":      "El médico le atenderá pronto",
        "dominican":    "El doctor viene ahora mismo",
        "puerto_rican": "El doctor viene enseguida",
        "mexican":      "El doctor lo/la atiende pronto",
        "colombian":    "El médico lo/la atenderá pronto",
        "cuban":        "El médico viene enseguida",
        "notes": "Caribbean patients say 'ahora mismo' or 'enseguida' for soon. Colombian patients use 'médico' more formally than 'doctor'."
    },

    # =========================================================================
    # CATEGORY 6: DISCHARGE AND FOLLOW-UP
    # =========================================================================

    "You can go home now": {
        "neutral":      "Ya puede irse a casa",
        "dominican":    "Ya se puede ir para su casa",
        "puerto_rican": "Ya puede irse a la casa",
        "mexican":      "Ya se puede ir a su casa",
        "colombian":    "Ya puede regresar a casa",
        "cuban":        "Ya puede irse para la casa",
        "notes": "Minor variation — all mean the same thing"
    },

    "Take this medication twice a day": {
        "neutral":      "Tome este medicamento dos veces al día",
        "dominican":    "Tome esta medicina dos veces al día",
        "puerto_rican": "Tome esta medicina dos veces al día",
        "mexican":      "Tome este medicamento dos veces al día",
        "colombian":    "Tome este medicamento dos veces al día",
        "cuban":        "Tome esta medicina dos veces al día",
        "notes": "Caribbean patients use 'medicina' — see medication note above"
    },

    "Come back if symptoms worsen": {
        "neutral":      "Regrese si los síntomas empeoran",
        "dominican":    "Si se pone peor, vuelva",
        "puerto_rican": "Si se pone peor, vuelva",
        "mexican":      "Regrese si los síntomas empeoran",
        "colombian":    "Regrese si los síntomas empeoran",
        "cuban":        "Si se pone peor, vuelva",
        "notes": "Caribbean patients respond better to direct 'si se pone peor'. 'Síntomas' may not be understood by all patients — simplify when possible."
    },

    "Follow up with your doctor in one week": {
        "neutral":      "Haga cita con su médico en una semana",
        "dominican":    "Busque su doctor en una semana",
        "puerto_rican": "Vea a su doctor en una semana",
        "mexican":      "Siga con su médico en una semana",
        "colombian":    "Consulte con su médico en una semana",
        "cuban":        "Vea a su médico en una semana",
        "notes": "Significant variation in how patients describe 'making an appointment'. 'Buscar el doctor' is Dominican. 'Ver al doctor' is PR/Cuban."
    },

    "Call 911 if you have an emergency": {
        "neutral":      "Llame al 911 si tiene una emergencia",
        "dominican":    "Llame al 911 si tiene una emergencia",
        "puerto_rican": "Llame al 911 si tiene una emergencia",
        "mexican":      "Llame al 911 si tiene una emergencia",
        "colombian":    "Llame al 911 si tiene una emergencia",
        "cuban":        "Llame al 911 si tiene una emergencia",
        "notes": "Universally consistent — 911 is the same across all US regions"
    },
}

# =============================================================================
# CRITICAL CLINICAL NOTES — Review with clinical experts
# =============================================================================
REVIEW_NOTES = """
HIGHEST PRIORITY TERMS FOR CLINICAL REVIEW:

1. DIABETES — 'azúcar' vs 'diabetes'
   Caribbean patients (Dominican, PR, Cuban) often refer to diabetes as 'azúcar'.
   A patient may deny having 'diabetes' but confirm having 'azúcar'.
   RECOMMENDATION: Ask both — '¿Tiene diabetes o azúcar?'

2. NAUSEA — 'náuseas' vs 'ganas de vomitar'
   Dominican patients may not recognize 'náuseas'.
   RECOMMENDATION: Use 'ganas de vomitar' for Dominican patients.

3. FEVER — 'fiebre' vs 'calentura'
   Dominican patients commonly say 'calentura' not 'fiebre'.
   RECOMMENDATION: Use both — '¿Tiene fiebre o calentura?'

4. BLOOD PRESSURE — 'presión' vs 'tensión'
   Colombian patients say 'tensión arterial' not 'presión arterial'.
   RECOMMENDATION: Use 'presión' for most patients, 'tensión' if Colombian.

5. MENSTRUAL PERIOD — major regional variation
   Dominican: 'el período' / 'me vino'
   Puerto Rican: 'me bajó'
   Mexican: 'la regla'
   Colombian: 'la menstruación'
   RECOMMENDATION: This phrase needs most careful regional attention.

6. IV LINE — significant variation
   Cuban: 'poner una vena'
   Dominican: 'aguja en la vena'
   PR/MX: 'suero'
   RECOMMENDATION: Show the equipment while speaking for all regions.

7. DRINKING — 'beber' vs 'tomar'
   Caribbean patients use 'tomar' for drinking liquids.
   'No beba nada' may confuse Dominican/PR patients who associate 'beber' with alcohol only.
   RECOMMENDATION: Always use 'no tome nada' for NPO instructions.
"""

# =============================================================================
# FUNCTION: Get regional translation
# =============================================================================
def get_regional_translation(phrase_key, region="neutral"):
    """
    Returns the regional variant of a phrase.
    Falls back to neutral if region or phrase not found.

    Args:
        phrase_key: The English phrase key
        region: One of 'neutral', 'dominican', 'puerto_rican',
                'mexican', 'colombian', 'cuban'

    Returns:
        tuple: (regional_translation, notes)
    """
    if phrase_key not in REGIONAL_VARIANTS:
        return None, "Phrase not in regional dictionary — use Google Translate output"

    phrase_data = REGIONAL_VARIANTS[phrase_key]
    translation = phrase_data.get(region, phrase_data.get("neutral"))
    notes = phrase_data.get("notes", "")

    return translation, notes


# =============================================================================
# FUNCTION: Get all variants for a phrase (for review/display)
# =============================================================================
def get_all_variants(phrase_key):
    """Returns all regional variants for a phrase."""
    if phrase_key not in REGIONAL_VARIANTS:
        return None
    return REGIONAL_VARIANTS[phrase_key]


# =============================================================================
# FUNCTION: List all phrases by category (placeholder — expand after
# Diana's feedback defines the six categories)
# =============================================================================
CATEGORY_MAP = {
    "Pain Assessment":      ["Where does it hurt?", "Rate your pain from 1 to 10",
                             "Is the pain sharp or dull?",
                             "Is the pain constant or does it come and go?",
                             "Does the pain go anywhere else?",
                             "Does anything make the pain better?",
                             "Does anything make the pain worse?"],
    "Vital Signs":          ["Do you have a fever?", "Are you short of breath?",
                             "Are you dizzy?", "Are you nauseous?",
                             "Have you vomited?", "Do you have a headache?",
                             "Do you have chest pain?", "Do you have abdominal pain?",
                             "Are you having trouble urinating?"],
    "Medical History":      ["Do you have any allergies?",
                             "Are you taking any medications?",
                             "Do you have diabetes?",
                             "Do you have high blood pressure?",
                             "Do you have heart problems?",
                             "Have you had surgery before?",
                             "Are you pregnant?",
                             "When was your last menstrual period?"],
    "Consent & Procedures": ["I need to examine you", "I need to draw blood",
                             "I need to start an IV", "Do you understand?",
                             "Please sign here"],
    "Instructions":         ["Please lie down", "Please sit up",
                             "Please breathe deeply",
                             "Do not eat or drink anything",
                             "I need a urine sample",
                             "The doctor will see you soon"],
    "Discharge":            ["You can go home now",
                             "Take this medication twice a day",
                             "Come back if symptoms worsen",
                             "Follow up with your doctor in one week",
                             "Call 911 if you have an emergency"],
}

if __name__ == "__main__":
    # Quick test — print all variants for a high-priority phrase
    print("=== DIABETES — CRITICAL CLINICAL TERM ===")
    variants = get_all_variants("Do you have diabetes?")
    for region, translation in variants.items():
        if region != "notes":
            print(f"  {region:15}: {translation}")
    print(f"  Notes: {variants['notes']}")
    print()

    print("=== FEVER — CRITICAL CLINICAL TERM ===")
    variants = get_all_variants("Do you have a fever?")
    for region, translation in variants.items():
        if region != "notes":
            print(f"  {region:15}: {translation}")
    print(f"  Notes: {variants['notes']}")
    print()

    print(f"Total phrases in dictionary: {len(REGIONAL_VARIANTS)}")
    print(f"Regions covered: neutral, dominican, puerto_rican, mexican, colombian, cuban")
    print()
    print("STATUS: DRAFT — Requires review by clinical experts")
    print("        clinical expert review")


def normalize(text: str) -> str:
    """
    Normalize text for fuzzy matching.
    Removes punctuation, lowercases, strips whitespace.
    """
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def find_best_match(text: str):
    """
    Find the best matching dictionary key for any input text.
    Handles case insensitive, punctuation differences, fuzzy word overlap.

    Args:
        text: Input English text from voice or keyboard

    Returns:
        Best matching dictionary key, or None if no match found
    """
    normalized_input = normalize(text)

    # 1. Exact match after normalization
    for key in REGIONAL_VARIANTS:
        if normalize(key) == normalized_input:
            return key

    # 2. Fuzzy word overlap matching
    input_words = set(normalized_input.split())
    best_key = None
    best_score = 0.0

    for key in REGIONAL_VARIANTS:
        key_words = set(normalize(key).split())
        if not key_words:
            continue
        intersection = len(input_words & key_words)
        union = len(input_words | key_words)
        score = intersection / union if union > 0 else 0.0
        if score > best_score:
            best_score = score
            best_key = key

    if best_score >= 0.65:
        return best_key

    return None


def get_regional_translation_fuzzy(text: str, region: str = "neutral"):
    """
    Get regional translation using fuzzy matching.
    Use this for voice input and free text — handles case and punctuation.

    Args:
        text:   Any English text — voice transcription or typed
        region: Region key

    Returns:
        tuple: (translation, notes) or (None, "") if no match
    """
    matched_key = find_best_match(text)
    if matched_key:
        return get_regional_translation(matched_key, region)
    return None, "No regional variant found — use Google Translate"
