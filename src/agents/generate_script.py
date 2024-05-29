from openai import AsyncOpenAI
import chainlit as cl

client = AsyncOpenAI()

@cl.step(type="tool")
async def generate_script():
    prompt = """
    Create a short script for a 30-second dialogue between two characters, Alice and Bob. Provide a brief background for each character and ensure the conversation is engaging.

    Character Backgrounds:
    - Alice: A curious journalist always on the hunt for a new story.
    - Bob: A tech-savvy inventor who just created a revolutionary gadget.

    Script:
    """
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )

    # Extract the completions from the response
    completions = [choice.message.content.strip() for choice in response.choices]

    # Parse the completions into lines for Alice and Bob
    alice_lines, bob_lines = parse_completions(completions)
    
    # Join the parsed lines into a single string for each character
    alice_script = "\n".join(alice_lines)
    bob_script = "\n".join(bob_lines)
    
    # Return the parsed scripts for Alice and Bob
    return alice_script, bob_script

def parse_completions(completions):
    alice_lines = []
    bob_lines = []
    current_character = None
    
    for completion in completions:
        for line in completion.split('\n'):
            # Alternate lines between Alice and Bob
            if current_character == "Alice":
                bob_lines.append(line.strip())
                current_character = "Bob"
            else:
                alice_lines.append(line.strip())
                current_character = "Alice"
                
    return alice_lines, bob_lines

