import speech_recognition as sr
import pyttsx3
import spacy
from datetime import datetime
import json

# Initialize the recognizer
r = sr.Recognizer()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Load spacy NLP model
nlp = spacy.load("en_core_web_sm")

# Placeholder for user profiles and context management
context = {"last_command": None, "user": "default", "authenticated": False}
user_profiles = {
    "default": {
        "name": "User",
        "preferences": {
            "greeting": "Hi there! How can I assist you today?",
            "farewell": "Goodbye, and have a great day!",
        },
        "language": "en",
    },
    # Additional user profiles could be added here
}

# Placeholder for multi-language support
languages = {"en": "English", "fr": "French"}
nlp_models = {"en": spacy.load("en_core_web_sm"), "fr": spacy.load("fr_core_news_sm")}

def listen(language="en"):
    """Listen to audio and convert it to text."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        # Language parameter can be used here for speech recognition in different languages
        text = r.recognize_google(audio, language=language)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        speak("I couldn't understand what you said. Please try again.", language)
        return None
    except sr.RequestError as e:
        speak(f"Could not request results from the speech recognition service; {e}", language)
        return None

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
        speak("I couldn't understand what you said. Please try again.")
        return None
    except sr.RequestError as e:
        speak(f"Could not request results from the speech recognition service; {e}")
        return None

def analyze_intent(text):
    """Analyze the text to understand the user's intent using spacy for NLP."""
    doc = nlp(text)

    # Expanded intent patterns
intent_patterns = {
    "inquiry_wellbeing": [("how", "are", "you")],
    "query_time": [("what", "time"), ("time",)],
    "farewell": [("goodbye",), ("bye",)],
    "greeting": [("hello",), ("hi",)],
    "weather_check": [("how", "weather"), ("weather", "today"), ("forecast",)],
    "play_music": [("play", "music"), ("start", "song"), ("music",)],
    "set_alarm": [("set", "alarm"), ("wake", "me"), ("alarm",)],
    "create_reminder": [("remind", "me"), ("set", "reminder"), ("reminder",)],
    "ask_directions": [("how", "get", "to"), ("direction", "to"), ("navigate",)],
    
    # Additional patterns
    "check_email": [("check", "email"), ("read", "email"), ("emails",)],
    "send_email": [("send", "email"), ("write", "email"), ("email", "to")],
    "query_date": [("what", "date"), ("today's", "date"), ("date", "today")],
    "news_update": [("latest", "news"), ("news", "update"), ("what's", "news")],
    "stock_prices": [("stock", "price"), ("shares", "value"), ("market", "rate")],
    "order_food": [("order", "food"), ("delivery", "food"), ("food", "order")],
    "book_cab": [("book", "cab"), ("call", "taxi"), ("ride", "to")],
    "play_movie": [("play", "movie"), ("watch", "film"), ("movie",)],
    "turn_on_lights": [("turn", "on", "light"), ("lights", "on"), ("brighten", "room")],
    "turn_off_lights": [("turn", "off", "light"), ("lights", "off"), ("darken", "room")],
    "set_thermostat": [("set", "temperature"), ("adjust", "thermostat"), ("room", "temperature")],
    "open_app": [("open", "app"), ("launch", "application"), ("start", "program")],
    "make_call": [("make", "call"), ("call", "to"), ("dial",)],
    "send_text": [("send", "text"), ("text", "to"), ("message",)],
    "add_to_calendar": [("add", "to", "calendar"), ("schedule", "event"), ("calendar", "entry")],
    "play_podcast": [("play", "podcast"), ("listen", "podcast"), ("podcast", "episode")],
    "find_recipe": [("find", "recipe"), ("recipe", "for"), ("how", "make")],
    "translate_word": [("translate", "to"), ("what's", "in"), ("how", "say")],
    "calculate": [("calculate",), ("what's", "plus", "minus"), ("how", "much", "is")],
}

    # Simplified checker for matching patterns in the spacy doc
    def pattern_matcher(doc, patterns):
        text_tokens = [token.lemma_.lower() for token in doc]
        for pattern in patterns:
            if all(word in text_tokens for word in pattern):
                return True
        return False

    # Iterate through defined patterns to find a match
    for intent, patterns in intent_patterns.items():
        if pattern_matcher(doc, patterns):
            return intent

    # If no predefined patterns match, return unknown
    return "unknown"

def perform_action(intent):
    """Perform an action based on the recognized intent."""
    responses = {
        "inquiry_wellbeing": "I'm just a program, so I'm always okay!",
        "query_time": f"Currently, it's {datetime.now().strftime('%H:%M on %B %d, %Y')}.",
        "farewell": user_profiles[context["user"]]["preferences"]["farewell"],
        "unknown": "I'm not sure how to respond to that."
    }
    return responses.get(intent, "I'm not sure how to respond to that.")

def speak(text):
    """Convert text to speech."""
    print(f"Assistant: {text}")  # Print response for debugging
    engine.say(text)
    engine.runAndWait()

def main():
    """Main function to run the assistant."""
    user_language = user_profiles[context["user"]]["language"]
    speak(user_profiles[context["user"]]["preferences"]["greeting"], user_language)

    while True:
        text = listen(user_language)
        if text:
            intent, entities = analyze_intent(text, user_language)
            response = perform_action(intent, entities, user_language)
            speak(response, user_language)
            if intent == "farewell":
                break
        else:
            speak("I didn't catch that. Could you please repeat?", user_language)

if __name__ == "__main__":
    main()
