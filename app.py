# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
import os

app = Flask(__name__)
translator = Translator()

# Voice recognition
def recognize_voice():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except:
        return "Voice not recognized"


@app.route("/", methods=["GET", "POST"])
def index():

    translated_text = ""
    input_text = ""
    audio_file = ""

    if request.method == "POST":

        # Voice or text input
        if "voice" in request.form:
            input_text = recognize_voice()
        else:
            input_text = request.form.get("text", "")

        language = request.form.get("language", "en")

        # Translate text
        try:
            translation = translator.translate(input_text, dest=language)
            translated_text = translation.text
        except:
            translated_text = "Translation error"

        # Generate speech audio
        try:

            # Language mapping for gTTS
            lang_map = {
                "en": "en",
                "hi": "hi",
                "gu": "gu",
                "mr": "mr",
                "ta": "ta",
                "bn": "bn",
                "pa": "pa",
                "fr": "fr",
                "es": "es"
            }

            tts_lang = lang_map.get(language, "en")

            # delete old audio
            if os.path.exists("static/output.mp3"):
                os.remove("static/output.mp3")

            tts = gTTS(
                text=translated_text,
                lang=tts_lang,
                slow=False
            )

            audio_file = "static/output.mp3"
            tts.save(audio_file)

        except Exception as e:
            print("Audio generation error:", e)
            audio_file = ""

    return render_template(
        "index.html",
        translated_text=translated_text,
        input_text=input_text,
        audio_file=audio_file
    )


if __name__ == "__main__":
    app.run(debug=True)