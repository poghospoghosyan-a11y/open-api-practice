from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from prompts import SYSTEM_PROMPT, build_prompt
from rules import apply_rules
from supabase import create_client
import os

# Load environment variables
load_dotenv()
print("SUPABASE_URL =", os.getenv("FIRST_SUPABASE_URL"))
print("CWD =", os.getcwd())


# Create clients ONCE
client = OpenAI()
sb = create_client(
    os.environ["FIRST_SUPABASE_URL"],
    os.environ["FIRST_SUPABASE_SERVICE_ROLE_KEY"]
)

app = Flask(__name__, static_folder="public", static_url_path="")

def embed_query(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def semantic_search(query_text: str) -> list[dict]:
    emb_q = embed_query(query_text)
    res = sb.rpc(
        "match_chunks",
        {"query_embedding": emb_q, "match_count": 5}
    ).execute()
    return res.data or []

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

    rag_rows = semantic_search(prompt)

    context = "\n\n".join(
        f"[Source {i+1} | sim={row.get('similarity'):.3f}]\n{row.get('content','')}"
        for i, row in enumerate(rag_rows)
    )

    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {
                "role": "system",
                "content": (
                    f"{SYSTEM_PROMPT}\n\n"
                    "Use the retrieved context below.\n\n"
                    f"RETRIEVED CONTEXT:\n{context or '(no matches)'}"
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )

    return jsonify({"reply": response.output_text})

if __name__ == "__main__":
    app.run(debug=True)
