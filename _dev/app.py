import os
import shutil
import asyncio
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from engine import StemEngine

app = FastAPI(title="Intelligent Stem Separator")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, 'inputs')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

# Ensure directories exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Engine (Global for now, simpler for MVP)
# Note: In production, might want to instantiate on demand or manage via dependency injection
# to handle resource usage.
engine = StemEngine(stems=2)

def run_separation(file_path: str, output_path: str):
    """
    Wrapper to run the synchronous engine process in a background task.
    """
    try:
        engine.process(file_path, output_path)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def save_upload_file(file_src, dest_path):
    """
    Helper to save file in a thread-safe way (blocking I/O).
    """
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file_src, buffer)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    filename = file.filename
    safe_filename = os.path.basename(filename)
    file_location = os.path.join(INPUT_DIR, safe_filename)
    
    # Save the uploaded file
    await asyncio.to_thread(save_upload_file, file.file, file_location)
        
    # Create a specific output directory for this file (e.g. based on name)
    # Spleeter creates a folder with the song name in the output directory
    song_name = os.path.splitext(safe_filename)[0]
    
    # Queue the separation task
    background_tasks.add_task(run_separation, file_location, OUTPUT_DIR)
    
    return {"message": "File uploaded and separation started", "filename": safe_filename, "song_name": song_name}

@app.get("/status/{song_name}")
async def check_status(song_name: str):
    """
    Check if the output folder exists and has content.
    Simple polling mechanism.
    """
    target_dir = os.path.join(OUTPUT_DIR, song_name)
    if os.path.exists(target_dir) and len(os.listdir(target_dir)) > 0:
        files = os.listdir(target_dir)
        return {"status": "completed", "files": files}
    else:
        return {"status": "processing"}

@app.get("/download/{song_name}/{stem}")
async def download_stem(song_name: str, stem: str):
    """
    Download a specific stem (e.g., vocals.mp3, accompaniment.mp3)
    """
    file_path = os.path.join(OUTPUT_DIR, song_name, stem)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

# Mount static files for the frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
