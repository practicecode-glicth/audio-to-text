# from flask import Flask, render_template, request
# import requests
# from googletrans import Translator

# app = Flask(__name__)

# DG_API_KEY = "0ff78babd6969e0facb7da35bb608e77b046726d"   # 🔹 Add your Deepgram API key here


# def transcribe_audio(file_path):
#     url = "https://api.deepgram.com/v1/listen"
#     headers = {"Authorization": f"Token {DG_API_KEY}"}

#     with open(file_path, "rb") as f:
#         audio_data = f.read()

#     response = requests.post(url, headers=headers, data=audio_data)

#     result = response.json()
#     text = result["results"]["channels"][0]["alternatives"][0]["transcript"]
#     return text


# @app.route("/", methods=["GET", "POST"])
# def index():
#     english_text = ""
#     hindi_text = ""

#     if request.method == "POST":
#         file = request.files["audiofile"]
#         if file:
#             filepath = "uploaded_audio.mp3"
#             file.save(filepath)

#             # English transcription
#             english_text = transcribe_audio(filepath)

#             # Hindi translation
#             translator = Translator()
#             hindi_text = translator.translate(english_text, dest="hi").text

#     return render_template("index.html",
#                            english_text=english_text,
#                            hindi_text=hindi_text)


# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, request
import requests

app = Flask(__name__)

DG_API_KEY = "0ff78babd6969e0facb7da35bb608e77b046726d"   # Add your Deepgram API key here


def transcribe_audio(file_path):
    url = "https://api.deepgram.com/v1/listen"
    headers = {"Authorization": f"Token {DG_API_KEY}"}

    with open(file_path, "rb") as f:
        audio_data = f.read()

    response = requests.post(url, headers=headers, data=audio_data)
    result = response.json()

    print(result)  # Debug if needed

    return result["results"]["channels"][0]["alternatives"][0]["transcript"]


def translate_to_hindi(text):
    url = "https://api.mymemory.translated.net/get"
    translated_full = ""
    
    # Break text into chunks of 400 characters
    chunks = [text[i:i+400] for i in range(0, len(text), 400)]
    
    for chunk in chunks:
        params = {
            "q": chunk,
            "langpair": "en|hi"
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        translated_full += data["responseData"]["translatedText"] + " "
    
    return translated_full.strip()


@app.route("/", methods=["GET", "POST"])
def index():
    english_text = ""
    hindi_text = ""

    if request.method == "POST":
        file = request.files["audiofile"]
        if file:
            filepath = "uploaded_audio.mp3"
            file.save(filepath)

            english_text = transcribe_audio(filepath)
            hindi_text = translate_to_hindi(english_text)

    return render_template("index.html",
                           english_text=english_text,
                           hindi_text=hindi_text)


if __name__ == "__main__":
    app.run(debug=True)
