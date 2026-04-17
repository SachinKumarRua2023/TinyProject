# 🚀 Tiny Full Stack Project — Django + HTML + React Native
### By a 28-year-old Full Stack AI/ML Trainer — Keep it real, ship it fast

---

## 🧠 What Are We Building?

A **Notes App** with AI (Gemma) — create notes, list notes, AI replies.

```
User → HTML Page (Web)        ─┐
                                ├──→ Django REST API → SQLite DB
User → React Native (Android) ─┘         ↕
                                    Gemma 4 AI API
```

---

## 🗂️ Final File Structure

```
tiny-project/
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env                      ← secret keys (never push to git!)
│   ├── render.yaml               ← Render deployment config
│   ├── backend/
│   │   ├── settings.py
│   │   └── urls.py
│   └── notes/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py              ← Gemma AI call is here
│       └── urls.py
│
├── frontend-web/
│   ├── index.html
│   └── app.js                    ← axios + Gemma call
│   |__.gitignore /.env 
├── frontend-app/
│   ├── App.js
│   ├── .env                      ← EXPO_PUBLIC_* variables
│   ├── eas.json
│   └── package.json
│
└── .github/
    └── workflows/
        ├── backend-deploy.yml    ← CI/CD for backend
        └── app-build.yml         ← CI/CD for Android
```

> **Total files: ~16. Still tiny.**

---

## 🔧 PART 1 — Django Backend

### How Django REST Works

```
HTTP Request
     ↓
  urls.py       ← which door to enter
     ↓
  views.py      ← what happens inside
     ↓
  models.py     ← talks to DB
     ↓
  serializers   ← converts Python → JSON
     ↓
HTTP Response (JSON)
```

### Step 1 — Setup

```bash
mkdir tiny-project ; cd tiny-project
mkdir backend ; cd backend

python -m venv venv
venv\Scripts\activate

pip install django djangorestframework django-cors-headers python-dotenv requests
pip freeze > requirements.txt

django-admin startproject backend .
python manage.py startapp notes
```

---

### Step 2 — `.env` file (in backend/)

```env
GEMMA_API_KEY=your_gemma_api_key_here
DEBUG=True
```

> 🧠 **What is .env?**
> It's a secret file. Like a locker. You store passwords/API keys here.
> Your code reads from it. You NEVER push this to GitHub.
> Add `.env` to `.gitignore` — always!

---

### Step 3 — `backend/settings.py`

```python
import os
from dotenv import load_dotenv
load_dotenv()

DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
    'notes',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
GEMMA_API_KEY = os.getenv('GEMMA_API_KEY')
```

---

### Step 4 — `notes/models.py`

```python
from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=100)
    ai_reply = models.TextField(blank=True)    # ← Gemma's response stored here
    created_at = models.DateTimeField(auto_now_add=True)
```

---

### Step 5 — `notes/serializers.py`

```python
from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
```

---

### Step 6 — `notes/views.py` (with Gemma AI)

```python
import os, requests
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Note
from .serializers import NoteSerializer

GEMMA_API_KEY = os.getenv('GEMMA_API_KEY')

def ask_gemma(prompt):
    # Gemma 4 via Google AI Studio (OpenAI-compatible endpoint)
    res = requests.post(
        'https://generativelanguage.googleapis.com/v1beta/models/gemma-3-27b-it:generateContent',
        headers={'Content-Type': 'application/json'},
        params={'key': GEMMA_API_KEY},
        json={'contents': [{'parts': [{'text': prompt}]}]}
    )
    return res.json()['candidates'][0]['content']['parts'][0]['text']

class NoteList(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class NoteCreate(APIView):
    def post(self, request):
        title = request.data.get('title', '')
        ai_reply = ask_gemma(f'Give a one-line tip about: {title}')
        note = Note.objects.create(title=title, ai_reply=ai_reply)
        return Response(NoteSerializer(note).data)
```

> 🧠 **Visual — What happens when you POST a note:**
> ```
> You type "Buy milk"
>       ↓
> Django gets it → asks Gemma "Give a tip about: Buy milk"
>       ↓
> Gemma replies: "Buy organic milk for better nutrition!"
>       ↓
> Django saves note + AI reply → sends back JSON
>       ↓
> You see both on screen
> ```

---

### Step 7 — `notes/urls.py`

```python
from django.urls import path
from .views import NoteList, NoteCreate

urlpatterns = [
    path('notes/', NoteList.as_view()),
    path('notes/create/', NoteCreate.as_view()),
]
```

---

### Step 8 — `backend/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('notes.urls')),
]
```

---

### Step 9 — Run

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Test: `http://127.0.0.1:8000/api/notes/create/` → POST `{"title": "Buy milk"}`

