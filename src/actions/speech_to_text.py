import openai
import chainlit as cl

@cl.step(type="tool")
async def speech_to_text(audio_file):
    response = await openai.Audio.transcriptions.create(
        model="whisper-1", file=audio_file
    )
    return response.text
