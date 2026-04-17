from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=100)
    ai_reply = models.TextField(blank=True)    # ← Gemma's response stored here
    created_at = models.DateTimeField(auto_now_add=True)