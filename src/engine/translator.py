import logging
from speech_recognition import Recognizer, Microphone
from mtranslate import translate
import pyttsx3


def instantiate_tools(logger: logging):
    try:
        return Recognizer(), Microphone()
    except OSError:
        logger.error("No device Audio Available or Incompatible")
        return exit(0)


def trans3(string, lan):
    trad = translate(string, lan)
    return trad


def play(translated_text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[2].id)
    engine.say(translated_text, "en")
    engine.runAndWait()


def listen(recognizer: Recognizer, logger: logging):
    while True:
        with Microphone() as source:
            print("Hello, I’m your translator")
            recognizer.pause_threshold = 1
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language="es-ES")
                print("You said: ", text)
                translated_text = trans3(text, "en")
                print({translated_text})
                play(translated_text)
            except Exception as e:
                logger.error("Error: ", str(e))



