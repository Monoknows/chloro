from brain import ask_chloro
from ears import listen
from voice import speak

def main():
    speak("Good day, Sir. CHLORO is online. How can I help?")

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
