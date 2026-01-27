import os
import sys
import shutil
import subprocess

class StemEngine:
    def __init__(self, stems=2):
        """
        Initialize the Demucs Engine wrapper.
        stems: 2 (vocals/other) or 4 (drums/bass/other/vocals).
        """
        self.stems = stems
        self.model = "htdemucs" # Default robust model
        print(f"[Init] Demucs engine ready. Model: {self.model}, Stems: {stems}")

    def process(self, input_path, output_dir):
        """
        Separates the audio file at input_path using Demucs CLI.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        os.makedirs(output_dir, exist_ok=True)

        print(f"[Process] Separating: {os.path.basename(input_path)}")
        
        # Construct command
        # python -m demucs -n htdemucs input_path -o output_dir --mp3
        cmd = [
            sys.executable, "-m", "demucs",
            "-n", self.model,
            input_path,
            "-o", output_dir,
            "--mp3",
            "--mp3-bitrate", "192"
        ]

        if self.stems == 2:
            # Separates into 'vocals' and 'no_vocals'
            cmd.append("--two-stems=vocals")
        
        try:
            # Run Demucs
            # capture_output=False lets us see the progress bar in the console
            subprocess.run(cmd, check=True)
            
            # Post-processing to match Spleeter's folder structure
            # Demucs output: output_dir/htdemucs/song_name/
            # Expected: output_dir/song_name/
            
            song_name = os.path.splitext(os.path.basename(input_path))[0]
            demucs_output = os.path.join(output_dir, self.model, song_name)
            final_output = os.path.join(output_dir, song_name)

            if os.path.exists(demucs_output):
                # If the target directory already exists, remove it to avoid conflicts
                if os.path.exists(final_output):
                    shutil.rmtree(final_output)
                
                shutil.move(demucs_output, final_output)
                
                # Rename no_vocals.mp3 to accompaniment.mp3 for Spleeter compatibility
                no_vocals = os.path.join(final_output, "no_vocals.mp3")
                if os.path.exists(no_vocals):
                    os.rename(no_vocals, os.path.join(final_output, "accompaniment.mp3"))
                
                # Try to clean up the empty model folder
                try:
                    os.rmdir(os.path.join(output_dir, self.model))
                except OSError:
                    pass # Directory might not be empty if other processes are running
                    
            print(f"[Success] Saved to: {final_output}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"[Error] Demucs failed: {e}")
            raise e

if __name__ == "__main__":
    # Test block
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    INPUT_DIR = os.path.join(BASE_DIR, 'inputs')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
    
    # Ensure inputs dir exists for the test
    os.makedirs(INPUT_DIR, exist_ok=True)
    
    test_file = os.path.join(INPUT_DIR, 'test.mp3')

    if os.path.exists(test_file):
        engine = StemEngine(stems=2)
        engine.process(test_file, OUTPUT_DIR)
    else:
        print(f"No test file found at: {test_file}")
        print("Please place a 'test.mp3' in the inputs folder to verify.")