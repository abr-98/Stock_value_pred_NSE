import os

from apis.logging_config import setup_logging, log_service_io


logger = setup_logging("service-environment")

def load_api_key():
  log_service_io(logger, "environment.load_api_key.request", inputs={"source_file": "OpenAI-Key.txt"})
  with open("OpenAI-Key.txt") as api_key_file:
    os.environ["OPENAI_API_KEY"] = api_key_file.readline()
  log_service_io(logger, "environment.load_api_key.response", outputs={"openai_key_loaded": True})