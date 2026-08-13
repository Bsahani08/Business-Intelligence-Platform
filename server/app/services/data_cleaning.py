import pandas as pd


def clean_dataset(df: pd.DataFrame):
    """
    Clean a dataset and return:

    1. Cleaned DataFrame
    2. Cleaning summary
    """

    # ------------------------------------------
    # Original dataset information
    # ------------------------------------------

    original_rows = len(df)
    original_columns = len(df.columns)

    cleaned_df = df.copy()

    # ------------------------------------------
    # Clean column names
    # ------------------------------------------

    cleaned_df.columns = (
        cleaned_df.columns
        .str.strip()
        .str.replace(" ", "_")
    )

    # ------------------------------------------
    # Remove completely empty rows
    # ------------------------------------------

    empty_rows = int(
        cleaned_df.isna()
        .all(axis=1)
        .sum()
    )

    cleaned_df = cleaned_df.dropna(
        how="all"
    )

    # ------------------------------------------
    # Remove duplicate rows
    # ------------------------------------------

    duplicate_rows = int(
        cleaned_df.duplicated().sum()
    )

    cleaned_df = cleaned_df.drop_duplicates()

    # ------------------------------------------
    # Missing values BEFORE cleaning
    # ------------------------------------------

    missing_values_before = int(
        cleaned_df.isna()
        .sum()
        .sum()
    )

    # ------------------------------------------
    # Handle numeric missing values
    # ------------------------------------------

    numeric_columns = cleaned_df.select_dtypes(
        include=["number"]
    ).columns

    for column in numeric_columns:

        if cleaned_df[column].isna().any():

            median_value = cleaned_df[
                column
            ].median()

            if pd.notna(median_value):

                cleaned_df[column] = (
                    cleaned_df[column]
                    .fillna(median_value)
                )

    # ------------------------------------------
    # Handle categorical missing values
    # ------------------------------------------

    categorical_columns = cleaned_df.select_dtypes(
        include=["object", "category"]
    ).columns

    for column in categorical_columns:

        if cleaned_df[column].isna().any():

            cleaned_df[column] = (
                cleaned_df[column]
                .fillna("Unknown")
            )

    # ------------------------------------------
    # Missing values AFTER cleaning
    # ------------------------------------------

    missing_values_after = int(
        cleaned_df.isna()
        .sum()
        .sum()
    )

    # ------------------------------------------
    # Convert date columns
    # ------------------------------------------

    date_columns_converted = []

    for column in cleaned_df.columns:

        if "date" in column.lower():

            converted = pd.to_datetime(
                cleaned_df[column],
                errors="coerce"
            )

            if converted.notna().sum() > 0:

                cleaned_df[column] = converted

                date_columns_converted.append(
                    column
                )

    # ------------------------------------------
    # Final statistics
    # ------------------------------------------

    final_rows = len(cleaned_df)
    final_columns = len(cleaned_df.columns)

    rows_removed = (
        original_rows - final_rows
    )

    missing_values_handled = (
        missing_values_before
        - missing_values_after
    )

    # ------------------------------------------
    # Cleaning summary
    # ------------------------------------------

    cleaning_summary = {

        "original_rows": int(
            original_rows
        ),

        "final_rows": int(
            final_rows
        ),

        "original_columns": int(
            original_columns
        ),

        "final_columns": int(
            final_columns
        ),

        "duplicate_rows_removed": int(
            duplicate_rows
        ),

        "empty_rows_removed": int(
            empty_rows
        ),

        "rows_removed": int(
            rows_removed
        ),

        "missing_values_before": int(
            missing_values_before
        ),

        "missing_values_after": int(
            missing_values_after
        ),

        "missing_values_handled": int(
            missing_values_handled
        ),

        "date_columns_converted": (
            date_columns_converted
        ),
    }

    return cleaned_df, cleaning_summary