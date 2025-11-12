"""Tests for data ingestion functions."""

import pytest
import pandas as pd
from pathlib import Path
from src.data_processing.ingestion import load_csv, load_json, load_excel

# Test with actual sample files
def test_load_csv_success():
    """Test loading real CSV file."""
    df = load_csv('data/circulation_data.csv')

    assert len(df) > 0
    assert 'transaction_id' in df.columns

def test_load_csv_file_not_found():
    """Test error handling when file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        load_csv('data/nonexistent.csv')

def test_load_json_success():
    """Test loading real JSON file."""
    df = load_json('data/events_data.json')

    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)

# Add more tests...