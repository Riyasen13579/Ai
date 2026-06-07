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

```bash
git clone https://github.com/Riyasen13579/Ai.git
cd Ai
```

Install the required libraries:

```bash
pip install SpeechRecognition pyttsx3 pyaudio
```

> If you're on Windows and `pyaudio` fails, install it manually using a `.whl` file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).
>
> On macOS, run `brew install portaudio` first, then `pip install pyaudio`.

### Run the assistant

```bash
cd va
python main.py
```

## Usage

Once running, speak a command into your microphone. Some example commands:

- "Hello"
- "Open YouTube"
- "Open Google"
- "What is your name?"
- "Exit"

## Project Structure

```
Ai/
├── va/
│   └── main.py      # main script
├── .gitignore
└── README.md
```

## Troubleshooting

**Microphone not working** — Make sure it's connected and set as the default input device.

**Speech not recognized** — The default setup uses Google's Speech API, so an internet connection is required.

**pyaudio install error on Linux** — Run `sudo apt install portaudio19-dev` first.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

## License

[MIT](LICENSE)

