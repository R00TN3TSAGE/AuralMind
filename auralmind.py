import speech_recognition as sr
import pyttsx3
import spacy

# Initialize the recognizer
r = sr.Recognizer()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Load spacy NLP model
nlp = spacy.load("en_core_web_sm")

def listen():
    """Listen to audio and convert it to text."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

def perform_action(text):
    """Perform an action based on the recognized text."""
    # This is a placeholder for more complex logic
    if "hello" in text.lower():
        return "Hello! How can I help you?"
    elif "how are you" in text.lower():
        return "I'm fine, thank you!"
    else:
        return "I'm not sure how to respond to that."

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def main():
    """Main function to run the Jarvis-like system."""
    print("Jarvis is listening. Speak now...")
    while True:
        text = listen()
        if text:
            response = perform_action(text)
            print(f"Jarvis: {response}")
            speak(response)
        else:
            speak("I didn't catch that. Could you please repeat?")

if __name__ == "__main__":
    main()
