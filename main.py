from dotenv import load_dotenv
from openai import OpenAI
from colorama import Fore, Style, init
from profile import collect_user_profile
from rules import apply_rules
from prompts import SYSTEM_PROMPT, build_prompt
import time

init(autoreset=True)
load_dotenv()

client = OpenAI()

def typing_effect(text, delay=0.02):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def main():
    print(Fore.CYAN + "\n🤖 VEHICLE RECOMMENDATION BOT\n")

    profile = collect_user_profile()
    warnings = apply_rules(profile)

    print(Fore.GREEN + "\nProfile saved! Ask your questions.\n")
    print(Fore.YELLOW + "Type 'exit' to quit.\n")

    while True:
        user_question = input(Fore.BLUE + "You ➜ ")

        if user_question.lower() in ["exit", "quit"]:
            print(Fore.CYAN + "Goodbye! 👋")
            break

        prompt = build_prompt(profile, warnings, user_question)

        response = client.responses.create(
            model="gpt-5-nano",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )

        print(Fore.GREEN + "\n🤖 Bot:")
        typing_effect(response.output_text)

if __name__ == "__main__":
    main()
