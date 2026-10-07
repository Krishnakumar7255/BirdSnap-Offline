# BirdSnap Offline 🐦

**BirdSnap Offline** is a Python-only bird-call identification app built for the **Hacktoberfest 2026 Open-Source AI Challenge — Week 1: Touch Grass**.

It uses a locally running BirdNET acoustic model through Python and provides a simple Streamlit interface for recording/uploading bird sounds, identifying them, and keeping local field notes.

## The idea

The app follows one simple loop:

**Go outside → Record → Identify → Learn → Put the screen down → Explore**

The screen is intentionally only a small part of the experience.

## Features

- 🎙️ Browser microphone recording
- 📁 Audio upload
- 🐦 Bird-call identification
- 🧠 Local BirdNET inference
- 🔒 No closed AI API
- 📓 Local observation history
- 📊 Confidence scores and alternative matches
- 🌿 Hacktoberfest “Touch Grass” focused UX
- 🐍 Entire project written in Python

## Tech stack

- Python
- Streamlit
- BirdNET
- Local ONNX inference

No React, Node.js, FastAPI, or separate frontend server is required.

## Project structure

```text
BirdSnap-Python/
├── app.py
├── birdnet_service.py
├── history.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    ├── history.json        # generated automatically
    └── temp/               # temporary recordings
```

## Requirements

- Python 3.10+
- pip
- A modern browser with microphone support
- Internet access may be needed the first time the BirdNET package/model assets are initialized; inference itself runs locally after the model is available.

## Windows setup

Open PowerShell or Command Prompt:

```bash
git clone YOUR_REPOSITORY_URL
cd BirdSnap-Python
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

Streamlit will open the application in your browser.

## Linux/macOS setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## First run

The first model initialization can take longer than later predictions.

For the best field result:

- record around 10–30 seconds;
- avoid strong wind;
- stay reasonably close to the bird;
- avoid talking over the recording;
- try multiple recordings if the confidence is low.

## Why open innovation matters

A conventional closed AI API would require sending the audio to a remote provider.

BirdSnap instead uses a local open AI model.

That gives the project:

### Privacy

A bird recording does not have to leave the machine running the app.

### Local inference

Once model assets are available locally, the prediction itself does not require a remote AI API.

### Replaceability

The AI layer is isolated inside `birdnet_service.py`. Another compatible open model can be introduced without rebuilding the UI.

### Experimentation

Because the inference stack is local and accessible, developers can experiment with preprocessing, thresholds, model versions, and field workflows.

## Hacktoberfest: Touch Grass

BirdSnap is not designed to keep people staring at an AI chat window.

The app's ideal session is:

```text
10–30 seconds of recording
        ↓
A few seconds of identification
        ↓
Learn the bird
        ↓
PHONE DOWN
        ↓
Keep exploring 🌳
```

The AI is the tool that encourages the outdoor activity, not the destination.

## Suggested demo

For the Hacktoberfest submission:

1. Take your laptop/phone outside.
2. Find a bird.
3. Record its call.
4. Run BirdSnap.
5. Show the predicted species and confidence.
6. Explain that inference happens locally.
7. Put the device down.
8. Find the bird again if possible.
9. Write about what happened during the field test.

A real outdoor demo will make the “Touch Grass” connection much stronger.

## Architecture

```text
              ┌─────────────────────┐
              │     Streamlit UI    │
              │  record / upload    │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ birdnet_service.py │
              │ model adapter      │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   BirdNET 3.0       │
              │  local inference    │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ bird + confidence   │
              │ + field observation │
              └─────────────────────┘
```

## License

The application code in this repository is intended to be MIT licensed.

**Important:** BirdNET model files and related assets have their own licensing terms. The BirdNET Python package documentation states that its models are licensed under **CC BY-NC-SA 4.0**. Review the applicable BirdNET/model terms before commercial use.

This project is independent and is not an official Cornell Lab product.

## Hacktoberfest submission checklist

- [ ] Push the project to GitHub
- [ ] Add screenshots
- [ ] Record a short outdoor demo
- [ ] Mention the actual model used
- [ ] Explain why local/open AI mattered
- [ ] Describe your field test
- [ ] Link the GitHub repository in your DEV post
- [ ] Add applicable partner categories
- [ ] Include an agent session if you use DevRelay

## Future improvements

- GPS-based species filtering
- Bird observation map
- PWA/mobile packaging
- Species information cards
- CSV export
- Better audio preprocessing
- Offline model packaging
- Daily outdoor challenges
- Personal birding streaks
