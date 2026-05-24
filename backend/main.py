from brain import ask_chloro
from ears import listen
from voice import speak

def main():
    speak("Hello! I am CHLORO, your personal assistant. How can I help you today?")

    while True:
        query = listen()
        if not query:
            continue
            
        if query.lower() in ["exit", "quit", "goodbye"]:
            speak("Goodbye! Have a great day!")
            break
            
        ai_response = ask_chloro(query)
        print(f"CHLORO: {ai_response}")
        speak(ai_response)

if __name__ == "__main__":
    main()