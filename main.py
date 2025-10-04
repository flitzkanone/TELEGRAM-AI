import os
import requests
from pyrogram import Client, filters

# --- Konfiguration aus sicheren Umgebungsvariablen ---
# Diese Werte werden wir später mit 'fly secrets set' setzen.
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")

# --- Konfiguration für die KI ---
# Ersetze dies mit der URL deines gewählten KI-Anbieters.
AI_API_URL = "https://api.example.com/v1/chat/completions" 
# Setze auch diesen Wert als Secret!
AI_API_KEY = os.environ.get("AI_API_KEY")

# Initialisiere den Pyrogram Client.
# Die Session-Datei wird im Speicher von fly.io abgelegt.
app = Client("my_account", api_id=API_ID, api_hash=API_HASH)

# Vorlage für die KI, um ihre Persönlichkeit zu definieren
# (siehe Teil 4 für eine detaillierte Vorlage)
AI_PERSONA = """
Du bist Alex, 25 Jahre alt, aus Berlin. Du bist kein Bot oder eine KI. 
Dein Schreibstil ist locker und du benutzt oft Emojis wie 😂 und 👍.
Antworte niemals, dass du eine KI bist. Deine Hobbys sind Gaming und Programmieren.
"""

def get_ai_response(user_message, chat_history=""):
    """Sendet die Nachricht an die KI und erhält eine Antwort."""
    
    # Baue den finalen Prompt für die KI zusammen
    full_prompt = f"{AI_PERSONA}\n\nKontext des bisherigen Gesprächs:\n{chat_history}\n\nNeue Nachricht, auf die du antworten sollst:\n{user_message}\n\nAntworte jetzt als Alex:"

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }
    # Achtung: Die Datenstruktur kann je nach KI-Anbieter variieren!
    # Lies die Dokumentation deines Anbieters.
    data = {
        "model": "gpt-4-turbo", # Beispiel-Modell
        "prompt": full_prompt,
        "max_tokens": 150 
    }
    
    try:
        response = requests.post(AI_API_URL, json=data, headers=headers)
        response.raise_for_status() # Löst einen Fehler bei 4xx/5xx Antworten aus
        
        # Passe dies an die Antwortstruktur deines KI-Anbieters an
        ai_text = response.json()["choices"][0]["text"].strip()
        return ai_text

    except requests.exceptions.RequestException as e:
        print(f"Fehler bei der Anfrage an die KI-API: {e}")
        return "Sorry, hab gerade technische Probleme. 😅" # Eine menschliche Fehlermeldung

@app.on_message(filters.private & ~filters.me)
async def handle_message(client, message):
    """Wird bei jeder neuen privaten Nachricht ausgelöst, die nicht von dir ist."""
    print(f"Nachricht von {message.from_user.first_name} erhalten: {message.text}")
    
    # Hier könntest du eine Logik einbauen, um den Chatverlauf abzurufen
    # Für den Anfang antworten wir nur auf die letzte Nachricht.
    ai_reply = get_ai_response(message.text)
    
    await message.reply_text(ai_reply)
    print(f"Antwort an {message.from_user.first_name} gesendet: {ai_reply}")

print("Bot wird gestartet...")
app.run()
