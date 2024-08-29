import os
import pyttsx3
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import google.generativeai as genai
import streamlit as st

# Initialize the recognizer and the translator
recognizer = sr.Recognizer()
translator = Translator()

# Configure the Google Generative AI model
genai.configure(api_key="AIzaSyA4A_26tCHH8_-2-G91WuX7OkiamuQRAno")  # Replace with your actual API key

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[]
)

# Function to translate text and convert to speech
def translate_and_speak(text, dest_lang):
    # Translate text
    translated = translator.translate(text, dest=dest_lang)
    translated_text = translated.text

    # Convert to speech
    tts = gTTS(text=translated_text, lang=dest_lang)
    audio_file = f"{dest_lang}.mp3"
    tts.save(audio_file)
    
    return translated_text, audio_file

# Streamlit application
def main():
    st.title("Speech-to-Text and Multi-Language Translator with Speech Output")

    # Sidebar for language selection
    st.sidebar.header("Select Target Languages")
    target_languages = st.sidebar.multiselect("Target Languages", list(LANGUAGES.values()))

    st.write(f"Translating to: {', '.join(target_languages)}")

    # Button to start the recording process
    if st.button("Record Speech"):
        with sr.Microphone() as source:
            st.write("Adjusting for ambient noise, please wait...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            st.write("Say something:")
            audio = recognizer.listen(source, timeout=6)

        # Recognize speech using Google Web Speech API
        try:
            st.write("Recognizing...")
            text = recognizer.recognize_google(audio)
            st.write("You said: " + text)
            
            # Generate a response based on the input text
            instruction = "1.give accurate information about the text limitto 100 words"
            user_input = instruction + text
            response = chat_session.send_message(user_input)
            response_text = response.text
            st.write("AI Response: " + response_text)
            
            # Translate and convert to speech for each target language
            for language in target_languages:
                dest_lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(language)]
                translated_text, audio_file = translate_and_speak(response_text, dest_lang_code)
                
                st.write(f"**{language}**:")
                st.write(translated_text)
                audio_data = open(audio_file, 'rb').read()
                st.audio(audio_data, format='audio/mp3')
                os.remove(audio_file)  # Clean up the audio file after playing

        except sr.UnknownValueError:
            st.write("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
        except sr.WaitTimeoutError:
            st.write("Listening timed out while waiting for phrase to start")

if __name__ == "__main__":
    main()
