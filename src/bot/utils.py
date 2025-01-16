from openai import OpenAI
import os
import config
import ollama

OPENAI_API_KEY = config.env('OPENAI_API_KEY', default=None, cast=str)


def chat_with_ollama(message, model='llama2'):
    
    response = ollama.chat(model=model, messages=[
    {
        'role': 'user',
        'content': message,
    },
    ])
    print(response['message']['content'])
    return response['message']['content']


def get_openai_client():
    return OpenAI(api_key=OPENAI_API_KEY)

def chat_with_openai(message, model="gpt-3.5-turbo", raw=False):
    client = get_openai_client()
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user", 
                "content": "write a haiku about ai"
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    if raw:
        return response
    return response.choices[0].message['content']