---

## 🌐 PART 2 — Web Frontend

### `frontend-web/index.html`

```html
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
</html>
```

### `frontend-web/app.js`

```js
// In production, replace with your Render URL
const API = 'https://your-backend.onrender.com/api'

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
```

---

## 📱 PART 3 — React Native App

### `frontend-app/.env`

```env
EXPO_PUBLIC_API_URL=https://your-backend.onrender.com/api
```

> 🧠 In Expo, env variables MUST start with `EXPO_PUBLIC_` to be accessible in JS code.

### `frontend-app/App.js`

```js
import { useState, useEffect } from 'react'
import { View, Text, TextInput, Button, FlatList, ScrollView } from 'react-native'
import axios from 'axios'

const API = process.env.EXPO_PUBLIC_API_URL || 'http://192.168.1.5:8000/api'

export default function App() {
  const [notes, setNotes] = useState([])
  const [title, setTitle] = useState('')

  const load = async () => {
    const res = await axios.get(`${API}/notes/`)
    setNotes(res.data)
  }

  const add = async () => {
    await axios.post(`${API}/notes/create/`, { title })
    setTitle('')
    load()
  }

  useEffect(() => { load() }, [])

  return (
    <ScrollView style={{ padding: 40 }}>
      <Text style={{ fontSize: 22 }}>📝 Notes + 🤖 Gemma</Text>
      <TextInput value={title} onChangeText={setTitle} placeholder="Note title"
        style={{ borderWidth: 1, padding: 8, marginVertical: 10 }} />
      <Button title="Add Note" onPress={add} />
      {notes.map(n => (
        <View key={n.id} style={{ marginTop: 10 }}>
          <Text style={{ fontWeight: 'bold' }}>{n.title}</Text>
          <Text style={{ color: 'gray' }}>🤖 {n.ai_reply}</Text>
        </View>
      ))}
    </ScrollView>
  )
}
```

---

## 🚀 PART 4 — Full Deployment (Step by Step)

### 🗺️ Deployment Big Picture

```
You write code on laptop
        ↓
   git push → GitHub repo
        ↓
   ┌────────────────────────────────────┐
   │           GitHub Actions           │
   │  (CI/CD — auto runs on every push) │
   └────┬──────────────┬────────────────┘
        ↓              ↓
   Render.com     EAS Build
   (Backend)      (Android APK)
        ↓              ↓
   Live API      APK Download Link
        ↓
   Vercel (Web)
   (just push frontend-web folder)
```

---

### 🟢 Deploy Backend → Render.com

**Step 1 — Add to `requirements.txt`:**
```
gunicorn
whitenoise
python-dotenv
requests
```

**Step 2 — Create `render.yaml` in backend/:**
```yaml
services:
  - type: web
    name: notes-api
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
    startCommand: gunicorn backend.wsgi:application
    envVars:
      - key: GEMMA_API_KEY
        sync: false          # you paste this manually on Render dashboard
      - key: DEBUG
        value: False
```

**Step 3 — Add env variable on Render Dashboard:**
- Go to render.com → your service → **Environment**
- Add `GEMMA_API_KEY` = your actual key
- Add `SECRET_KEY` = any long random string

**Step 4 — Push to GitHub:**
```bash
cd backend
git init
git add .
git commit -m "initial backend"
git remote add origin https://github.com/yourusername/tiny-project-backend.git
git push -u origin main
```

**Step 5 — Connect on Render:**
- render.com → New Web Service → Connect GitHub → select your repo → Deploy

Your API is live: `https://notes-api.onrender.com/api/notes/` ✅

---

### 🔵 Deploy Web Frontend → Vercel

**Option A — Drag & Drop (easiest):**
- Go to vercel.com → New Project → drag `frontend-web` folder → Deploy

**Option B — CLI:**
```bash
npm i -g vercel
cd frontend-web
vercel
```

> Before deploying, update `app.js`:
> Change `localhost:8000` → `https://notes-api.onrender.com`

Your web app is live: `https://your-app.vercel.app` ✅

---

### 🟡 Deploy Android App → EAS

**Step 1 — Setup EAS:**
```bash
cd frontend-app
npm install -g eas-cli
eas login
eas init
```

**Step 2 — `eas.json`:**
```json
{
  "cli": { "version": ">= 18.5.0" },
  "build": {
    "preview": {
      "distribution": "internal",
      "android": { "buildType": "apk" },
      "channel": "preview"
    },
    "production": {
      "autoIncrement": true,
      "channel": "production"
    }
  }
}
```

