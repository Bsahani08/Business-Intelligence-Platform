import pandas as pd


def analyze_data_quality(df: pd.DataFrame) -> dict:
    """
    Analyze the quality of a Pandas DataFrame.

    Returns:
        dict: Data quality metrics for the dataset.
    """

    # Basic dimensions
    rows = len(df)
    columns = len(df.columns)

    # Missing values
    total_missing = int(df.isna().sum().sum())

    missing_by_column = {
        column: int(count)
        for column, count in df.isna().sum().items()
        if count > 0
    }

    # Duplicate rows
    duplicate_rows = int(df.duplicated().sum())

    # Data types
    data_types = {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }

    # Unique values
    unique_values = {
        column: int(df[column].nunique(dropna=True))
        for column in df.columns
    }

    # Missing-value percentage
    total_cells = rows * columns

    if total_cells > 0:
        missing_percentage = round(
            (total_missing / total_cells) * 100,
            2
        )
    else:
        missing_percentage = 0.0

    # Calculate quality score
    score = 100.0

    # Deduct for missing values
    score -= min(missing_percentage, 40)

    # Deduct for duplicate rows
    if rows > 0:
        duplicate_percentage = (
            duplicate_rows / rows
        ) * 100

        score -= min(duplicate_percentage, 30)

    score = max(0, round(score, 2))

    # Quality status
    if score >= 90:
        quality_status = "Excellent"
    elif score >= 75:
        quality_status = "Good"
    elif score >= 50:
        quality_status = "Needs Improvement"
    else:
        quality_status = "Poor"

    return {
        "rows": rows,
        "columns": columns,
        "total_missing_values": total_missing,
        "missing_percentage": missing_percentage,
        "missing_by_column": missing_by_column,
        "duplicate_rows": duplicate_rows,
        "data_types": data_types,
        "unique_values": unique_values,
        "quality_score": score,
        "quality_status": quality_status,
    }