"""
Data Ingestion Module

This module handles the ingestion of hackathon submissions, including
validation of submission data and storage of valid submissions.

Exposed classes:
    - SubmissionHandler: Manages the submission process
    - DataValidator: Validates submission data
    - StorageService: Handles storage of valid submissions
"""

from .submission_handler import SubmissionHandler
from .data_validator import DataValidator
from .storage_service import StorageService

__all__ = ['SubmissionHandler', 'DataValidator', 'StorageService']