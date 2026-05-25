import shutil
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from lens_contract import add_contract_routes, add_cors

from .core import analyse_file
from .manifest import MANIFEST
from .models import WordPressAnalysisResult

app = FastAPI(title="wordpress-analyser", version=MANIFEST["version"])

# GET /health and GET /manifest (the family contract, via lens-contract).
add_contract_routes(app, MANIFEST)
# CORS — env-driven: WORDPRESS_ANALYSER_MODE=desktop (Electron) or WORDPRESS_ANALYSER_ALLOWED_ORIGINS.
add_cors(app, env_prefix="WORDPRESS_ANALYSER")


@app.post("/analyse", response_model=WordPressAnalysisResult)
async def analyse(file: UploadFile = File(...)):
    if not (file.filename or "").endswith(".php"):
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
