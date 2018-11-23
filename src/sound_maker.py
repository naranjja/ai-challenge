import gtts

loading = "¡Ok! Veamos."
gtts.gTTS(text=loading, lang="es-us").save(f"./../data/sounds/loading.mp3")

match = "Permíteme analizar tu rostro."
gtts.gTTS(text=match, lang="es-us").save(f"./../data/sounds/match.mp3")
