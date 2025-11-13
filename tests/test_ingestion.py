"""Tests for data ingestion functions."""

import json
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


def test_load_json_success():
    """Test loading real JSON file."""
    df = load_json('data/events_data.json')
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)


def test_load_excel_success():
    """Test loading real XLSX file."""
    df = load_excel('data/catalogue.xlsx')
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)


@pytest.mark.skip(reason="Skipping for now")
def test_load_csv_file_not_found():
    """Test error handling when file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        load_csv('data/nonexistent.csv')


@pytest.mark.skip(reason="Skipping for now")
def test_load_json_file_not_found():
    """Test error handling when JSON file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        load_json('data/nonexistent.json')


@pytest.mark.skip(reason="Skipping for now")
def test_load_excel_file_not_found():
    """Test error handling when XLSX file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        load_excel('data/nonexistent.xlsx')


@pytest.mark.skip(reason="Skipping for now")
def test_load_csv_empty_file(tmp_path):
    """Test error handling when CSV file is empty."""
    empty_path = tmp_path / 'empty.csv'
    empty_path.write_text("", encoding="utf-8")
    with pytest.raises(pd.errors.EmptyDataError):
        load_csv(empty_path)


@pytest.mark.skip(reason="Skipping for now")
def test_load_json_empty_file(tmp_path):
    """Test error handling when JSON file is empty."""
    json_path = tmp_path / 'empty.json'
    json_path.write_text("", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_json(json_path)


@pytest.mark.skip(reason="Skipping for now")
def test_load_json_invalid_json(tmp_path):
    """Test error handling when CSV file is empty."""
    json_path = tmp_path / 'invalid.json'
    json_path.write_text("{invalid}", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_json(json_path)
