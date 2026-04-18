const API ="https://tinyproject-nm7k.onrender.com/notes/"

async function loadNotes() {
  try {
    const res = await axios.get(API)

    const chat = document.getElementById('chat')
    chat.innerHTML = ''

    res.data.reverse().forEach(n => {
      chat.innerHTML += `
        <div class="msg user"><b>You:</b> ${n.title}</div>
        <div class="msg"><b>AI:</b> ${n.ai_reply}</div>
      `
    })

  } catch (err) {
    console.error("Load error:", err)
  }
}

async function addNote() {
  const input = document.getElementById('inp')
  const chat = document.getElementById('chat')
  const title = input.value.trim()

  if (!title) return

  // Show user message instantly (ChatGPT feel)
  chat.innerHTML += `
    <div class="msg user"><b>You:</b> ${title}</div>
    <div class="msg"><b>AI:</b> ⏳ Thinking...</div>
  `

  input.value = ''

  try {
    await axios.post(API, { title })
    loadNotes()

  } catch (err) {
    console.error("POST error:", err)

    chat.innerHTML += `
      <div class="msg">⚠️ Failed to send. Check backend.</div>
    `
  }
}

// ENTER key support
document.getElementById("inp").addEventListener("keypress", function(e) {
  if (e.key === "Enter") {
    addNote()
  }
})

loadNotes()