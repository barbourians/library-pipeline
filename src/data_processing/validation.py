"""
Data validation functions.
"""

import pandas as pd


def validate_isbn(isbn):
    """Validate ISBN-13 format.

    Args:
        isbn (str | int | float): ISBN to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if pd.isna(isbn) or isbn == "":
        return False

    # Remove hyphens
    isbn = str(isbn).replace("-", "").strip()

    # Check length
    if len(isbn) != 13:
        return False

    # Check if all digits
    if not isbn.isdigit():
        return False

    return True
