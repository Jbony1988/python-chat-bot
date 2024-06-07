from flask import Flask, request, render_template
from openai import OpenAI
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')


client = OpenAI(api_key=openai_api_key)

app = Flask(__name__)

# Initialize OpenAI API key

def format_code_snippets(response_text):
    # Use regex to find code snippets and wrap them with terminal-styled div
    code_snippet_pattern = re.compile(r'```(.*?)```', re.DOTALL)
    formatted_text = code_snippet_pattern.sub(
        lambda match: f'<div class="terminal"><button class="copy-button" onclick="copyToClipboard(this)">Copy</button><pre>{match.group(1)}</pre></div>',
        response_text
    )
    return formatted_text

def generate_response(prompt):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an online tutor for Python programming."},
        {"role": "user", "content": prompt},
    ])
    message = response.choices[0].message.content.strip()
    formatted_message = format_code_snippets(message)
    return formatted_message

@app.route("/", methods=["GET", "POST"])
def index():
    user_input = None
    response = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        prompt = f"The user says: {user_input}"
        response = generate_response(prompt)
    return render_template("index.html", user_input=user_input, response=response)

if __name__ == "__main__":
    app.run(debug=True)
