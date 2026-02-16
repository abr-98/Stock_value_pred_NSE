import os

def load_api_key():
  with open("OpenAI-Key.txt") as api_key_file:
    os.environ["OPENAI_API_KEY"] = api_key_file.readline()