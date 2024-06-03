import chainlit as cl
from agents.generate_script import generate_script
from agents.characters import CharacterAgent
from actions.text_to_speech import text_to_speech_eleven_labs

from pydub import AudioSegment
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

# TODO: Instead of creating seperate audio files for each character merge into one audio file
def concatenate_audio(audio_segments):
    combined = AudioSegment.empty()
    for segment in audio_segments:
        combined += AudioSegment.from_file(BytesIO(segment), format="mp3")
    return combined

# FIXME: Only works upon first initialization
# TODO: Add a way to create other characters and assign their personalities, and have them interact with each other, and have a conversation, in the same way as Alice and Bob, but for now for testing purposes, we will only have Alice and Bob hardcoded along with their personality traits

@cl.on_message
async def manage_conversation():
    global alice_turn
    mime_type = "audio/mpeg"
    answer_message = await cl.Message(content="").send()

    if "alice" not in globals():
        alice_script, bob_script = await generate_script()
        global alice, bob
        alice = CharacterAgent("Alice", alice_script)
        bob = CharacterAgent("Bob", bob_script)
        alice_turn = True
        print(alice, bob)

    all_lines = []
    all_audio_data = []

    while True:
        if alice_turn:
            line, audio_data = alice.speak()
            if not line and not audio_data:
                break
            all_lines.append({"author": "Alice", "line": line})
            all_audio_data.append(audio_data)
            alice_turn = False
        else:
            line, audio_data = bob.speak()
            if not line and not audio_data:
                break
            all_lines.append({"author": "Bob", "line": line})
            all_audio_data.append(audio_data)
            alice_turn = True

    for entry in all_lines:
        await cl.Message(content=entry["line"], author=entry["author"]).send()

    combined_audio = concatenate_audio(all_audio_data)
    audio_io = BytesIO()
    combined_audio.export(audio_io, format="mp3")
    audio_io.seek(0)

    output_audio_el = cl.Audio(
        auto_play=True,
        mime=mime_type,
        content=audio_io.read(),
    )
    answer_message.elements = [output_audio_el]
    await answer_message.update()

if __name__ == "__main__":
    cl.run(manage_conversation)
