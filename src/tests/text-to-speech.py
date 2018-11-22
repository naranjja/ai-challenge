from gtts import gTTS

spanish_latam = "es-us"
spanish_spain = "es-ES"

key = "test"
say = "¡Buenos días Jose! Espero que todo te esté yendo bien con tus chatbots."

tts = gTTS(text=say, lang='es-us').save("./test.mp3")