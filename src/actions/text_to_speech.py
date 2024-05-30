import httpx
from io import BytesIO
import chainlit as cl
import os
from dotenv import load_dotenv
load_dotenv()

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY must be set")

@cl.step(type="tool")
async def text_to_speech_eleven_labs(text: str, mime_type: str, voice_id: str):
    logger.debug(f"Converting text to speech for text: {text}, voice_id: {voice_id}")

    CHUNK_SIZE = 1024

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": mime_type,
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    async with httpx.AsyncClient(timeout=25.0) as client:
      response = await client.post(url, json=data, headers=headers)
      response.raise_for_status()
      print(response)

      buffer = BytesIO()
      buffer.name = f"output_audio.{mime_type.split('/')[1]}"

      async for chunk in response.aiter_bytes(chunk_size=CHUNK_SIZE):
        if chunk:
          buffer.write(chunk)
      
      buffer.seek(0)
      print("buffer name:", buffer.name)
      # print("buffer content:", buffer.read())
      return buffer.name, buffer.read()
