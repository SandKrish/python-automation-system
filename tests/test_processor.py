import pytest
import pandas as pd
from src.core.processor import ExcelProcessor

@pytest.fixture
def sample_config():
    return {
        "paths": {"output_dir": "data/output"},
        "logging": {"level": "INFO"}
    }

def test_validation_logic(sample_config):
    processor = ExcelProcessor(sample_config)
    
    # Valid data
    valid_df = pd.DataFrame({
        'Transaction ID': ['T001'],
        'Date': ['2026-04-18'],
        'Product': ['Laptop'],
        'Quantity': [1],
        'Unit Price': [1200.0],
        'Total Revenue': [1200.0]
    })
    
    data_frames = {"sales_data": valid_df}
    results = processor.validate_data(data_frames)
    
    assert len(results["sales_data"]) == 1
    assert results["sales_data"][0].product == "Laptop"

def test_invalid_validation(sample_config):
    processor = ExcelProcessor(sample_config)
    
    # Invalid data (Negative quantity)
    invalid_df = pd.DataFrame({
        'Transaction ID': ['T001'],
        'Date': ['2026-04-18'],
        'Product': ['Laptop'],
        'Quantity': [-1],
        'Unit Price': [1200.0],
        'Total Revenue': [1200.0]
    })
    
    data_frames = {"sales_data": invalid_df}
    results = processor.validate_data(data_frames)
    
    # Should skip the invalid row
    assert len(results["sales_data"]) == 0
