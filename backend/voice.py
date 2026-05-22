import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Using the voice of a Male speaker
    engine.setProperty('rate', 150)  # Adjust the speech rate
    engine.say(text)
    engine.runAndWait()