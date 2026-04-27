# 🧠 LLM Smart Assistant (Level 2)

A desktop-based smart assistant built with Python that combines:
- 🤖 LLM-powered responses (Google Gemini)
- 🧮 Custom math tool
- 🎤 Voice input (speech recognition)
- 🔊 Text-to-speech output
- 💬 GUI chat interface (Tkinter)

---

## 🚀 Features

- **Natural Language Chat** using Gemini API
- **Math Tool Integration**
  - Handles simple arithmetic (2 numbers, 1 operation)
- **Voice Input**
  - Speak your queries using a microphone
- **Text-to-Speech**
  - Bot responses can be spoken aloud
- **Multi-intent Detection**
  - Prevents handling multiple questions at once
- **Conversation Logging**
  - Saves interactions to `interaction_logs.txt`

---

## 📂 Project Structure

```

.
├── chatbot_with_tool.py   # Main GUI chatbot application
├── calculator_tool.py     # Math processing module
├── interaction_logs.txt   # Saved chat history (auto-generated)

````

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/Bhanu2k04/Level2-chatbot.git
cd Level2-chatbot
````

### 2. Install dependencies

```bash
pip install google-generativeai pyttsx3 SpeechRecognition pyaudio
```

> ⚠️ On some systems, installing `pyaudio` may require additional setup.

---

## 🔑 Setup API Key

Set your Gemini API key as an environment variable:

### Linux / Mac

```bash
export GEMINI_API_KEY="your_api_key_here"
```

### Windows

```cmd
set GEMINI_API_KEY=your_api_key_here
```

---

## ▶️ Run the App

```bash
python chatbot_with_tool.py
```

---

## 🧪 Example Queries

* `What is 5 + 3?`
* `Multiply 10 and 4`
* `Who is the president of India?`
* Use 🎤 button to speak queries

---

## ⚠️ Limitations

* Only supports **simple math expressions**
* Cannot handle **multiple questions in one input**
* Requires internet for LLM responses

---

## 📌 Future Improvements

* Multi-intent handling
* Advanced math parsing
* Better UI/UX
* Offline LLM support

---

## 📜 License

MIT License

---


