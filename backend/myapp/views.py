import os, requests
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Note
from .serializers import NoteSerializer
import google.generativeai as genai

GEMMA_API_KEY = os.getenv('GEMMA_API_KEY')

'''
[Your Code]
   ↓
(API URL)  → where request   #optional to use
(API KEY)  → who is making request
   ↓
[Google Server]
   ↓
Response

'''
# def ask_gemma(prompt):
#     try:
#         res = requests.post(
#             'https://generativelanguage.googleapis.com/v1beta/models/gemma-3-27b-it:generateContent',
#             headers={'Content-Type': 'application/json'},
#             params={'key': GEMMA_API_KEY},
#             json={'contents': [{'parts': [{'text': prompt}]}]}
#         )

#         data = res.json()

#         # DEBUG (important)
#         print("Gemma response:", data)

#         return data['candidates'][0]['content']['parts'][0]['text']

#     except Exception as e:
#         print("Gemma ERROR:", str(e))
#         return "⚠️ AI failed to respond. Check API key or quota."
genai.configure(api_key=os.getenv("GEMMA_API_KEY"))

# create model once (better performance)
model = genai.GenerativeModel("gemma-4-31b-it")

def ask_gemma(prompt):
    try:
        response = model.generate_content(prompt)

        # DEBUG
        print("Gemma response:", response.text)

        return response.text

    except Exception as e:
        print("Gemma ERROR:", str(e))
        return "⚠️ AI failed to respond. Check API key or quota."

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        title = self.request.data.get('title', '')
        ai_reply = ask_gemma(f'Give a one-line tip about: {title}')
        serializer.save(ai_reply=ai_reply)

    def perform_update(self, serializer):
        title = self.request.data.get('title', '')
        ai_reply = ask_gemma(f'Update tip about: {title}')
        serializer.save(ai_reply=ai_reply)