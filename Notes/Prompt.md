my api for performing crud
http://127.0.0.1:8000/notes/

this is the response 
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "title": "Testing",
        "ai_reply": "Testing here",
        "created_at": "2026-04-11T01:36:46.473442Z"
    },
    {
        "id": 2,
        "title": "Testing again",
        "ai_reply": "Don't just test your happy path – actively try to *break* your code to uncover hidden bugs and ensure robustness.\n\n\n\n",
        "created_at": "2026-04-11T01:54:15.691533Z"
    },
    {
        "id": 3,
        "title": "Testing again",
        "ai_reply": "Don't just test your happy path – actively try to *break* your code to uncover hidden bugs and ensure robustness.\n\n\n\n",
        "created_at": "2026-04-11T01:54:16.752320Z"
    },
    {
        "id": 4,
        "title": "Testing again",
        "ai_reply": "Don't just test your happy path – actively try to *break* your code to uncover hidden bugs and ensure robustness.\n\n\n\n",
        "created_at": "2026-04-11T01:54:18.463458Z"
    }
]


that is 100% working code what i tested


import google.generativeai as genai

# 🔑 add your API key
genai.configure(api_key="AIzaSyDFgaLEzroG1tUpS60yK9EmiAejw__Ulrs")

# 🚀 Gemma 4 model
model = genai.GenerativeModel("gemma-4-31b-it")

# prompt
response = model.generate_content("I need to learn how i can use gemma api in python, can you give me a simple example?")

print(response.text)


I want to perfrom the crud with html and js
package which we will use that is axios and all the crud operations i must be able to perform


here you go with my html which must be able to show the output and perform crud operation 
<!DOCTYPE html>
<html>
<head>
  <title>Notes + AI</title>
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  <script src="app.js" defer></script>
</head>
<body>
  <h2>📝 Notes + 🤖 Gemma AI</h2>
  <input id="inp" placeholder="Write a note..." />
  <button onclick="addNote()">Add</button>
  <div id="list"></div>
</body>
</html


and this is the js file 
// In production, replace with your Render URL
const API = 'http://127.0.0.1:8000/notes/'

async function addNote() {
  const title = document.getElementById('inp').value
  const res = await axios.post(`${API}/notes/create/`, { title })
  document.getElementById('inp').value = ''
  document.getElementById('list').innerHTML =
    `<p><b>${res.data.title}</b><br>🤖 ${res.data.ai_reply}</p>` +
    document.getElementById('list').innerHTML
  loadNotes()
}

async function loadNotes() {
  const res = await axios.get(`${API}/notes/`)
  document.getElementById('list').innerHTML =
    res.data.map(n => `<p><b>${n.title}</b><br>🤖 ${n.ai_reply}</p>`).join('')
}

loadNotes()


working api views.py

import os, requests
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Note
from .serializers import NoteSerializer

GEMMA_API_KEY = os.getenv('GEMMA_API_KEY')


def ask_gemma(prompt):
    res = requests.post(
        'https://generativelanguage.googleapis.com/v1beta/models/gemma-3-27b-it:generateContent',
        headers={'Content-Type': 'application/json'},
        params={'key': GEMMA_API_KEY},
        json={'contents': [{'parts': [{'text': prompt}]}]}
    )
    return res.json()['candidates'][0]['content']['parts'][0]['text']


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


now i need html and js file to be updated as per the working api's so that i can perform the crud and also it should look like simple chatgpt