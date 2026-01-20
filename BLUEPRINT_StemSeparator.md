Here is a technical architecture blueprint for the **Intelligent Stem Separator**. This design prioritizes portability between Raspberry Pi 4 environment and Termux on Android, while adding a lightweight Web GUI for easier interaction.

### 1. High-Level Architecture

This project follows a **Client-Server** model, even when running locally on one device. This decoupling allows the "backend" (heavy AI processing) to run on your powerful Galaxy S25 or Raspberry Pi, while the "frontend" (UI) can be accessed via any browser.

* **Core Engine (Backend):** Python-based API that handles file upload, processing, and storage.
* **AI Model:** `Spleeter` (TensorFlow) or `Demucs` (PyTorch). *Note: Spleeter is generally lighter and easier to install in Termux.*
* **Interface (Frontend):** A lightweight, static HTML/JS web page (PWA-ready) that communicates with the backend via REST API.

---

### 2. Technology Stack

| Component | Technology | Rationale |
| --- | --- | --- |
| **Language** | Python 3.9+ | Standard for AI/ML; fully supported in Termux & Pi. |
| **Web Framework** | **FastAPI** | Extremely fast, lightweight, and auto-generates API docs (Swagger UI). |
| **AI Library** | **Spleeter** | Pre-trained models available; separates 2, 4, or 5 stems. |
| **Audio Processing** | **FFmpeg** | Required for audio decoding/encoding. |
| **Frontend** | Vanilla JS + HTML5 | No build steps (React/Vue) needed; keeps it portable and easily editable. |
| **Task Queue** | Python `asyncio` | Handles long-processing tasks without freezing the server. |

---

### 3. Directory Structure (User Standard)

Adhering to your preferred project structure:

```text
STEM_SEPARATOR/
├── _arch/                  # Archives of old experiments or logs
├── _dev/                   # Current development sandbox
│   ├── app.py              # Main FastAPI application entry point
│   ├── engine.py           # Wrapper for Spleeter/Demucs logic
│   ├── requirements.txt    # Python dependencies
│   └── static/             # Frontend assets
│       ├── index.html      # Web GUI
│       ├── style.css
│       └── app.js
├── _ver/                   # Previous stable versions
├── v1.0/                   # Production release
├── inputs/                 # Folder for uploaded tracks
└── outputs/                # Folder for separated stems

```

---

### 4. Data Flow Diagram

```text
[ User / Browser ]
       |
       | (1) Upload Audio File (POST /upload)
       v
[ FastAPI Server ] <-----> [ FFmpeg ] (Validation/Conversion)
       |
       | (2) Queue Job
       v
[ AI Engine (Spleeter) ]
       |
       | (3) Process (Load Model -> Separate -> Write to Disk)
       v
[ File System ] (/outputs/song_name/vocals.wav, drums.wav...)
       |
       | (4) Return Download Links
       v
[ User / Browser ] <----- (5) Download Stems (GET /download)

```

---

### 5. Implementation Details & Challenges

#### **A. Raspberry Pi 4 (Linux)**

* **Performance:** The 8GB RAM model is sufficient for Spleeter. Processing a 3-minute song may take 1–3 minutes depending on the model (2-stems vs 5-stems).
* **Thermal:** Ensure the Pi has a heatsink or fan; ML inference causes CPU throttling quickly.

#### **B. Termux (Android)**

* **Dependency Hell:** Installing `tensorflow` or `numpy` in Termux can be tricky due to compilation requirements.
* *Solution:* Use the `tur-repo` (Termux User Repository) or `proot-distro` (running a virtual Ubuntu inside Termux) to install standard Linux wheels.


* **Binaries:** Ensure `ffmpeg` is installed via `pkg install ffmpeg`.

#### **C. The Web GUI**

* **Design:** Simple "Drag & Drop" zone.
* **Feedback:** Since processing takes time, the UI must poll the server ("Is it done yet?") or use WebSockets to show a progress bar so the user doesn't think it froze.

---

### 6. Development Roadmap

1. **Environment Setup:**
* Install FFmpeg (`sudo apt install ffmpeg` on Pi, `pkg install ffmpeg` on Termux).
* Set up Python Virtual Environment.


2. **Core Script:** Write a simple Python script `engine.py` that takes a file path and runs Spleeter on it.
3. **API Layer:** Wrap `engine.py` with FastAPI to accept HTTP uploads.
4. **Frontend:** Create the `index.html` to upload a file and display the results.

---