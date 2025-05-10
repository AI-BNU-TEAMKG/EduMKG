import os
import shutil
import sys
from pathlib import Path
from venv import logger
from openai import OpenAI
import time
import requests
import json
from timeit import default_timer as timer
def synthesize_speech_from_text(text:str, concept:str, filePath:str) -> bool:
 
    # Initialize the speech synthesizer
    # you can customize the synthesis parameters, like voice, format, sample_rate or other parameters
    if not os.path.exists(filePath+concept+".wav") and not os.path.exists(filePath+concept+".mp3"):
        speech_file_path = filePath+concept+".mp3"
        while True:
            try:
                client = OpenAI(
                        base_url= "",
                        api_key = "",
                    )
                response = client.audio.speech.create(
                    input=text,
                    model="tts-1",
                    voice="",
                )
                response.stream_to_file(speech_file_path)
                print(f"{speech_file_path}  ")
                return True
            except Exception as e:
                print(f"Error occurred: {e}")
                print("Retrying...")
                time.sleep(61)  # Wait for a while before retrying
                continue
    else:
        return False

def speechGenerator(text: str, concept:str,filePath:str) -> None:
    synthesize_speech_from_text(text,concept,filePath)







