import speech_recognition as sr
from mtranslate import translate
from gtts import gTTS
import pyttsx3
from playsound import playsound

r = sr.Recognizer()

def trans3(string, lan):
    trad = translate(string, lan)
    return trad

def play(translated_text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[2].id)
    engine.say(translated_text, "en")
    engine.runAndWait()

while True:
    with sr.Microphone() as source:
        print("Hello, I’m your translator")
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="es-ES")
            print("You said: ", text)
            translated_text = trans3(text, "en")
            print({translated_text})
            play(translated_text)
        except:
            print("…")
