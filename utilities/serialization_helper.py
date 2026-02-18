"""
Helper functions to convert numpy/pandas types to Python native types for JSON serialization
"""
import numpy as np
import pandas as pd
from typing import Any, Dict, List


def convert_to_serializable(obj: Any) -> Any:
    """
    Recursively convert numpy/pandas types to Python native types for JSON serialization.
    
    Args:
        obj: Any object that may contain numpy/pandas types
        
    Returns:
        Object with all numpy/pandas types converted to Python native types
    """
    # Handle None
    if obj is None:
        return None
    
    # Handle numpy scalars
    if isinstance(obj, (np.integer, np.int64, np.int32, np.int16, np.int8)):
        return int(obj)
    if isinstance(obj, (np.floating, np.float64, np.float32, np.float16)):
        return float(obj)
    if isinstance(obj, (np.bool_, np.bool)):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    
    # Handle pandas types
    if isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient='records')
    if isinstance(obj, pd.Series):
        return obj.to_list()
    if isinstance(obj, (pd.Timestamp, pd.DatetimeIndex)):
        return str(obj)
    
    # Handle dictionaries recursively
    if isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    
    # Handle lists/tuples recursively
    if isinstance(obj, (list, tuple)):
        return [convert_to_serializable(item) for item in obj]
    
    # Return as-is for basic Python types
    return obj
