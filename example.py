from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

user_prompt = input("Enter your prompt")

response = client.responses.create(

    model="gpt-5-nano",
    input="write me a short story about a group of coders from armenia"
)

print(response.output_text)
