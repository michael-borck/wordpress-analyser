from fastapi import FastAPI, UploadFile, File, HTTPException
import tempfile
import shutil
from pathlib import Path

from .core import analyse_file
from .models import WordPressAnalysisResult

app = FastAPI(title="wordpress-analyser", version="0.2.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyse", response_model=WordPressAnalysisResult)
async def analyse(file: UploadFile = File(...)):
    if not file.filename.endswith(".php"):
        raise HTTPException(status_code=400, detail="Only .php files are supported")
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        tmp_file = tmp_dir / file.filename
        tmp_file.write_bytes(await file.read())
        result = analyse_file(tmp_file)
        if result.error:
            raise HTTPException(status_code=400, detail=result.error)
        return result
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
