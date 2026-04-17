import os

import google.generativeai as genai

# 🔑 add your API key
# GEMMA_API_KEY = os.getenv('GEMMA_API_KEY')

genai.configure(api_key="AIzaSyDLoPaH86c7QD0UFozSOVL5877uuLkbP6g")

# 🚀 Gemma 4 model
model = genai.GenerativeModel("gemma-4-31b-it")

# prompt
response = model.generate_content("I need to learn how i can use gemma api in python, can you give me a simple example?")

print(response.text)