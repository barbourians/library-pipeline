"""Tests for data cleaning functions.
add more test
This module demonstrates proper testing patterns for Pandas code.
"""

import pytest
import pandas as pd
import pandas.testing as pdt
from src.data_processing.cleaning import (
    remove_duplicates,
    handle_missing_values,
    standardize_dates
)

# ========================================
# FIXTURES - Reusable test data
# ========================================

@pytest.fixture
def sample_df_with_duplicates():
    """Sample DataFrame with duplicate rows."""
    return pd.DataFrame({
        'id': [1, 2, 2, 3, 3, 3],
        'name': ['Alice', 'Bob', 'Bob', 'Charlie', 'Charlie', 'Charlie'],
        'value': [10, 20, 20, 30, 30, 30]
    })

@pytest.fixture
def sample_df_with_missing():
    """Sample DataFrame with missing values."""
    return pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Alice', None, 'Charlie', 'David'],
        'value': [10, 20, None, 40]
    })

@pytest.fixture
def sample_df_with_forward_fill():
    """Sample DataFrame with missing values."""
    return pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Alice', 'Alice', 'Charlie', 'David'],
        'value': [10, 20, 20, 40]
    })

# ========================================
# TESTS FOR remove_duplicates()
# ========================================

def test_remove_duplicates_exact(sample_df_with_duplicates):
    """Test duplicate removal using exact DataFrame comparison."""
    result = remove_duplicates(sample_df_with_duplicates, subset=['id'])

    expected = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'value': [10, 20, 30]
    })

    # Reset index for comparison
    result = result.reset_index(drop=True)

    pdt.assert_frame_equal(result, expected)

def test_remove_duplicates_properties(sample_df_with_duplicates):
    """Test duplicate removal using property assertions."""
    result = remove_duplicates(sample_df_with_duplicates, subset=['id'])

    # Test properties instead of exact values
    assert len(result) == 3
    assert result['id'].is_unique
    assert set(result['id']) == {1, 2, 3}

def test_remove_duplicates_no_changes():
    """Test with DataFrame that has no duplicates."""
    df_unique = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['A', 'B', 'C']
    })

    result = remove_duplicates(df_unique, subset=['id'])

    pdt.assert_frame_equal(result, df_unique)

def test_remove_duplicates_empty():
    """Test with empty DataFrame."""
    empty_df = pd.DataFrame({'id': [], 'name': []})
    result = remove_duplicates(empty_df)

    assert len(result) == 0
    pdt.assert_frame_equal(result, empty_df)

# ========================================
# TESTS FOR handle_missing_values()
# ========================================

def test_handle_missing_drop(sample_df_with_missing):
    """Test dropping rows with missing values."""
    result = handle_missing_values(sample_df_with_missing, strategy='drop')

    # Should only have rows without any NaN
    assert len(result) == 2
    assert result['name'].notna().all()
    assert result['value'].notna().all()

def test_handle_missing_fill(sample_df_with_missing):
    """Test filling missing values."""
    result = handle_missing_values(
        sample_df_with_missing, 
        strategy='fill', 
        fill_value=0
    )

    # Should have all 4 rows
    assert len(result) == 4
    # No missing values
    assert result['name'].notna().all() or (result['name'] == 0).any()
    assert result['value'].notna().all()

def test_handle_missing_invalid_strategy(sample_df_with_missing):
    """Test that invalid strategy raises error."""
    with pytest.raises(ValueError, match="Unknown strategy"):
        handle_missing_values(sample_df_with_missing, strategy='invalid')

def test_handle_missing_drop_column_name(sample_df_with_missing):
    """Test dropping rows with missing values for column name"""
    result = handle_missing_values(
        sample_df_with_missing, 
        strategy='drop',
        columns=['name']
        )

    # Should only have rows without any NaN
    assert len(result) == 3
    assert result['name'].notna().all()

def test_fill_value_must_be_provided_when_strategy_fill(sample_df_with_missing):
    """Test that fill_value missing raises error."""
    with pytest.raises(ValueError, match="fill_value must be provided when strategy='fill'"):
        handle_missing_values(sample_df_with_missing, strategy='fill')

def test_handle_missing_drop_column_forward_fill(
        sample_df_with_missing, sample_df_with_forward_fill
        ):
    """Test dropping rows with missing values."""
    result = handle_missing_values(sample_df_with_missing, strategy='forward_fill')

    # All rows should be returned
    assert len(result) == 4
    assert result['name'].notna().all()
    assert result['value'].notna().all()

    # Result should match pytest fixture for forward fill
    pdt.assert_frame_equal(result, sample_df_with_forward_fill)
