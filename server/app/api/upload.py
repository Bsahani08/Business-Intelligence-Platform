from fastapi import APIRouter, UploadFile, File
import pandas as pd

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    return {
        "filename": file.filename,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "preview": df.head(10).fillna("").to_dict(orient="records"),
    }