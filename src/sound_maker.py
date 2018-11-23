import gtts

loading = "¡Buenas tardes Jose Naranjo! Adelante por favor."
gtts.gTTS(text=loading, lang="es-us").save(f"./../data/sounds/greeting.mp3")

# match = "Permíteme analizar tu rostro."
# gtts.gTTS(text=match, lang="es-us").save(f"./../data/sounds/match.mp3")

