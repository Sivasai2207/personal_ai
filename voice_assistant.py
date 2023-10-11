import sounddevice as sd
import numpy as np
import speech_recognition as sr
import webbrowser
import urllib.parse
import datetime
from gtts import gTTS
import os
import soundfile as sf  # Import soundfile for WAV file operations

SAMPLE_RATE = 44100
CHANNELS = 1
DTYPE = np.int16
DURATION = 5

r = sr.Recognizer()

def record_audio(duration=DURATION, samplerate=SAMPLE_RATE):
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=CHANNELS, dtype=DTYPE)
    sd.wait()
    return audio_data

def greet():
    current_time = datetime.datetime.now().strftime("%H:%M")
    response = f"Good day! The current time is {current_time}. How can I assist you today?"
    return response

def text_to_speech(text, filename="response.wav"):
    tts = gTTS(text, lang="en")
    tts.save(filename)
    os.system(f'afplay {filename}')

def assistant():
    print(greet())
    text_to_speech(greet())  # Greet with audio response

    while True:
        try:
            print("Recording audio...")
            recorded_audio = record_audio()
            
            # Save the recorded audio as a WAV file
            sf.write("temp.wav", recorded_audio, SAMPLE_RATE, format='wav')

            with sr.AudioFile("temp.wav") as source:
                audio_data = r.record(source)
                command = r.recognize_google(audio_data).lower()
                print("You said:", command)

            if "open google" in command:
                webbrowser.open("https://www.google.com/")

            elif "open youtube" in command:
                webbrowser.open("https://www.youtube.com/")

            elif "what's the time" in command:
                current_time = datetime.datetime.now().strftime("%H:%M")
                response = f"The current time is {current_time}"
                print(response)
                text_to_speech(response)

            elif "bye" in command:
                print("Goodbye!")
                text_to_speech("Goodbye!")
                break

            elif "search" in command:
                query = command.replace("search", "").strip()
                search_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
                webbrowser.open(search_url)

            else:
                print("I'm not sure how to help with that.")
                text_to_speech("I'm not sure how to help with that.")

        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Can you please repeat?")
            text_to_speech("Sorry, I didn't catch that. Can you please repeat.")
        except sr.RequestError:
            print("Sorry, I'm having trouble processing your request.")
            text_to_speech("Sorry, I'm having trouble processing your request.")
        except Exception as e:
            print(f"An error occurred: {e}")
            text_to_speech(f"An error occurred: {e}")

if __name__ == "__main__":
    assistant()
