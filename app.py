from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from prompts import SYSTEM_PROMPT, build_prompt
from rules import apply_rules

load_dotenv()
client = OpenAI()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    profile = {
        "age": data["age"],
        "height": data["height"],
        "weight": data["weight"],
        "experience": data["experience"],
        "use_case": data["use_case"],
        "budget": data["budget"],
        "country": data["country"],
        "preference": data["preference"]
    }

    question = data["message"]
    warnings = apply_rules(profile)

    prompt = build_prompt(profile, warnings, question)

    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return jsonify({"reply": response.output_text})

if __name__ == "__main__":
    app.run(debug=True)