**Step 3 — Add env variable for EAS:**
```bash
eas secret:create --scope project --name EXPO_PUBLIC_API_URL --value https://notes-api.onrender.com/api
```

**Step 4 — Build:**
```bash
eas build --platform android --profile preview
```

Share the APK link. Done. ✅

---

## 🔁 PART 5 — CI/CD Pipeline (Auto Deploy on Every Push)

### What is CI/CD?

```
CI = Continuous Integration   → auto test your code on every push
CD = Continuous Deployment    → auto deploy on every push

Without CI/CD:               With CI/CD:
  write code                   write code
  → manually test               → git push
  → manually build              → GitHub sees it
  → manually deploy             → auto test → auto deploy
  (boring + error-prone)        (you sleep, it deploys) 😎
```

---

### CI/CD for Backend → `.github/workflows/backend-deploy.yml`

Create this file in your repo:

```yaml
name: Deploy Backend to Render

on:
  push:
    branches: [main]
    paths: ['backend/**']     # only runs when backend files change

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Trigger Render Deploy
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

> 🧠 **Render Deploy Hook** = a secret URL Render gives you.
> When GitHub hits that URL → Render auto-deploys.
> Get it from: Render Dashboard → your service → Settings → Deploy Hook

**Add to GitHub Secrets:**
- Your repo → Settings → Secrets → Actions
- Add `RENDER_DEPLOY_HOOK` = the URL from Render

Now every `git push` to main → backend auto-deploys. ✅

---

### CI/CD for Android App → `.github/workflows/app-build.yml`

```yaml
name: EAS Build on Push

on:
  push:
    branches: [main]
    paths: ['frontend-app/**']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install deps
        run: cd frontend-app && npm install

      - name: Build APK
        run: cd frontend-app && eas build --platform android --profile preview --non-interactive
        env:
          EXPO_TOKEN: ${{ secrets.EXPO_TOKEN }}
```

**Add GitHub Secret:**
- Get token: `eas whoami` → expo.dev → account → access tokens
- GitHub → your repo → Settings → Secrets → Add `EXPO_TOKEN`

Now every push to `frontend-app/` → new APK auto-builds on EAS. ✅

---

## 🤔 PART 6 — Git vs EAS — Beginner Questions Answered

### Q1: Are Git and EAS the same thing?

**NO. Completely different tools. Same concept (version control) but different purpose.**

```
GIT                              EAS (Expo Application Services)
────────────────────────         ────────────────────────────────
Saves your CODE history          Builds & deploys your APP
Works for any project            Works only for Expo/React Native
Lives on GitHub/GitLab           Lives on expo.dev
Free, open source                Has free + paid tier
You control it                   Expo's cloud servers do the work
```

> 🧠 **Real life analogy:**
> Git = Google Docs history (tracks changes to your files)
> EAS = Factory (takes your files and builds an APK/IPA)

---

### Q2: When I push to GitHub, does EAS automatically build?

**Not by default. You connect them via CI/CD (GitHub Actions).**

```
Without CI/CD:                  With CI/CD (GitHub Actions):
  git push                        git push
  (nothing happens to EAS)          ↓
  you manually run:               GitHub Actions runs
  eas build ...                   eas build ... automatically
```

---

### Q3: What is a "channel" in EAS?

```
channel = which version of the app users get OTA updates from

preview  → your testers get this
production → your real users get this

Like branches in Git, but for your deployed app.
```

---

### Q4: What is `eas update` vs `eas build`?

```
eas build                        eas update
─────────────────────            ─────────────────────────
Full APK rebuild                 Just update JS code (OTA)
Takes 10-20 mins                 Takes 30 seconds
Users need to download           Users get it on app restart
Use when: new native package,    Use when: bug fix, UI change,
permissions change               logic change, API URL change
```

---

### Q5: Does Git track my `.env` file?

**It should NOT. Here's why:**

```
.env file has your secret keys
       ↓
If you push to GitHub (public repo)
       ↓
Anyone can see your GEMMA_API_KEY
       ↓
They use your key → you get charged 💸
```

**Always add `.env` to `.gitignore`:**
```
# .gitignore
.env
node_modules
__pycache__
venv
*.pyc
db.sqlite3
```

---

### Q6: How does Render/Vercel know my secret keys if I don't push `.env`?

```
You add them manually on the platform dashboard:

Render Dashboard → Environment Variables → Add Key/Value
Vercel Dashboard → Settings → Environment Variables → Add Key/Value
EAS              → eas secret:create --name KEY --value value
GitHub Actions   → repo Settings → Secrets → Add secret
```

> 🧠 **Visual:**
> ```
> Your laptop           Cloud Platform
>    .env          →    (you type it manually in dashboard)
>  [never pushed]        ↓
>                    Server reads it as environment variable
>                    Same as your .env, but safe!
> ```

---

### Q7: What is the difference between `git push` and `eas build`?

```
git push  → uploads your SOURCE CODE to GitHub
            "Here's my recipe"

