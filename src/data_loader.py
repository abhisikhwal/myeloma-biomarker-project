"""
Data Loading Utilities for Multiple Myeloma Clinical Data

This module provides functions to load and merge clinical data files from the
MMRF CoMMpass dataset. It handles TSV files and performs basic data validation.

Author: Abhinav Sikhwal
Date: January 2026
"""

import pandas as pd
import os
from pathlib import Path
from typing import Dict, Optional


def load_clinical_files(data_dir: str) -> Dict[str, pd.DataFrame]:
    """
    Load all clinical TSV files from the specified directory.
    
    This function reads the following files:
    - clinical.tsv: Core clinical information
    - exposure.tsv: Patient exposure history
    - family_history.tsv: Family medical history
    - follow_up.tsv: Patient follow-up data
    - pathology_detail.tsv: Pathology details
    
    Parameters
    ----------
    data_dir : str
        Path to the directory containing the TSV files
        
    Returns
    -------
    Dict[str, pd.DataFrame]
        Dictionary with file names as keys and DataFrames as values
        
    Examples
    --------
    >>> data_dict = load_clinical_files('data/raw/')
    >>> print(data_dict.keys())
    dict_keys(['clinical', 'exposure', 'family_history', 'follow_up', 'pathology_detail'])
    """
    # Define the files we want to load
    file_names = [
        'clinical.tsv',
        'exposure.tsv',
        'family_history.tsv',
        'follow_up.tsv',
        'pathology_detail.tsv'
    ]
    
    data_dict = {}
    data_path = Path(data_dir)
    
    # Check if directory exists
    if not data_path.exists():
        raise FileNotFoundError(f"Directory not found: {data_dir}")
    
    # Load each file
    for file_name in file_names:
        file_path = data_path / file_name
        
        if file_path.exists():
            try:
                # Load TSV file (tab-separated values)
                df = pd.read_csv(file_path, sep='\t', low_memory=False)
                
                # Store with simplified name (without .tsv extension)
                key = file_name.replace('.tsv', '')
                data_dict[key] = df
                
                print(f"✓ Loaded {file_name}: {df.shape[0]} rows, {df.shape[1]} columns")
                
            except Exception as e:
                print(f"✗ Error loading {file_name}: {str(e)}")
        else:
            print(f"⚠ Warning: {file_name} not found in {data_dir}")
    
    return data_dict


def merge_clinical_data(data_dict: Dict[str, pd.DataFrame], 
                        merge_key: str = 'case_id') -> pd.DataFrame:
    """
    Merge multiple clinical dataframes into a single dataframe.
    
    Performs left joins on the specified key (default: case_id) to combine
    all clinical data sources into one comprehensive dataframe.
    
    Parameters
    ----------
    data_dict : Dict[str, pd.DataFrame]
        Dictionary of dataframes returned by load_clinical_files()
    merge_key : str, optional
        Column name to merge on (default: 'case_id')
        
    Returns
    -------
    pd.DataFrame
        Merged dataframe containing all clinical information
        
    Notes
    -----
    - Uses left joins, starting with 'clinical' as the base
    - Duplicate columns (except merge_key) are suffixed with source name
    - Missing data will be NaN where patients don't have records in all files
    
    Examples
    --------
    >>> data_dict = load_clinical_files('data/raw/')
    >>> merged_df = merge_clinical_data(data_dict)
    >>> print(f"Merged shape: {merged_df.shape}")
    """
    # Check if we have any data
    if not data_dict:
        raise ValueError("data_dict is empty. Load data first using load_clinical_files()")
    
    # Start with clinical data as the base (most comprehensive)
    if 'clinical' in data_dict:
        merged_df = data_dict['clinical'].copy()
        print(f"Starting with clinical data: {merged_df.shape}")
    else:
        # If no clinical file, start with the first available dataframe
        first_key = list(data_dict.keys())[0]
        merged_df = data_dict[first_key].copy()
        print(f"Starting with {first_key} data: {merged_df.shape}")
    
    # Merge each additional dataframe
    for name, df in data_dict.items():
        if name == 'clinical' or name == list(data_dict.keys())[0]:
            continue  # Skip the base dataframe
        
        if merge_key in df.columns:
            # Perform left join
            before_cols = merged_df.shape[1]
            merged_df = merged_df.merge(df, on=merge_key, how='left', suffixes=('', f'_{name}'))
            added_cols = merged_df.shape[1] - before_cols
            
            print(f"Merged {name}: added {added_cols} columns")
        else:
            print(f"⚠ Warning: '{merge_key}' not found in {name}, skipping...")
    
    print(f"\nFinal merged shape: {merged_df.shape[0]} rows, {merged_df.shape[1]} columns")
    
    return merged_df


def validate_data(df: pd.DataFrame, required_columns: Optional[list] = None) -> bool:
    """
    Perform basic validation checks on the dataframe.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to validate
    required_columns : list, optional
        List of column names that must be present
        
    Returns
    -------
    bool
        True if all validation checks pass, False otherwise
        
    Examples
    --------
    >>> is_valid = validate_data(df, required_columns=['case_id', 'age_at_diagnosis'])
    """
    print("\n" + "="*60)
    print("DATA VALIDATION REPORT")
    print("="*60)
    
    is_valid = True
    
    # Check 1: DataFrame is not empty
    if df.empty:
        print("✗ FAIL: DataFrame is empty")
        is_valid = False
    else:
        print(f"✓ PASS: DataFrame has {df.shape[0]} rows")
    
    # Check 2: Required columns present
    if required_columns:
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"✗ FAIL: Missing required columns: {missing_cols}")
            is_valid = False
        else:
            print(f"✓ PASS: All required columns present")
    
    # Check 3: Report missing data
    missing_counts = df.isnull().sum()
    missing_pct = (missing_counts / len(df)) * 100
    
    print(f"\nMissing Data Summary:")
    print(f"  Total columns: {len(df.columns)}")
    print(f"  Columns with missing data: {(missing_counts > 0).sum()}")
    
    if (missing_counts > 0).any():
        print(f"\n  Top 5 columns with most missing values:")
        top_missing = missing_pct[missing_pct > 0].sort_values(ascending=False).head()
        for col, pct in top_missing.items():
            print(f"    - {col}: {pct:.1f}%")
    
    # Check 4: Duplicate rows
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        print(f"\n⚠ WARNING: Found {dup_count} duplicate rows")
    else:
        print(f"\n✓ PASS: No duplicate rows found")
    
    print("="*60 + "\n")
    
    return is_valid


if __name__ == "__main__":
    # Example usage
    print("Data Loader Module for Multiple Myeloma Analysis")
    print("="*60)
    print("\nExample usage:")
    print("  from src.data_loader import load_clinical_files, merge_clinical_data")
    print("  data_dict = load_clinical_files('data/raw/')")
    print("  merged_df = merge_clinical_data(data_dict)")
    print("  validate_data(merged_df, required_columns=['case_id'])")
