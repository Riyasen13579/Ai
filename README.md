<<<<<<< HEAD
# AI Voice Assistant

A simple voice assistant built with Python. It listens to your voice commands, recognizes speech, and performs tasks like opening websites or giving predefined responses.

## About

This project uses popular Python libraries to handle voice input and output:

- **SpeechRecognition** – converts your voice to text
- **pyttsx3** – converts text back to speech (works offline)
- **pyaudio** – captures microphone input

## Getting Started

### Prerequisites

Make sure you have Python 3.8 or above installed.

### Installation

Clone the repository:
=======
# 🎙️ AI Voice Assistant

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

A simple yet powerful voice assistant built with Python. It listens to your voice commands, converts speech to text, and performs tasks like opening websites or responding with predefined messages — all hands-free.

---

## ✨ Features

- 🎤 **Voice Recognition** — Converts spoken commands to text using `SpeechRecognition`
- 🔊 **Text-to-Speech** — Responds back with a natural voice using `pyttsx3`
- 🌐 **Open Websites** — Launch URLs via voice command
- 💬 **Predefined Responses** — Handles common queries with instant replies
- ⚡ **Lightweight & Fast** — Minimal dependencies, runs on any Python 3.8+ environment

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| `SpeechRecognition` | Converts microphone input to text |
| `pyttsx3` | Text-to-speech engine (offline) |
| `pyaudio` | Microphone access and audio stream |

---

## 📦 Installation

### 1. Clone the repository
>>>>>>> 78341f5e96cdbefd632b20717ec20e67dba8e9a6

```bash
git clone https://github.com/Riyasen13579/Ai.git
cd Ai
```

<<<<<<< HEAD
Install the required libraries:
=======
### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
>>>>>>> 78341f5e96cdbefd632b20717ec20e67dba8e9a6

```bash
pip install SpeechRecognition pyttsx3 pyaudio
```

<<<<<<< HEAD
> If you're on Windows and `pyaudio` fails, install it manually using a `.whl` file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).
>
> On macOS, run `brew install portaudio` first, then `pip install pyaudio`.

### Run the assistant
=======
> **Note for Windows users:** If `pyaudio` fails to install, download the appropriate `.whl` file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install it manually:
> ```bash
> pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl
> ```

---

## 🚀 Usage
>>>>>>> 78341f5e96cdbefd632b20717ec20e67dba8e9a6

```bash
cd va
python main.py
```

<<<<<<< HEAD
## Usage

Once running, speak a command into your microphone. Some example commands:

- "Hello"
- "Open YouTube"
- "Open Google"
- "What is your name?"
- "Exit"

## Project Structure
=======
The assistant will start listening. Try these voice commands:

| Voice Command | Action |
|---|---|
| `"Hello"` | Greets you back |
| `"Open YouTube"` | Opens YouTube in browser |
| `"Open Google"` | Opens Google in browser |
| `"What is your name?"` | Assistant introduces itself |
| `"Exit"` or `"Stop"` | Shuts down the assistant |

---

## 📁 Project Structure
>>>>>>> 78341f5e96cdbefd632b20717ec20e67dba8e9a6

```
Ai/
├── va/
<<<<<<< HEAD
│   └── main.py      # main script
=======
│   └── main.py          # Entry point — runs the voice assistant
>>>>>>> 78341f5e96cdbefd632b20717ec20e67dba8e9a6
├── .gitignore
└── README.md
```

<<<<<<< HEAD
## Troubleshooting

**Microphone not working** — Make sure it's connected and set as the default input device.

**Speech not recognized** — The default setup uses Google's Speech API, so an internet connection is required.

**pyaudio install error on Linux** — Run `sudo apt install portaudio19-dev` first.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

## License

[MIT](LICENSE)

=======
---

## ⚙️ Configuration

You can customize the assistant's behaviour directly in `main.py`:

- **Change voice speed** — modify `engine.setProperty('rate', 150)`
- **Switch voice (male/female)** — change the voice ID in `engine.setProperty('voice', voices[0].id)`
- **Add new commands** — extend the `if/elif` block that matches recognized text

---

## 🐛 Troubleshooting

**Microphone not detected**
- Make sure your microphone is connected and set as the default input device.
- On Linux, you may need to install `portaudio`: `sudo apt install portaudio19-dev`

**`pyaudio` install error**
- On macOS: `brew install portaudio && pip install pyaudio`
- On Windows: use the pre-built `.whl` file (see Installation section)

**No speech recognized / constant errors**
- Check your internet connection — Google Speech API requires it by default.
- Try increasing the `pause_threshold` in the recognizer settings.

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/my-feature`
3. Make your changes and commit: `git commit -m "Add my feature"`
4. Push to your branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) by Anthony Zhang
- [pyttsx3](https://pypi.org/project/pyttsx3/) for offline TTS
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) for audio I/O
>>>>>>> 78341f5e96cdbefd632b20717ec20e67dba8e9a6