eas build → takes your source code, compiles it into an APK
            "Cook the recipe, give me the food (APK)"
```

---

### Q8: Full Git + EAS Workflow for a Beginner

```
Day 1: Setup
  git init → git remote add origin → first git push

Daily work:
  write code
    ↓
  git add . → git commit -m "what I changed" → git push
    ↓
  (if CI/CD set up) → auto deploys backend + triggers EAS build

When you fix a bug (JS only):
  git push → eas update --branch preview (OTA, no reinstall)

When you add camera/maps/new package:
  git push → eas build (full APK, users download once)
```

---

## 🔐 PART 7 — Gemma API Key — Where & How

### Get Gemma API Key
1. Go to → `aistudio.google.com`
2. Create API Key
3. Copy it

### Where to put it

| Place | How |
|-------|-----|
| Local backend | `.env` file → `GEMMA_API_KEY=xxx` |
| Render (backend) | Dashboard → Environment Variables |
| Expo app | `eas secret:create` or `.env` with `EXPO_PUBLIC_` prefix |
| GitHub Actions | repo → Settings → Secrets |

> 🧠 **The key never lives in your code. Only in environment. Always.**

---

## 📋 Master Command Cheat Sheet

```bash
# ── GIT ───────────────────────────────────────────────
git init                              # start tracking
git add .                             # stage all changes
git commit -m "your message"          # save snapshot
git push origin main                  # upload to GitHub
git pull                              # download latest

# ── BACKEND ───────────────────────────────────────────
venv\Scripts\activate                 # activate virtualenv
python manage.py makemigrations       # detect model changes
python manage.py migrate              # apply to DB
python manage.py runserver            # run locally

# ── FRONTEND WEB ──────────────────────────────────────
# open index.html in browser          # no server needed locally
vercel                                # deploy to Vercel

# ── FRONTEND APP ──────────────────────────────────────
npx expo start                        # run locally
eas build --platform android --profile preview   # build APK
eas update --branch preview --message "fix"      # OTA update
eas secret:create --name KEY --value val         # add secret

# ── CI/CD ─────────────────────────────────────────────
# just git push → GitHub Actions handles the rest
```

---

## 🧠 Full System Visual — Everything Together

```
┌─────────────────────────────────────────────────────────┐
│                   YOUR LAPTOP                           │
│  VS Code → write code → git push                        │
└──────────────────────┬──────────────────────────────────┘
                       ↓
             ┌─────────────────┐
             │    GitHub Repo  │
             │  (your code)    │
             └────────┬────────┘
                      ↓ GitHub Actions (CI/CD)
         ┌────────────┴─────────────┐
         ↓                          ↓
  ┌─────────────┐           ┌──────────────┐
  │  Render.com │           │  EAS (Expo)  │
  │  Django API │           │  Android APK │
  │  + SQLite   │           │  Build       │
  │  + Gemma    │           └──────┬───────┘
  └──────┬──────┘                  ↓
         ↓                   APK Download Link
  Live API URL                     ↓
         ↓               Users install on phone
  ┌──────┴──────┐
  ↓             ↓
Vercel       Phone App
(HTML page)  (React Native)
  ↓             ↓
Both call API, show notes + Gemma AI reply
```

---

## ❓ More Beginner Questions

**Q: My app is installed on phone. I fixed a bug. Do users reinstall?**
> No! Run `eas update --branch preview`. App updates silently on restart.

**Q: Render free tier sleeps after 15 min. API is slow on first call?**
> Yes. Free tier spins down. Solution: use a cron job to ping it every 10 min,
> or upgrade to paid ($7/month).

**Q: Can I use the same GitHub repo for backend + frontend?**
> Yes! It's called a monorepo. Use `paths:` in GitHub Actions to only trigger
> the right job when the right folder changes.

**Q: Should I use PostgreSQL instead of SQLite on Render?**
> For learning: SQLite is fine.
> For real users: switch to PostgreSQL. Render gives free PostgreSQL too.
> Just change 2 lines in `settings.py`.

**Q: What if Gemma API fails?**
> Wrap `ask_gemma()` in try/except and return a default reply. Never crash
> your API because of an external service.

---

> 💬 **Trainer's Note:** You now understand the FULL cycle.
> Code → Git → CI/CD → Deploy → Users → Update → Repeat.
> This is literally what every startup does at scale. You just did it with 16 files. 🔥
