#!/usr/bin/env python3
import os
import sys
import time
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

HISTORY_FILE = os.path.expanduser("~/.zsh_history")

key = os.environ.get('OPENAI_TOKEN')
if not key:
    quit("OPENAI TOKEN NOT FOUND: Add it into the .env file for the chat-terminal project")

client = OpenAI(api_key=key)

steering_prompt = "Write a macos terminal command to perform the user's request. Return only the text that should be directly written into the user's terminal session. If no feasible macos command is possible then return the phrase `NO COMMAND FOUND`."

query = ' '.join(sys.argv[1:])
if not query:
    try:
        query = input("Write your prompt:\n> ").strip()
    except KeyboardInterrupt:
        quit()

response = client.chat.completions.create(model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": steering_prompt
        },
        {
            "role": "user",
            "content": query
        }
    ],
    temperature=1.0,
    max_tokens=75,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

subresp = response.choices[0].message.content
print(f"\n  {subresp}")

cont = input(f'\nRun this command? [Y/n]: ').strip()
if cont.lower().startswith('y') or cont == '':
    print()
    os.system(subresp)
    if HISTORY_FILE:
        with open(HISTORY_FILE, 'a') as file:
            file.write(f": {int(time.time())}:0;{subresp}")
else:
    print('stopping')
