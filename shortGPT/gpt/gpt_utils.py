import json
import os
import re
from time import sleep, time

import openai
import tiktoken
import yaml

from shortGPT.config.api_db import ApiKeyManager


def num_tokens_from_messages(texts, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        if isinstance(texts, str):
            texts = [texts]
        score = 0
        for text in texts:
            score += 4 + len(encoding.encode(text))
        return score
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
        See https://github.com/openai/openai-python/blob/main/chatml.md for information""")


def extract_biggest_json(string):
    json_regex = r"\{(?:[^{}]|(?R))*\}"
    json_objects = re.findall(json_regex, string)
    if json_objects:
        return max(json_objects, key=len)
    return None


def get_first_number(string):
    pattern = r'\b(0|[1-9]|10)\b'
    match = re.search(pattern, string)
    if match:
        return int(match.group())
    else:
        return None


def load_yaml_file(file_path: str) -> dict:
    """Reads and returns the contents of a YAML file as dictionary"""
    return yaml.safe_load(open_file(file_path))


def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    return json_data

from pathlib import Path

def load_local_yaml_prompt(file_path):
    _here = Path(__file__).parent
    _absolute_path = (_here / '..' / file_path).resolve()
    json_template = load_yaml_file(str(_absolute_path))
    return json_template['chat_prompt'], json_template['system_prompt']


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


import requests
import os
import re
from time import sleep

def gpt3Turbo_completion(chat_prompt="Give an interesting science fact", 
                         system="You are an AI that can give the answer to anything", 
                         temp=0.7, 
                         model="gemini-1.5-pro", 
                         max_tokens=1000, 
                         remove_nl=True, 
                         conversation=None):
    # Naga AI API Base URL and API Key
    base_url = 'https://api.naga.ac/v1'
    api_key = 'ng-LGcMxBTm67vhTuchGZMthJ3gJxb5L'
    
    # Headers for the API request
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Set up retries
    max_retry = 5
    retry = 0

    while True:
        try:
            # Prepare messages (conversation format)
            if conversation:
                messages = conversation
            else:
                messages = [
                    {"role": "system", "content": system},
                    {"role": "user", "content": chat_prompt}
                ]
            
            # Prepare the API payload (check Naga's required payload structure)
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temp
            }

            # Send the request to Naga AI
            response = requests.post(f"{base_url}/chat/completions", 
                                     headers=headers, 
                                     json=payload)

            # Raise error if request fails
            if response.status_code != 200:
                raise Exception(f"Error code: {response.status_code} - {response.json()}")

            # Extract the response text from the API response (based on Naga AI's structure)
            text = response.json()['choices'][0]['message']['content'].strip()

            # Optionally remove new lines
            if remove_nl:
                text = re.sub(r'\s+', ' ', text)
            
            # Log the response to a file
            filename = f'{model}_gpt3.txt'
            log_dir = '.logs/gpt_logs'
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            with open(f'{log_dir}/{filename}', 'w', encoding='utf-8') as outfile:
                outfile.write(f"System prompt: ===\n{system}\n===\n"
                              f"Chat prompt: ===\n{chat_prompt}\n===\n"
                              f"RESPONSE:\n====\n{text}\n===\n")

            return text

        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                raise Exception(f"Error communicating with Naga AI: {oops}")
            print(f'Error communicating with Naga AI: {oops}')
            sleep(1)  # Wait before retrying
