# Intelligent Stem Separator

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg) ![Python](https://img.shields.io/badge/python-3.9%2B-green.svg) ![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

**Bring the power of AI Audio Separation to your Raspberry Pi, Android phone, or local Linux machine.**

The **Intelligent Stem Separator** is a lightweight, self-hosted web application that splits any audio track into its constituent parts: **Vocals** and **Accompaniment** (Instrumental). It is explicitly designed to be portable, running on constrained hardware without requiring cloud subscriptions or heavy desktop GUIs.

---

## 🚀 Features

*   **Self-Hosted AI:** Runs entirely on your device. No data leaves your network.
*   **Web Interface:** Simple Drag & Drop UI accessible from any browser on your network.
*   **Powerful Backend:** Uses **Demucs (Hybrid Transformer)**, a state-of-the-art music source separation model by Meta Research.
*   **Hardware Optimized:** Designed to run on Raspberry Pi 4 (4GB/8GB) and Android (via Termux).
*   **API Ready:** Includes a fully documented Swagger/OpenAPI endpoint for developers.

---

## 🛠️ Architecture

The project consists of three main components:
1.  **Frontend:** A vanilla HTML/JS web page that handles file uploads and status updates.
2.  **API Server:** A **FastAPI** application that queues tasks and serves results.
3.  **Engine:** A Python wrapper around the **Demucs** CLI that performs the actual audio processing using FFmpeg and PyTorch.

---

## 📥 Installation

### Prerequisites
*   **Operating System:** Linux (Ubuntu/Debian/Raspberry Pi OS) or Android (Termux).
*   **Python:** Version 3.9 or newer.
*   **System Libraries:** `FFmpeg` is required for audio processing.

### Step-by-Step Setup

#### 1. Install System Dependencies
**Debian / Ubuntu / Raspberry Pi:**
```bash
sudo apt update
sudo apt install ffmpeg python3-venv -y
```

**Android (Termux):**
```bash
pkg update
pkg install ffmpeg python
```

#### 2. Clone & Prepare
Navigate to the project directory (or download the source):
```bash
cd StemSeparator/_dev
```

#### 3. Set up the Environment
Create a virtual environment to keep dependencies clean:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4. Install Python Packages
```bash
pip install -r requirements.txt
```
*Note: The first time you run this, it may take a few minutes to compile some packages on ARM devices.*

---

## 🎮 Usage

### Starting the Server
From the `_dev` directory, run:

```bash
# Standard run
python app.py

# OR run in the background (keeps running after you close terminal)
nohup python app.py > ../server.log 2>&1 &
```

The server will start at: `http://0.0.0.0:8000`

### Using the Interface
1.  Open your web browser (Chrome, Firefox, Safari).
2.  Navigate to `http://localhost:8000` (or your device's IP address, e.g., `http://192.168.1.50:8000`).
3.  **Drag and drop** an MP3 or WAV file into the box.
4.  Wait for the processing to complete.
    *   *First Run Note:* The AI model (approx. 100MB) will be downloaded automatically the first time you process a file. This may cause a delay.
5.  **Download** your isolated Vocals or Accompaniment tracks!

---

## 🔧 Troubleshooting

| Issue | Possible Cause | Solution |
| :--- | :--- | :--- |
| **"Upload Failed"** | File too large or network issue. | Check server logs. Ensure file is audio format. |
| **Server crashes on Pi** | Out of RAM. | Ensure you are using a Pi 4 with at least 4GB RAM. Add swap space. |
| **"FFT not found"** | PyTorch issue on ARM. | Reinstall PyTorch via system packages or specific wheels. |
| **Stuck on "Processing..."** | Backend error. | Check the terminal output where `app.py` is running for error logs. |

---

## 🧩 Directory Structure

*   `_dev/`: Contains all source code (`app.py`, `engine.py`, `static/`).
*   `inputs/`: Where uploaded files are temporarily stored.
*   `outputs/`: Where the separated stems are saved.
*   `GEMINI.md`: Context file for AI assistants.
*   `AGENTS.md`: Operational manual for AI agents.

---

## ⚖️ License & Credits

*   **Engine:** Powered by [Demucs](https://github.com/facebookresearch/demucs) (MIT License).
*   **Web Framework:** Built with [FastAPI](https://fastapi.tiangolo.com/).
*   **Project:** Intelligent Stem Separator.

---
*Happy Mixing!*
