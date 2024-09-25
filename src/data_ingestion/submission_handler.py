"""
Submission Handler Module

This module contains the SubmissionHandler class, which manages the process
of accepting and processing hackathon submissions.
"""

import logging
from typing import Dict, Any
from .data_validator import DataValidator
from storage_service import StorageService
from typing import List

logger = logging.getLogger(__name__)

class SubmissionHandler:
    """
    Handles the submission process for hackathon entries.

    This class coordinates the validation and storage of submission data,
    ensuring that only valid submissions are processed and stored.
    """

    def __init__(self, validator: DataValidator, storage: StorageService):
        """
        Initialize the SubmissionHandler with validator and storage services.

        Args:
            validator (DataValidator): The validator to use for submission data.
            storage (StorageService): The storage service to use for valid submissions.
        """
        self.validator = validator
        self.storage = storage

    async def process_submission(self, submission_data: Dict[str, Any]) -> bool:
        """
        Process a single submission.

        This method validates the submission data and, if valid, stores it.

        Args:
            submission_data (Dict[str, Any]): The submission data to process.

        Returns:
            bool: True if the submission was successfully processed and stored, False otherwise.
        """
        try:
            if await self.validator.validate(submission_data):
                await self.storage.store(submission_data)
                logger.info(f"Submission processed successfully: {submission_data.get('id', 'Unknown ID')}")
                return True
            else:
                logger.warning(f"Invalid submission: {submission_data.get('id', 'Unknown ID')}")
                return False
        except Exception as e:
            logger.error(f"Error processing submission: {str(e)}")
            return False

    async def bulk_process_submissions(self, submissions: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Process multiple submissions in bulk.

        This method attempts to process each submission in the provided list.

        Args:
            submissions (List[Dict[str, Any]]): A list of submission data to process.

        Returns:
            Dict[str, int]: A dictionary containing counts of successful, failed, and total processed submissions.
        """
        results = {
            "successful": 0,
            "failed": 0,
            "total": len(submissions)
        }

        for submission in submissions:
            if await self.process_submission(submission):
                results["successful"] += 1
            else:
                results["failed"] += 1

        logger.info(f"Bulk processing complete. Results: {results}")
        return results