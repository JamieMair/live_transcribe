# Live Transcribe


This repo is based on the work done [here](https://github.com/openai/whisper) by OpenAI, and a prototype built by Blake Mallory, hosted [here](https://github.com/mallorbc/whisper_mic).

This library runs a GUI app that should display what is said into the microphone. At the moment it is only a rough prototype, but may be of use to people who have trouble hearing, but are able to read the text.

[!Screenshot of App](screenshots/example.png)

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
```
2. Activate the environment, e.g. on Windows Command Prompt:
```bash
.venv\Scripts\activate.bat
```
3. Install the GPU version of pytorch, following [this guide](https://pytorch.org/get-started/locally/)
4. Install the packages that you need:
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
5. Run the app!
```bash
python -m live_transcribe.app
```

## Tips

The app is very hard to quit, but you can just kill the terminal that you launched it from. 

Hopefully this will be fixed in the future.