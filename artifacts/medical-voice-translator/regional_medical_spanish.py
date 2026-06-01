# =============================================================================
# Medical Voice Translator — Regional Spanish Variant Dictionary
# =============================================================================
# Purpose: Provides clinically accurate regional Spanish variants AND
#          correct English back-translations for all preset phrases.
#
# How it works:
#   EN→ES: Returns region-specific Spanish translation
#   ES→EN: Returns correct English back-translation from dictionary
#          (bypasses Argos Translate for all preset phrases)
#
# Regions covered:
#   - neutral:      Standard Latin American Spanish
#   - dominican:    Dominican Republic
#   - puerto_rican: Puerto Rico
#   - mexican:      Mexico
#   - colombian:    Colombia
#   - cuban:        Cuba
#
# Status: DRAFT — requires review by clinical experts
# Last updated: May 2026
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
        "notes": "'Sordo' for dull pain is more academic — Dominican and Cuban patients respond better to 'suave' or 'leve'"
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
        "notes": "'Irradia' is clinical but most patients understand 'se corre' or 'se va' better"
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
        "notes": "CLINICALLY IMPORTANT: Dominican patients often say 'calentura' not 'fiebre'. Mexican patients may use both."
    },

    "Are you short of breath?": {
        "neutral":      "¿Tiene dificultad para respirar?",
        "dominican":    "¿Le falta el aire?",
        "puerto_rican": "¿Le falta el aire?",
        "mexican":      "¿Le falta el aire?",
        "colombian":    "¿Tiene dificultad para respirar?",
        "cuban":        "¿Le falta el aire?",
        "notes": "'Le falta el aire' most universally understood across all regions"
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
        "notes": "CLINICALLY IMPORTANT: Dominican patients may not recognize 'náuseas' — 'ganas de vomitar' is more reliable"
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
        "notes": "Both phrasings widely understood"
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
        "notes": "IMPORTANT: 'Abdominal' not commonly used colloquially. 'Barriga' (Dominican), 'estómago' (PR/MX) more natural"
    },

    "Are you having trouble urinating?": {
        "neutral":      "¿Tiene problemas para orinar?",
        "dominican":    "¿Tiene problemas para hacer pipí?",
        "puerto_rican": "¿Tiene problemas para orinar?",
        "mexican":      "¿Tiene problemas para orinar?",
        "colombian":    "¿Tiene dificultad para orinar?",
        "cuban":        "¿Tiene problemas para orinar?",
        "notes": "Dominican patients may use 'hacer pipí' or 'hacer del uno'"
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
        "notes": "'Medicina' more colloquial than 'medicamento' in Caribbean Spanish"
    },

    "Do you have diabetes?": {
        "neutral":      "¿Tiene diabetes?",
        "dominican":    "¿Tiene azúcar?",
        "puerto_rican": "¿Tiene azúcar?",
        "mexican":      "¿Tiene diabetes?",
        "colombian":    "¿Tiene diabetes?",
        "cuban":        "¿Tiene azúcar?",
        "notes": "CLINICALLY IMPORTANT: Caribbean patients (Dominican, PR, Cuban) commonly refer to diabetes as 'azúcar'"
    },

    "Do you have high blood pressure?": {
        "neutral":      "¿Tiene presión alta?",
        "dominican":    "¿Tiene la presión alta?",
        "puerto_rican": "¿Tiene la presión alta?",
        "mexican":      "¿Tiene presión alta?",
        "colombian":    "¿Tiene la tensión alta?",
        "cuban":        "¿Tiene la presión alta?",
        "notes": "IMPORTANT: Colombian patients may say 'tensión' instead of 'presión'"
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
        "notes": "'Operado' more colloquial and better understood than 'cirugía'"
    },

    "Are you pregnant?": {
        "neutral":      "¿Está embarazada?",
        "dominican":    "¿Está embarazada?",
        "puerto_rican": "¿Está embarazada?",
        "mexican":      "¿Está embarazada?",
        "colombian":    "¿Está embarazada?",
        "cuban":        "¿Está embarazada?",
        "notes": "Universally consistent"
    },

    "When was your last menstrual period?": {
        "neutral":      "¿Cuándo fue su última menstruación?",
        "dominican":    "¿Cuándo le vino el período?",
        "puerto_rican": "¿Cuándo le bajó?",
        "mexican":      "¿Cuándo fue su última regla?",
        "colombian":    "¿Cuándo fue su última menstruación?",
        "cuban":        "¿Cuándo fue su última regla?",
        "notes": "CLINICALLY IMPORTANT: Significant regional variation. Dominican: 'venir el período'. Puerto Rican: 'bajar'. Mexican: 'regla'."
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
        "notes": "'Revisar' more colloquial and widely understood than 'examinar' in Caribbean and Mexican Spanish"
    },

    "I need to draw blood": {
        "neutral":      "Necesito sacarle sangre",
        "dominican":    "Le voy a sacar sangre",
        "puerto_rican": "Le voy a sacar sangre",
        "mexican":      "Le voy a tomar una muestra de sangre",
        "colombian":    "Necesito tomarle una muestra de sangre",
        "cuban":        "Le voy a sacar sangre",
        "notes": "'Sacar' more direct and commonly used in Caribbean Spanish"
    },

    "I need to start an IV": {
        "neutral":      "Necesito ponerle un suero",
        "dominican":    "Le voy a poner una aguja en la vena",
        "puerto_rican": "Le voy a poner un suero",
        "mexican":      "Le voy a poner un catéter intravenoso",
        "colombian":    "Le voy a poner un suero",
        "cuban":        "Le voy a poner una vena",
        "notes": "IMPORTANT: 'Suero' widely understood for IV. 'Poner una vena' is Cuban slang for starting an IV line"
    },

    "Do you understand?": {
        "neutral":      "¿Entiende?",
        "dominican":    "¿Entiende?",
        "puerto_rican": "¿Entiende?",
        "mexican":      "¿Entiende?",
        "colombian":    "¿Comprende?",
        "cuban":        "¿Entiende?",
        "notes": "Both 'entiende' and 'comprende' universally understood"
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
        "notes": "IMPORTANT: Dominican and Cuban patients commonly use 'echarse'. Mexican patients prefer 'recostarse'."
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
        "notes": "IMPORTANT: Caribbean patients use 'tomar' for drinking liquids, not 'beber'"
    },

    "I need a urine sample": {
        "neutral":      "Necesito una muestra de orina",
        "dominican":    "Necesito que haga del uno en este vasito",
        "puerto_rican": "Necesito una muestra de orina",
        "mexican":      "Necesito una muestra de orina",
        "colombian":    "Necesito una muestra de orina",
        "cuban":        "Necesito una muestra de orina",
        "notes": "Dominican patients respond better to 'hacer del uno'"
    },

    "The doctor will see you soon": {
        "neutral":      "El médico le atenderá pronto",
        "dominican":    "El doctor viene ahora mismo",
        "puerto_rican": "El doctor viene enseguida",
        "mexican":      "El doctor lo/la atiende pronto",
        "colombian":    "El médico lo/la atenderá pronto",
        "cuban":        "El médico viene enseguida",
        "notes": "Caribbean patients say 'ahora mismo' or 'enseguida' for soon"
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
        "notes": "Caribbean patients use 'medicina'"
    },

    "Come back if symptoms worsen": {
        "neutral":      "Regrese si los síntomas empeoran",
        "dominican":    "Si se pone peor, vuelva",
        "puerto_rican": "Si se pone peor, vuelva",
        "mexican":      "Regrese si los síntomas empeoran",
        "colombian":    "Regrese si los síntomas empeoran",
        "cuban":        "Si se pone peor, vuelva",
        "notes": "Caribbean patients respond better to direct 'si se pone peor'"
    },

    "Follow up with your doctor in one week": {
        "neutral":      "Haga cita con su médico en una semana",
        "dominican":    "Busque su doctor en una semana",
        "puerto_rican": "Vea a su doctor en una semana",
        "mexican":      "Siga con su médico en una semana",
        "colombian":    "Consulte con su médico en una semana",
        "cuban":        "Vea a su médico en una semana",
        "notes": "Significant variation in how patients describe making an appointment"
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
# SPANISH → ENGLISH REVERSE DICTIONARY
# Maps every Spanish preset phrase to its correct English translation.
# This bypasses Argos Translate for preset phrases in Spanish→English mode,
# ensuring accurate clinical back-translation regardless of pronoun ambiguity.
# =============================================================================

SPANISH_TO_ENGLISH = {
    # Pain Assessment
    "¿Dónde le duele?":                        "Where does it hurt?",
    "Califique su dolor del 1 al 10":           "Rate your pain from 1 to 10",
    "Dígame cuánto le duele del 1 al 10":       "Rate your pain from 1 to 10",
    "¿Cuánto le duele del 1 al 10?":            "Rate your pain from 1 to 10",
    "Del 1 al 10, ¿cuánto le duele?":           "Rate your pain from 1 to 10",
    "Del 1 al 10, ¿qué tanto le duele?":        "Rate your pain from 1 to 10",
    "¿El dolor es agudo o sordo?":              "Is the pain sharp or dull?",
    "¿El dolor es fuerte o suave?":             "Is the pain sharp or dull?",
    "¿El dolor es punzante o leve?":            "Is the pain sharp or dull?",
    "¿El dolor es agudo o leve?":               "Is the pain sharp or dull?",
    "¿El dolor es constante o va y viene?":     "Is the pain constant or does it come and go?",
    "¿El dolor está siempre ahí o va y viene?": "Is the pain constant or does it come and go?",
    "¿El dolor es continuo o va y viene?":      "Is the pain constant or does it come and go?",
    "¿El dolor es seguido o va y viene?":       "Is the pain constant or does it come and go?",
    "¿El dolor se va a algún otro lugar?":      "Does the pain go anywhere else?",
    "¿El dolor corre para algún otro lado?":    "Does the pain go anywhere else?",
    "¿El dolor se corre para otro lado?":       "Does the pain go anywhere else?",
    "¿El dolor se va a otro lado?":             "Does the pain go anywhere else?",
    "¿El dolor irradia a otra parte?":          "Does the pain go anywhere else?",
    "¿El dolor se va para algún otro lugar?":   "Does the pain go anywhere else?",
    "¿Hay algo que mejore el dolor?":           "Does anything make the pain better?",
    "¿Hay algo que le quite el dolor?":         "Does anything make the pain better?",
    "¿Algo le quita el dolor?":                 "Does anything make the pain better?",
    "¿Hay algo que le alivie el dolor?":        "Does anything make the pain better?",
    "¿Algo alivia el dolor?":                   "Does anything make the pain better?",
    "¿Hay algo que empeore el dolor?":          "Does anything make the pain worse?",
    "¿Hay algo que le ponga el dolor peor?":    "Does anything make the pain worse?",
    "¿Algo le empeora el dolor?":               "Does anything make the pain worse?",
    "¿Hay algo que le aumente el dolor?":       "Does anything make the pain worse?",
    "¿Algo empeora el dolor?":                  "Does anything make the pain worse?",

    # Symptoms
    "¿Tiene fiebre?":                           "Do you have a fever?",
    "¿Tiene calentura?":                        "Do you have a fever?",
    "¿Tiene fiebre o calentura?":               "Do you have a fever?",
    "¿Tiene dificultad para respirar?":         "Are you short of breath?",
    "¿Le falta el aire?":                       "Are you short of breath?",
    "¿Tiene mareos?":                           "Are you dizzy?",
    "¿Está mareado/mareada?":                   "Are you dizzy?",
    "¿Tiene náuseas?":                          "Are you nauseous?",
    "¿Tiene ganas de vomitar?":                 "Are you nauseous?",
    "¿Tiene asco o náuseas?":                   "Are you nauseous?",
    "¿Ha vomitado?":                            "Have you vomited?",
    "¿Tiene dolor de cabeza?":                  "Do you have a headache?",
    "¿Le duele la cabeza?":                     "Do you have a headache?",
    "¿Tiene dolor en el pecho?":                "Do you have chest pain?",
    "¿Le duele el pecho?":                      "Do you have chest pain?",
    "¿Tiene dolor abdominal?":                  "Do you have abdominal pain?",
    "¿Le duele la barriga?":                    "Do you have abdominal pain?",
    "¿Le duele el estómago?":                   "Do you have abdominal pain?",
    "¿Tiene dolor en el abdomen?":              "Do you have abdominal pain?",
    "¿Tiene problemas para orinar?":            "Are you having trouble urinating?",
    "¿Tiene problemas para hacer pipí?":        "Are you having trouble urinating?",
    "¿Tiene dificultad para orinar?":           "Are you having trouble urinating?",

    # Medical History
    "¿Tiene alguna alergia?":                   "Do you have any allergies?",
    "¿Es alérgico/alérgica a algo?":            "Do you have any allergies?",
    "¿Está tomando algún medicamento?":         "Are you taking any medications?",
    "¿Está tomando alguna medicina?":           "Are you taking any medications?",
    "¿Está tomando medicamentos?":              "Are you taking any medications?",
    "¿Tiene diabetes?":                         "Do you have diabetes?",
    "¿Tiene azúcar?":                           "Do you have diabetes?",
    "¿Tiene presión alta?":                     "Do you have high blood pressure?",
    "¿Tiene la presión alta?":                  "Do you have high blood pressure?",
    "¿Tiene la tensión alta?":                  "Do you have high blood pressure?",
    "¿Tiene problemas del corazón?":            "Do you have heart problems?",
    "¿Tiene problemas cardíacos?":              "Do you have heart problems?",
    "¿Ha tenido cirugías antes?":               "Have you had surgery before?",
    "¿Lo/La han operado antes?":                "Have you had surgery before?",
    "¿Ha tenido cirugías anteriormente?":       "Have you had surgery before?",
    "¿Está embarazada?":                        "Are you pregnant?",
    "¿Cuándo fue su última menstruación?":      "When was your last menstrual period?",
    "¿Cuándo le vino el período?":              "When was your last menstrual period?",
    "¿Cuándo le bajó?":                         "When was your last menstrual period?",
    "¿Cuándo fue su última regla?":             "When was your last menstrual period?",

    # Consent and Procedures
    "Necesito examinarle":                      "I need to examine you",
    "Le voy a revisar":                         "I need to examine you",
    "Le voy a examinar":                        "I need to examine you",
    "Necesito examinarlo/examinarla":           "I need to examine you",
    "Necesito sacarle sangre":                  "I need to draw blood",
    "Le voy a sacar sangre":                    "I need to draw blood",
    "Le voy a tomar una muestra de sangre":     "I need to draw blood",
    "Necesito tomarle una muestra de sangre":   "I need to draw blood",
    "Necesito ponerle un suero":                "I need to start an IV",
    "Le voy a poner una aguja en la vena":      "I need to start an IV",
    "Le voy a poner un suero":                  "I need to start an IV",
    "Le voy a poner un catéter intravenoso":    "I need to start an IV",
    "Le voy a poner una vena":                  "I need to start an IV",
    "¿Entiende?":                               "Do you understand?",
    "¿Comprende?":                              "Do you understand?",
    "Por favor firme aquí":                     "Please sign here",
    "Por favor ponga su firma aquí":            "Please sign here",

    # Instructions
    "Por favor acuéstese":                      "Please lie down",
    "Por favor échese":                         "Please lie down",
    "Por favor recuéstese":                     "Please lie down",
    "Por favor siéntese":                       "Please sit up",
    "Por favor respire profundo":               "Please breathe deeply",
    "Por favor respire hondo":                  "Please breathe deeply",
    "No coma ni beba nada":                     "Do not eat or drink anything",
    "No coma ni tome nada":                     "Do not eat or drink anything",
    "Necesito una muestra de orina":            "I need a urine sample",
    "Necesito que haga del uno en este vasito": "I need a urine sample",
    "El médico le atenderá pronto":             "The doctor will see you soon",
    "El doctor viene ahora mismo":              "The doctor will see you soon",
    "El doctor viene enseguida":                "The doctor will see you soon",
    "El doctor lo/la atiende pronto":           "The doctor will see you soon",
    "El médico lo/la atenderá pronto":          "The doctor will see you soon",
    "El médico viene enseguida":                "The doctor will see you soon",

    # Discharge
    "Ya puede irse a casa":                     "You can go home now",
    "Ya se puede ir para su casa":              "You can go home now",
    "Ya puede irse a la casa":                  "You can go home now",
    "Ya se puede ir a su casa":                 "You can go home now",
    "Ya puede regresar a casa":                 "You can go home now",
    "Ya puede irse para la casa":               "You can go home now",
    "Tome este medicamento dos veces al día":   "Take this medication twice a day",
    "Tome esta medicina dos veces al día":      "Take this medication twice a day",
    "Regrese si los síntomas empeoran":         "Come back if symptoms worsen",
    "Si se pone peor, vuelva":                  "Come back if symptoms worsen",
    "Haga cita con su médico en una semana":    "Follow up with your doctor in one week",
    "Busque su doctor en una semana":           "Follow up with your doctor in one week",
    "Vea a su doctor en una semana":            "Follow up with your doctor in one week",
    "Siga con su médico en una semana":         "Follow up with your doctor in one week",
    "Consulte con su médico en una semana":     "Follow up with your doctor in one week",
    "Vea a su médico en una semana":            "Follow up with your doctor in one week",
    "Llame al 911 si tiene una emergencia":     "Call 911 if you have an emergency",
}


# =============================================================================
# CRITICAL CLINICAL NOTES
# =============================================================================
REVIEW_NOTES = """
HIGHEST PRIORITY TERMS FOR CLINICAL REVIEW:

1. DIABETES — 'azúcar' vs 'diabetes'
   Caribbean patients (Dominican, PR, Cuban) often refer to diabetes as 'azúcar'.
   A patient may deny having 'diabetes' but confirm having 'azúcar'.

2. NAUSEA — 'náuseas' vs 'ganas de vomitar'
   Dominican patients may not recognize 'náuseas'.

3. FEVER — 'fiebre' vs 'calentura'
   Dominican patients commonly say 'calentura' not 'fiebre'.

4. BLOOD PRESSURE — 'presión' vs 'tensión'
   Colombian patients say 'tensión arterial' not 'presión arterial'.

5. MENSTRUAL PERIOD — major regional variation
   Dominican: 'el período' / 'me vino'
   Puerto Rican: 'me bajó'
   Mexican: 'la regla'
   Colombian: 'la menstruación'

6. DRINKING — 'beber' vs 'tomar'
   Caribbean patients use 'tomar' for drinking liquids.
   Always use 'no tome nada' for NPO instructions.
"""


# =============================================================================
# FUNCTIONS
# =============================================================================

def get_regional_translation(phrase_key, region="neutral"):
    """
    Returns the regional Spanish variant of an English phrase.
    Falls back to neutral if region or phrase not found.
    """
    if phrase_key not in REGIONAL_VARIANTS:
        return None, "Phrase not in regional dictionary"
    phrase_data = REGIONAL_VARIANTS[phrase_key]
    translation = phrase_data.get(region, phrase_data.get("neutral"))
    notes = phrase_data.get("notes", "")
    return translation, notes


def get_english_back_translation(spanish_phrase):
    """
    Returns the correct English translation for a Spanish preset phrase.
    Used in Spanish→English mode to bypass Argos Translate.
    Returns None if phrase not in dictionary.
    """
    return SPANISH_TO_ENGLISH.get(spanish_phrase.strip(), None)


def get_all_variants(phrase_key):
    """Returns all regional variants for a phrase."""
    if phrase_key not in REGIONAL_VARIANTS:
        return None
    return REGIONAL_VARIANTS[phrase_key]


def normalize(text: str) -> str:
    """Normalize text for fuzzy matching."""
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def find_best_match(text: str):
    """
    Find the best matching dictionary key for any input text.
    Handles case insensitive, punctuation differences, fuzzy word overlap.
    Returns best matching dictionary key, or None if no match found.
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


def find_best_spanish_match(spanish_text: str):
    """
    Find the best English back-translation for Spanish input using fuzzy matching.
    Used when exact match not found in SPANISH_TO_ENGLISH dictionary.
    """
    normalized_input = normalize(spanish_text)

    # 1. Exact match
    for spanish_key, english_val in SPANISH_TO_ENGLISH.items():
        if normalize(spanish_key) == normalized_input:
            return english_val

    # 2. Fuzzy match
    input_words = set(normalized_input.split())
    best_val = None
    best_score = 0.0

    for spanish_key, english_val in SPANISH_TO_ENGLISH.items():
        key_words = set(normalize(spanish_key).split())
        if not key_words:
            continue
        intersection = len(input_words & key_words)
        union = len(input_words | key_words)
        score = intersection / union if union > 0 else 0.0
        if score > best_score:
            best_score = score
            best_val = english_val

    if best_score >= 0.65:
        return best_val

    return None


def get_regional_translation_fuzzy(text: str, region: str = "neutral"):
    """
    Get regional translation using fuzzy matching.
    Use this for voice input and free text.
    """
    matched_key = find_best_match(text)
    if matched_key:
        return get_regional_translation(matched_key, region)
    return None, "No regional variant found"


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
    print(f"Total EN→ES phrases: {len(REGIONAL_VARIANTS)}")
    print(f"Total ES→EN entries: {len(SPANISH_TO_ENGLISH)}")

    print("\n=== DIABETES ===")
    variants = get_all_variants("Do you have diabetes?")
    for region, translation in variants.items():
        if region != "notes":
            back = get_english_back_translation(translation)
            print(f"  {region:15}: {translation} → '{back}'")

    print("\n=== BACK-TRANSLATION TEST ===")
    test_cases = [
        ("¿Tiene calentura?",       "Do you have a fever?"),
        ("¿Tiene azúcar?",          "Do you have diabetes?"),
        ("¿Dónde le duele?",        "Where does it hurt?"),
        ("¿Le bajó?",               "When was your last menstrual period?"),
        ("No coma ni tome nada",    "Do not eat or drink anything"),
    ]
    for spanish, expected in test_cases:
        result = get_english_back_translation(spanish)
        status = "PASS" if result == expected else "FAIL"
        print(f"  {status}: '{spanish}' → '{result}'")
