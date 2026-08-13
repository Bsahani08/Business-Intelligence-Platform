from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
from io import BytesIO

from app.services.data_quality import analyze_data_quality


app = FastAPI(
    title="AI Business Intelligence Platform",
    description="AI-powered Business Intelligence Platform API",
    version="1.0.0",
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Root API
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "AI Business Intelligence Platform API is running 🚀"
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Business Intelligence Platform"
    }


# --------------------------------------------------
# Dataset Upload
# --------------------------------------------------

@app.post("/upload/")
async def upload_datasets(
    sales: UploadFile = File(...),
    features: UploadFile = File(...),
    stores: UploadFile = File(...),
):

    try:

        # ------------------------------------------
        # Read uploaded CSV files
        # ------------------------------------------

        sales_content = await sales.read()
        features_content = await features.read()
        stores_content = await stores.read()

        # ------------------------------------------
        # Convert CSV files to DataFrames
        # ------------------------------------------

        sales_df = pd.read_csv(
            BytesIO(sales_content)
        )

        features_df = pd.read_csv(
            BytesIO(features_content)
        )

        stores_df = pd.read_csv(
            BytesIO(stores_content)
        )

        # ------------------------------------------
        # Clean column names
        # ------------------------------------------

        sales_df.columns = sales_df.columns.str.strip()
        features_df.columns = features_df.columns.str.strip()
        stores_df.columns = stores_df.columns.str.strip()

        # ------------------------------------------
        # Required columns
        # ------------------------------------------

        required_sales_columns = {
            "Store",
            "Dept",
            "Date",
            "Weekly_Sales",
        }

        required_features_columns = {
            "Store",
            "Date",
        }

        required_stores_columns = {
            "Store",
        }

        # ------------------------------------------
        # Validate Sales dataset
        # ------------------------------------------

        missing_sales = (
            required_sales_columns
            - set(sales_df.columns)
        )

        if missing_sales:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Invalid Sales dataset",
                    "missing_columns": sorted(
                        missing_sales
                    ),
                },
            )

        # ------------------------------------------
        # Validate Features dataset
        # ------------------------------------------

        missing_features = (
            required_features_columns
            - set(features_df.columns)
        )

        if missing_features:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Invalid Features dataset",
                    "missing_columns": sorted(
                        missing_features
                    ),
                },
            )

        # ------------------------------------------
        # Validate Stores dataset
        # ------------------------------------------

        missing_stores = (
            required_stores_columns
            - set(stores_df.columns)
        )

        if missing_stores:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Invalid Stores dataset",
                    "missing_columns": sorted(
                        missing_stores
                    ),
                },
            )

        # ------------------------------------------
        # Convert dates
        # ------------------------------------------

        sales_df["Date"] = pd.to_datetime(
            sales_df["Date"],
            errors="coerce",
        )

        features_df["Date"] = pd.to_datetime(
            features_df["Date"],
            errors="coerce",
        )

        # ------------------------------------------
        # Analyze Data Quality
        # ------------------------------------------

        sales_quality = analyze_data_quality(
            sales_df
        )

        features_quality = analyze_data_quality(
            features_df
        )

        stores_quality = analyze_data_quality(
            stores_df
        )

        # ------------------------------------------
        # Remove invalid dates
        # ------------------------------------------

        sales_df = sales_df.dropna(
            subset=["Date"]
        )

        features_df = features_df.dropna(
            subset=["Date"]
        )

        # ------------------------------------------
        # Merge Sales + Features
        # ------------------------------------------

        merged_df = pd.merge(
            sales_df,
            features_df,
            on=["Store", "Date"],
            how="left",
            suffixes=("", "_feature"),
        )

        # ------------------------------------------
        # Merge with Stores
        # ------------------------------------------

        merged_df = pd.merge(
            merged_df,
            stores_df,
            on="Store",
            how="left",
            suffixes=("", "_store"),
        )

        # ------------------------------------------
        # Basic Data Quality Information
        # ------------------------------------------

        sales_missing = int(
            sales_df.isna().sum().sum()
        )

        features_missing = int(
            features_df.isna().sum().sum()
        )

        stores_missing = int(
            stores_df.isna().sum().sum()
        )

        merged_missing = int(
            merged_df.isna().sum().sum()
        )

        # ------------------------------------------
        # Response
        # ------------------------------------------

        return {

            "message": (
                "Datasets uploaded and "
                "analyzed successfully"
            ),

            # --------------------------------------
            # Dataset Statistics
            # --------------------------------------

            "sales_rows": int(
                len(sales_df)
            ),

            "features_rows": int(
                len(features_df)
            ),

            "stores_rows": int(
                len(stores_df)
            ),

            "merged_rows": int(
                len(merged_df)
            ),

            "sales_columns": int(
                len(sales_df.columns)
            ),

            "features_columns": int(
                len(features_df.columns)
            ),

            "stores_columns": int(
                len(stores_df.columns)
            ),

            "merged_columns": int(
                len(merged_df.columns)
            ),

            # --------------------------------------
            # Data Quality Results
            # --------------------------------------

            "data_quality": {

                "sales": sales_quality,

                "features": features_quality,

                "stores": stores_quality,

            },

            # --------------------------------------
            # Missing Values
            # --------------------------------------

            "missing_values": {

                "sales": sales_missing,

                "features": features_missing,

                "stores": stores_missing,

                "merged": merged_missing,

            },

            # --------------------------------------
            # File Names
            # --------------------------------------

            "files": {

                "sales": sales.filename,

                "features": features.filename,

                "stores": stores.filename,

            },

        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail={
                "message": "Dataset processing failed",
                "error": str(e),
            },
        )