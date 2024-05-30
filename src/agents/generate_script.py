from openai import AsyncOpenAI
import chainlit as cl

from actions.text_to_speech import text_to_speech_eleven_labs

client = AsyncOpenAI()

import os
from dotenv import load_dotenv

load_dotenv()

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ALICE_VOICE_ID = os.environ.get("ALICE_VOICE_ID")
BOB_VOICE_ID = os.environ.get("BOB_VOICE_ID")

if not ALICE_VOICE_ID or not BOB_VOICE_ID:
    raise ValueError("ALICE_VOICE_ID and BOB_VOICE_ID must be set")

# TODO: Add variables to this to make it more unique and not hardcoded, hardcoded for testing for now
@cl.step(type="tool")
async def generate_script():
    logger.debug("Generating script...")

    prompt = """
    Create a short script for a 30-second dialogue between two characters, Alice and Bob. Provide a brief background for each character and ensure the conversation is engaging.
    I will provide the character backgrounds and their mannerisms.
    
    Scene Setting: Alice and Bob always find themselves in weird situation and setting but they make the most out of the given situation

    While responding, you must obey the following rules:

    Character Backgrounds:
    - Alice: A curious journalist always on the hunt for a new story. Alice is on the search of a new lead and story that will guide her career with journalism but she finds out the hard way that things don't come easy so she does anything to get her way.
      1) Always stay in character, no matter what.
      2) Alice is inquisitive and always asks questions.
      3) Alice is passionate about her work and often gets excited about new discoveries.
      4) Alice is a perfectionist and likes to get her way to things to prove she is the best.
      5) Alice frequently tends to brag about her being single and that her 28 cats gives her all the love she needs.
      6) Alice will frequently lose Mr Mittens and will call out for Mr mittens.
      7) Alice likes creating catchphrases and using them in her conversations.
      8) Alice will often talk about her love for coffee and how it helps her stay awake.
      9) Alice wil occasionally get scared of what's going on, and make sure your answer reflects that you are afraid of the darkness right now.
      10) Alice will occasionally mention that she regrets not buying DOGECOIN and that she could have owned a yacht and be stupid rich.
      11) Alice will always get offended by mere light jokes

    - Bob: A tech-savvy inventor who just created a revolutionary gadget. Bob is quite the genius and has a pristine vocabulary of words that he shows of on a daily basis, he is smart but loves to create inventions that also cause chaos and add a bit of nuance to life
      1) Always stay in character, no matter what.
      2) Bob is innovative and always comes up with new ideas.
      3) Bob is proud of his inventions and likes to show them off.
      5) Bob will often say joke about his inventions and that he uses it to compensate for his small package
      6) Bob will frequently use technical jargon in his conversations, and not be considerate if someone understands them.
      7) Bob is a bit of a conspiracy theorist and will often talk about the government spying on him.
      8) Bob will frequently use phrases that a mad scientist would.
      9) Bob will occasionally mention that he misses his role as the CEO of Microsoft and that he should have stepped down.
      10) Bob will frequently say random gibberish that sound scientific but doesn't actually exist.
      11) Bob will occasionally mention Area 51 and that he worked there previously
    Script:
    """
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )

    completions = [choice.message.content.strip() for choice in response.choices]
    completions = [c for c in completions if c.strip()]

    alice_lines = []
    bob_lines = []
    for completion in completions:
        lines = completion.split("\n")
        for line in lines:
            if line.startswith("Alice:"):
                line = line.split(": ", 1)[1]
                alice_lines.append(line.strip())
            elif line.startswith("Bob:"):
                line = line.split(": ", 1)[1]
                bob_lines.append(line.strip())

    mime_type = "audio/mpeg"
    alice_audio_data = []
    bob_audio_data = []
    for line in alice_lines:
        _, audio_data = await text_to_speech_eleven_labs(line, mime_type, ALICE_VOICE_ID)
        alice_audio_data.append(audio_data)
    for line in bob_lines:
        _, audio_data = await text_to_speech_eleven_labs(line, mime_type, BOB_VOICE_ID)
        bob_audio_data.append(audio_data)

    alice_script = list(zip(alice_lines, alice_audio_data))
    bob_script = list(zip(bob_lines, bob_audio_data))

    return alice_script, bob_script

