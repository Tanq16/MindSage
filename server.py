import json
import openai
from flask import Flask, request, jsonify
from functools import wraps
from youtube_transcript_api import YouTubeTranscriptApi
import re
import requests
import os

app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "The requested resource was not found."}), 404
@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "An internal server error occurred."}), 500

oai_key = os.environ["OPENAI_API_KEY"]

ALLOWLIST_PATTERN = re.compile(r"^[a-zA-Z0-9\s.,;:!?\-]+$")
def sanitize_content(content):
    return "".join(char for char in content if ALLOWLIST_PATTERN.match(char))

def fetch_content_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        sanitized_content = sanitize_content(response.text)
        return sanitized_content
    except requests.RequestException as e:
        return str(e)

def get_system_content(pattern):
    with open("./patterns/" + pattern + ".md") as f:
        return f.read()

def get_ytvideo_id(url):
    return url.split("?v=")[1][:11]

models = {
    "gpt3.5": "gpt-3.5-turbo-0125",
    "gpt4": "gpt-4-turbo",
}

@app.route("/<pattern>", methods=["POST"])
# needs link=1|0, model="gpt4"|"gpt3.5", and input=<link>|<input>
def milling(pattern):
    data = request.get_json()
    if "input" not in data:
        return jsonify({"error": "Missing input parameter"}), 400
    if data["link"]:
        if "youtu" in data["input"].split("/")[2]:
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(get_ytvideo_id(data["input"]), languages=["en"])
                input_data = " ".join([item["text"] for item in transcript_list])
                input_data = input_data.replace("\n", " ")
            except Exception as e:
                input_data = f"Transcript not available in the selected language (EN). ({e})"
        else:
            input_data = fetch_content_from_url(data["input"])
    else:
        input_data = data["input"]

    system_content = get_system_content(pattern)

    system_message = {"role": "system", "content": system_content}
    user_message = {"role": "user", "content": input_data}
    messages = [system_message, user_message]
    try:
        response = openai.chat.completions.create(
            model=models[data["model"]],
            messages=messages,
            temperature=0.0,
            top_p=1,
            frequency_penalty=0.1,
            presence_penalty=0.1,
        )
        assistant_message = response.choices[0].message.content
        return str(assistant_message)
    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while processing the request."}), 500

def main():
    """Runs the main fabric API backend server"""
    app.run(host="0.0.0.0", port=6000, debug=True)

if __name__ == "__main__":
    main()
