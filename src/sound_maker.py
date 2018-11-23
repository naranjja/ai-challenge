import gtts

loading = "¡Ok! Ya estoy lista. Veamos quién anda ahí."
gtts.gTTS(text=loading, lang="es-us").save(f"./../data/sounds/loading.mp3")

match = "Permíteme analizar tu rostro."
gtts.gTTS(text=match, lang="es-us").save(f"./../data/sounds/match.mp3")

