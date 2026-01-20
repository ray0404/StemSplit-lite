Here is **Phase 1** of the blueprint. We are focusing strictly on getting the **Core Engine** running on Raspberry Pi.

Our goal today is to get the Pi to successfully separate one audio file using a Python script. Once this logic holds up, we will wrap it in the API in the next session.

### Phase 1: The Core Engine (Raspberry Pi Focus)

#### 1. System-Level Dependencies

Before touching Python, we need the underlying audio libraries installed on Raspberry Pi OS.

```bash
# Update package list
sudo apt update

# Install FFmpeg (Crucial for audio decoding) and libsndfile (needed by some audio libs)
sudo apt install ffmpeg libsndfile1-dev -y

```

---

#### 2. Project & Environment Setup

Navigate to project folder (adjusting for where you keep  projects) and set up the structure.

```bash
# Create directories
mkdir -p StemSeparator/_dev
mkdir -p StemSeparator/inputs
mkdir -p StemSeparator/outputs

# Enter development folder
cd StemSeparator/_dev

# Create a virtual environment (Best practice on Pi to avoid conflicting with system Python)
python3 -m venv venv

# Activate it
source venv/bin/activate

```

---

#### 3. The `requirements.txt`

Create this file inside `_dev/`.
*Note: We are pinning `spleeter` but also including `fastapi` now so we don't have to reinstall later.*

**File:** `_dev/requirements.txt`

```text
spleeter==2.4.0
fastapi
uvicorn
python-multipart
# Pandas is required by Spleeter but sometimes needs specific versions on Pi
pandas

```

**Install them:**

```bash
pip install --upgrade pip
pip install -r requirements.txt

```

*(Heads up: Spleeter installs TensorFlow. On a Raspberry Pi, this can take a few minutes to compile/install. If you hit a "wheel" error regarding TensorFlow, let me know, as Pi architectures sometimes need a specific TensorFlow binary.)*

---

#### 4. The Engine Wrapper (`engine.py`)

This script acts as the "controller" for the AI. It checks paths and runs the separator.

**File:** `_dev/engine.py`

```python
import os
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter

class StemEngine:
    def __init__(self, stems=2):
        """
        Initialize the Spleeter Separator.
        stems: 2 (vocals/accomp), 4 (vocals/drums/bass/other), or 5 (adds piano)
        """
        self.stems = stems
        # Initialize the model immediately so we don't load it on every request
        print(f"[Init] Loading Spleeter model for {stems} stems...")
        self.separator = Separator(f'spleeter:{stems}stems')
        print("[Init] Model loaded.")

    def process(self, input_path, output_dir):
        """
        Separates the audio file at input_path and saves to output_dir.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print(f"[Process] Separating: {os.path.basename(input_path)}")
        
        # This function handles the heavy lifting
        # synchronous=False is often used in API contexts, but for CLI testing we keep it simple
        self.separator.separate_to_file(
            input_path,
            output_dir,
            codec='mp3',
            bitrate='192k'
        )
        print(f"[Success] Saved to: {output_dir}")
        return True

# --- Quick Test Block ---
# This allows you to run 'python engine.py' directly to test without the API.
if __name__ == "__main__":
    # 1. Define paths relative to this script
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    INPUT_DIR = os.path.join(BASE_DIR, 'inputs')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

    # 2. Check for a test file
    # Place a file named 'test.mp3' in the /inputs folder to test this!
    test_file = os.path.join(INPUT_DIR, 'test.mp3')

    if os.path.exists(test_file):
        engine = StemEngine(stems=2)
        engine.process(test_file, OUTPUT_DIR)
    else:
        print(f"No test file found at: {test_file}")
        print("Please place a 'test.mp3' in the inputs folder to verify.")

```

---

### 5. Verification Step

1. **Find an audio file:** Copy any MP3 to `StemSeparator/inputs/` and rename it `test.mp3`.
2. **Run the script:**
```bash
python engine.py

```


3. **First Run Delay:** Spleeter will download a pre-trained model (approx. 100MB) on the very first run.
4. **Check Output:** Look in `StemSeparator/outputs/test/`. You should see `vocals.mp3` and `accompaniment.mp3`.

---