"""
Input validation utilities for file uploads and analysis.
Ensures secure and valid input processing.
"""

import os
import zipfile


def validate_upload(file, max_size=50*1024*1024):
    """
    Validate uploaded file before processing.
    
    Args:
        file: File object from Flask request
        max_size (int): Maximum allowed file size in bytes
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not file:
        return False, "No file provided"
    
    if file.filename == '':
        return False, "No file selected"
    
    if not file.filename.endswith('.zip'):
        return False, "Only .zip files are allowed"
    
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size == 0:
        return False, "File is empty"
    
    if file_size > max_size:
        return False, f"File too large. Maximum size is {max_size / (1024*1024):.0f} MB"
    
    return True, None


def validate_file_size(file_path, max_size=50*1024*1024):
    """
    Validate file size on disk.
    
    Args:
        file_path (str): Path to the file
        max_size (int): Maximum allowed file size in bytes
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not os.path.exists(file_path):
        return False, "File not found"
    
    file_size = os.path.getsize(file_path)
    
    if file_size == 0:
        return False, "File is empty"
    
    if file_size > max_size:
        return False, f"File too large. Maximum size is {max_size / (1024*1024):.0f} MB"
    
    return True, None


def validate_zip_contents(zip_path):
    """
    Validate zip file contents for security issues.
    
    Args:
        zip_path (str): Path to zip file
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not zipfile.is_zipfile(zip_path):
        return False, "Invalid zip file format"
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                if member.startswith('/') or '..' in member:
                    return False, "Zip file contains invalid paths (path traversal detected)"
    except Exception as e:
        return False, f"Failed to read zip file: {str(e)}"
    
    return True, None
