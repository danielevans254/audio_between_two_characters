from openai import AsyncOpenAI
import chainlit as cl

client = AsyncOpenAI()

@cl.step(type="tool")
async def generate_text_answer(transcription):
    model = "gpt-3.5-turbo"
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": transcription}
    ]

    response = await client.chat.completions.create(
        messages=messages, model=model, temperature=0.3
    )

    choices = response.choices
    if choices and len(choices) > 0:
        content = choices[0].message.content
        return content
    else:
        return "No response from the model."
