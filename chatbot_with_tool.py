import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
import os
import calculator_tool
import re
import pyttsx3
import speech_recognition as sr
import threading

# ========== Setup Gemini API ==========
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or "API_KEY")
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
chat = model.start_chat(history=[])

# ========== Setup TTS ==========
engine = pyttsx3.init()
engine.setProperty('rate', 170)
speech_active = False
last_bot_response = ""

# ========== Intent Checkers ==========
def is_math_question(text):
    math_keywords = ['add', 'plus', 'sum', 'subtract', 'minus', 'multiply', 'times', 'divide', 'divided', '+', '-', '*', '/']
    return any(kw in text.lower() for kw in math_keywords)

def is_general_question(text):
    general_keywords = ['capital', 'president', 'country', 'leader', 'where', 'located']
    return any(kw in text.lower() for kw in general_keywords)

def is_multi_intent(text):
    parts = re.split(r'\band\b|,', text.lower())
    intent_count = sum(1 for part in parts if is_math_question(part) or is_general_question(part))
    return intent_count > 1

# ========== Get Response Logic ==========
def get_response(user_input):
    if is_multi_intent(user_input):
        return "⚠️ Sorry, I can't handle multiple questions in one message yet."
    elif is_math_question(user_input):
        return calculator_tool.calculate(user_input)
    else:
        try:
            response = chat.send_message(user_input)
            return response.text
        except Exception as e:
            return f"[Error] {e}"

# ========== Speak Toggle ==========
def toggle_speech():
    global speech_active
    if speech_active:
        engine.stop()
        speech_active = False
    else:
        speech_active = True
        threading.Thread(target=speak_response).start()

def speak_response():
    global speech_active
    if last_bot_response:
        engine.say(last_bot_response)
        engine.runAndWait()
    speech_active = False

# ========== Voice Input ==========
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        add_message("🎤 Listening...", "Bot")
        try:
            audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio)
            add_message(user_input, "You")
            entry.delete(0, tk.END)
            response = get_response(user_input)
            add_message(response, "Bot")
            global last_bot_response
            last_bot_response = response
            with open("interaction_logs.txt", "a", encoding="utf-8") as f:
                f.write(f"You: {user_input}\nBot: {response}\n\n")
        except sr.WaitTimeoutError:
            add_message("🛑 Timeout: No speech detected.", "Bot")
        except sr.UnknownValueError:
            add_message("🛑 Could not understand audio.", "Bot")
        except sr.RequestError as e:
            add_message(f"🛑 Speech service error: {e}", "Bot")

# ========== GUI Setup ==========
root = tk.Tk()
root.title("🧠 LLM Smart Assistant (Level 2)")
root.geometry("670x600")
root.configure(bg="#1e1e1e")

# Chat display
chat_frame = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#121212", fg="#f0f0f0", font=("Consolas", 12))
chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_frame.config(state=tk.DISABLED)

# Input row
input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(fill=tk.X, padx=10, pady=10)

entry = tk.Entry(input_frame, font=("Arial", 14), bg="#2e2e2e", fg="#ffffff", insertbackground="#ffffff")
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entry.bind("<Return>", lambda e: send_message())

send_btn = tk.Button(input_frame, text="Send", font=("Arial", 12), bg="#1E88E5", fg="white", command=lambda: send_message())
send_btn.pack(side=tk.LEFT)

speak_btn = tk.Button(input_frame, text="🔊 Speak", font=("Arial", 12), bg="#43A047", fg="white", command=toggle_speech)
speak_btn.pack(side=tk.LEFT, padx=(10, 0))

mic_btn = tk.Button(input_frame, text="🎤 Mic", font=("Arial", 12), bg="#FB8C00", fg="white", command=voice_input)
mic_btn.pack(side=tk.LEFT, padx=(10, 0))

# ========== Message Display ==========
def add_message(text, sender="Bot"):
    chat_frame.config(state=tk.NORMAL)
    if sender == "You":
        chat_frame.insert(tk.END, f"\n🧑 You:\n", "user")
    else:
        chat_frame.insert(tk.END, f"\n🤖 Bot:\n", "bot")
    chat_frame.insert(tk.END, f"{text}\n", "msg")
    chat_frame.see(tk.END)
    chat_frame.config(state=tk.DISABLED)

chat_frame.tag_config("user", foreground="#90CAF9", font=("Consolas", 11, "bold"))
chat_frame.tag_config("bot", foreground="#A5D6A7", font=("Consolas", 11, "bold"))
chat_frame.tag_config("msg", foreground="#E0E0E0")

# ========== Send Message ==========
def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return
    add_message(user_input, sender="You")
    entry.delete(0, tk.END)

    response = get_response(user_input)
    add_message(response, sender="Bot")
    global last_bot_response
    last_bot_response = response

    with open("interaction_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"You: {user_input}\nBot: {response}\n\n")

# ========== Run App ==========
root.mainloop()
