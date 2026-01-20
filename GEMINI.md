# Intelligent Stem Separator

This project is a web-based application for separating audio tracks into individual stems (vocals, accompaniment, etc.) using AI. It is designed to be portable and efficient, running on platforms like Raspberry Pi and Android (via Termux).

## Project Overview

*   **Type:** Full-stack Web Application (Python Backend + Static Frontend)
*   **Core Technology:** Python 3.9+, FastAPI, Demucs (AI Model), FFmpeg
*   **Goal:** Provide a simple "drag & drop" interface for audio stem separation.

## Architecture

The application follows a Client-Server model:

1.  **Frontend:** A lightweight, static HTML/JS interface (PWA-ready) served by the backend. It handles file uploads and status polling.
2.  **Backend:** A FastAPI server (`_dev/app.py`) that manages uploads, queues tasks, and serves files.
3.  **Core Engine:** A Python wrapper (`_dev/engine.py`) around the **Demucs** AI model (running via CLI) to perform the heavy audio processing.
4.  **Storage:**
    *   `inputs/`: Stores uploaded audio files.
    *   `outputs/`: Stores the separated stems (organized by song name).

## Directory Structure

```text
STEM_SEPARATOR/
├── _dev/                   # Development Source Code
│   ├── app.py              # Main FastAPI application entry point
│   ├── engine.py           # Wrapper for Demucs logic
│   ├── requirements.txt    # Python dependencies
│   ├── venv/               # Virtual Environment
│   └── static/             # Frontend Assets
│       ├── index.html
│       ├── style.css
│       └── app.js
├── inputs/                 # Uploaded audio files
├── outputs/                # Processed stems
├── _arch/                  # Archives
├── _ver/                   # Version history
└── BLUEPRINT_*.md          # Architectural documentation
```

## Getting Started

### Prerequisites

*   **Python 3.9+**
*   **FFmpeg** (System dependency: `sudo apt install ffmpeg`)

### Setup

1.  Navigate to the development directory:
    ```bash
    cd _dev
    ```

2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: This project uses `demucs` instead of `spleeter` due to Python version compatibility.*

### Running the Application

1.  Start the FastAPI server:
    ```bash
    python app.py
    ```
    *Or run in background:* `nohup python app.py > app.log 2>&1 &`

2.  Access the Web GUI:
    Open your browser and go to `http://localhost:8000` (or your device's IP address).

## Development Conventions

*   **Environment:** Always work within the `_dev` directory and use the virtual environment (`venv`).
*   **Engine Logic:** The `StemEngine` class in `engine.py` handles the interaction with the AI model. It currently abstracts the `demucs` CLI command.
*   **Async Processing:** The API uses FastAPI's `BackgroundTasks` to prevent the UI from freezing during the intensive separation process.
*   **Output Format:** The engine automatically renames Demucs' `no_vocals` output to `accompaniment` to maintain consistency with Spleeter's conventions.
