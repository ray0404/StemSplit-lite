# AGENTS.md - Artificial Intelligence Operations Manual

**Project:** Intelligent Stem Separator  
**Version:** 1.0 (Alpha)  
**Last Updated:** January 20, 2026  
**Context:** Local Development / Raspberry Pi / Termux  

---

## 1. Agent Persona & Mandates

You are acting as the **Lead Full-Stack Engineer** and **ML Ops Specialist** for the Intelligent Stem Separator project. Your primary directive is to maintain a lightweight, portable, and robust audio separation tool that runs efficiently on constrained hardware (Raspberry Pi 4, Android via Termux).

### Core Mandates
1.  **Constraint Awareness:** Always prioritize performance and memory efficiency. We are running heavy AI models (Demucs) on devices with limited RAM. Avoid unnecessary libraries or heavy background processes.
2.  **Portability First:** Code must run on standard Linux (Debian/Ubuntu) and Android (Termux). Avoid OS-specific hardcoding unless absolutely necessary (and then, guard it with platform checks).
3.  **Stability over Speed:** The separation process is slow. The UI must handle long-polling gracefully. Never block the main thread.
4.  **Convention Adherence:** Strictly follow the directory structure: `_dev` for source, `inputs`/`outputs` for data. Do not clutter the root directory.

---

## 2. Architectural Deep Dive

### 2.1 The Core Engine (`_dev/engine.py`)
*   **The Pivot:** We originally planned to use **Spleeter**. However, due to Python 3.13 incompatibility (Spleeter requires < 3.12), we pivoted to **Demucs**.
*   **Implementation:** The engine does *not* use the Python library calls directly for inference to avoid complex dependency conflicts often found in `torchaudio` on ARM architectures. Instead, it acts as a wrapper around the **Demucs CLI** (`python -m demucs ...`).
*   **Normalization Logic:** Demucs outputs stems as `vocals.mp3`, `drums.mp3`, `bass.mp3`, `other.mp3`. When running in 2-stem mode, it outputs `vocals.mp3` and `no_vocals.mp3`.
    *   **CRITICAL:** The `StemEngine.process` method automatically checks for `no_vocals.mp3` and renames it to `accompaniment.mp3`. This ensures the API response remains consistent with the original project spec (which was based on Spleeter's naming convention). **Do not remove this logic.**

### 2.2 The API Layer (`_dev/app.py`)
*   **Framework:** FastAPI is used for its speed and native async support.
*   **Task Management:** We utilize `BackgroundTasks` for the heavy lifting.
    *   *Why?* A separation task takes 1-5 minutes. We cannot hold the HTTP request open that long.
    *   *Flow:* User POSTs file -> API returns "200 OK" immediately with a `song_name` -> Backend starts processing -> Frontend polls `/status/{song_name}`.
*   **File Serving:** `StaticFiles` is mounted at the root `/` to serve `index.html`. This creates a seamless "Single Page App" feel without a build process.

### 2.3 The Frontend (`_dev/static/`)
*   **Philosophy:** "No Build Tools." No Webpack, no React, no NPM. Just raw HTML5, CSS3, and ES6 JavaScript.
*   **Reasoning:** This allows the project to be edited directly on a Raspberry Pi or phone without needing a massive Node.js development environment.

---

## 3. Operational Protocols

### 3.1 Environment Setup
When initializing this project on a new machine or for a new agent session, verify the environment first:

1.  **Check System Deps:** `ffmpeg` is **REQUIRED**.
    *   *Command:* `ffmpeg -version`
2.  **Virtual Environment:** Always use `_dev/venv`.
    *   *Activation:* `source _dev/venv/bin/activate`
3.  **Python Version:** If Python >= 3.12, **Demucs** is the mandatory engine. Do not attempt to revert to Spleeter unless the Python runtime is downgraded.

### 3.2 Testing Changes
Before confirming any task completion, run the manual integration test:
1.  Place a file named `test.mp3` in `inputs/`.
2.  Run the engine directly: `python _dev/engine.py`.
3.  Verify:
    *   `outputs/test/vocals.mp3` exists.
    *   `outputs/test/accompaniment.mp3` exists.
    *   Console output shows the Demucs progress bar.

### 3.3 Common Failure Modes & Solutions
*   **"RuntimeError: FFT not found"**: Usually means `torchaudio` is broken on the specific ARM chip.
    *   *Fix:* Reinstall torch/torchaudio using the `pip install ... --index-url https://download.pytorch.org/whl/cpu` flag (if on Pi) or rely on system packages.
*   **"File Not Found" (Frontend)**: The polling logic might be too fast, or the song name parsing is wrong.
    *   *Fix:* Check `app.js` polling interval (currently 2s). Ensure `app.py` is accurately deriving `song_name` from the filename (stripping extensions correctly).

---

## 4. Future Roadmap & Expansion

If asked to implement "Blueprint Phase 2" or "Phase 3":
1.  **Advanced Stems:** The current setup is hardcoded for 2 stems (`vocals` + `accompaniment`).
    *   *Upgrade:* Modify `engine.py` to accept a `stems` argument (4 or 6) and pass the `--two-stems` flag conditionally to the Demucs CLI.
2.  **Dockerization:** A `Dockerfile` would solve the "Dependency Hell" on Android/Pi.
    *   *Base Image:* `python:3.10-slim-bullseye` (ensures compatibility).
    *   *Install:* FFmpeg, Python deps.
3.  **Queue Management:** Currently, if 10 users upload files, 10 Demucs instances spawn, crashing the Pi.
    *   *Fix:* Implement a `Semaphore` or a proper Redis queue (`Celery` or `RQ`) to limit concurrent processing to **1**.

## 5. File System Map

*   `_dev/app.py`: **[ENTRY POINT]** API Server.
*   `_dev/engine.py`: **[CORE LOGIC]** Wrapper for AI model.
*   `_dev/requirements.txt`: **[CONFIG]** Python packages.
*   `_dev/static/app.js`: **[UI LOGIC]** Client-side upload & polling.
*   `inputs/`: **[DATA]** Raw user uploads.
*   `outputs/`: **[DATA]** The final product.

---
*End of Agent Manual*
