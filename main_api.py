from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

class ScriptInput(BaseModel):
    song_name: str  # Changed from 'argument' to 'song_name'

# Script paths
scripts = [
    os.path.join("redit_api", "post_calling.py"),
    os.path.join("model_filter", "filter_post_openai.py"),
    os.path.join("redit_api", "comments_calling.py"),
    os.path.join("model_filter", "filter_comment_openai.py"),
    "extract_song_1.py"
]

@app.post("/run-scripts")
def run_scripts(input: ScriptInput):
    results = []

    for script in scripts:
        try:
            print("Running script: ", script)
            result = subprocess.run(
                ["python3", script, input.song_name],
                check=True,
                capture_output=True,
                text=True
            )
            results.append({
                "script": script,
                "status": "success",
                "output": result.stdout.strip()
            })
            print("Completed results: ", results, '\n')
        except subprocess.CalledProcessError as e:
            results.append({
                "script": script,
                "status": "error",
                "output": e.stderr.strip()
            })

    return {"results": results}
