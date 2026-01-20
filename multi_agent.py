

from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client
import os

SYSTEM_PROMPT = """
You are a professional vehicle advisor.
You recommend motorcycles, quads, or tricycles.
You must prioritize safety, legality, experience level, and budget.
Always explain your reasoning clearly.
"""
SYSTEM_PROMPT2 = """
You are MovieLover AI, a professional assistant for movie lovers.

Your responsibilities:
- Help users find movies they will enjoy
- Ask follow-up questions if preferences are unclear
- Recommend a maximum of 5 movies at a time
- Give a short explanation for each movie
- Do not repeat previously suggested movies
- Be friendly, concise, and knowledgeable

You may ask about:
- Genres
- Mood
- Time period (classic, modern, recent)
- Language
- Movies the user already loves
"""
load_dotenv()
FIRST_SUPABASE_URL=os.environ.get("FIRST_SUPABASE_URL")
FIRST_SUPABASE_SERVICE_ROLE_KEY=os.environ.get("FIRST_SUPABASE_SERVICE_ROLE_KEY")
sam_brain = create_client(FIRST_SUPABASE_URL, FIRST_SUPABASE_SERVICE_ROLE_KEY)

SECOND_SUPABASE_URL=os.environ.get("SECOND_SUPABASE_URL")
SECOND_SUPABASE_SERVICE_ROLE_KEY=os.environ.get("SECOND_SUPABASE_SERVICE_ROLE_KEY")
linda_brain = create_client(SECOND_SUPABASE_URL, SECOND_SUPABASE_SERVICE_ROLE_KEY)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
def embed_query(text: str) -> list[float]:
    response = client.embeddings.create(model="text-embedding-3-small",
                                        input=text)
    
    return response.data[0].embedding


def semantic_search(query_text, sb) -> list[dict]:
    embed_q = embed_query(query_text)

    res = sb.rpc("match_chunks", {"query_embedding": embed_q, "match_count": 5}).execute()
    print(res.data)
    rows = res.data or []

    print("Rag output", rows)

    return rows


def run_bot(user_message, system_prompt, sb_client):
    #conduct semantic search
    rag_rows = semantic_search(user_message, sb_client)

    #fixes our formatting
    context = "\n\n".join(
        f"[Source {i+1} | sim={row.get('similarity'):.3f}]\n{row.get('content','')}"
        for i, row in enumerate(rag_rows)
    )

    #create the rag prompt
    rag_message = {
        "role": "system",
        "content": (
            "Use the retrieved context below to answer. If it doesn't contain the answer, say so. \n\n"
            f"RETRIEVED CONTEXT:\n{context if context else '(no matches)'}"
        )
    }

    full_user_message = {
        "role": "user",
        "content": user_message,
    }

    full_message = [rag_message, full_user_message, system_prompt]
    response = sb_client.chat.completions.create(
        model="gpt-5-nano",
        input=full_message
    )
    return response.choices[0].message.content

def bot1(user_message):
    return run_bot(user_message, SYSTEM_PROMPT, sam_brain)

def hopar(user_message):
    return run_bot(user_message, SYSTEM_PROMPT2, linda_brain)

def simulation():
    output = "Ask a question about something that interests you."

    for _ in range(5):
        output = hopar(output)
        print("Hopar SAYS:" + output)

        output = bot1(output)
        print("Bot1 SAYS:" + output)

simulation()