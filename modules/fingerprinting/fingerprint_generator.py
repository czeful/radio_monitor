from pathlib import Path
import subprocess

class FingerprintGenerator:

    def __init__( self, fpcalc_path: str = "tools/fpcalc.exe"):
        self.fpcalc_path = Path(fpcalc_path) 
        if not self.fpcalc_path.exists():
            raise  FileNotFoundError(
                f"fpcalc not found: {self.fpcalc_path}"
            )

    def generate(self, audio_path: str) -> dict:

        print("generate started")

        audio_file = Path(audio_path)
        
        if not audio_file.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file}")      

        result = subprocess.run(
            [
                str(self.fpcalc_path),
                "-json",
                str(audio_file)   
            ],
            capture_output=True,
            text=True,
            check=True
        )    

        import json

        data = json.loads(result.stdout)

        return {
            "duration": data["duration"],
            "fingerprint": data["fingerprint"]
        }