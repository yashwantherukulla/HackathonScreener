"""
Data Validator Module

This module contains the DataValidator class, which is responsible for
validating the structure and content of hackathon submissions.
"""

import re
import logging
from typing import Dict, Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class DataValidator:
    """
    Validates hackathon submission data.

    This class provides methods to check the structure and content of
    submission data, ensuring it meets the required criteria.
    """

    def __init__(self):
        """Initialize the DataValidator."""
        self.required_fields = ['team_name', 'github_url', 'presentation_file']

    async def validate(self, data: Dict[str, Any]) -> bool:
        """
        Validate the submission data.

        This method checks for the presence of required fields and validates
        the content of each field.

        Args:
            data (Dict[str, Any]): The submission data to validate.

        Returns:
            bool: True if the data is valid, False otherwise.
        """
        try:
            if not all(field in data for field in self.required_fields):
                logger.warning(f"Missing required fields in submission: {data.get('id', 'Unknown ID')}")
                return False

            if not self._validate_team_name(data['team_name']):
                return False

            if not self._validate_github_url(data['github_url']):
                return False

            if not self._validate_presentation_file(data['presentation_file']):
                return False

            logger.info(f"Submission validated successfully: {data.get('id', 'Unknown ID')}")
            return True
        except Exception as e:
            logger.error(f"Error validating submission: {str(e)}")
            return False

    def _validate_team_name(self, team_name: str) -> bool:
        """Validate the team name."""
        if not 3 <= len(team_name) <= 50:
            logger.warning(f"Invalid team name length: {team_name}")
            return False
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', team_name):
            logger.warning(f"Invalid characters in team name: {team_name}")
            return False
        return True

    def _validate_github_url(self, url: str) -> bool:
        """Validate the GitHub URL."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc]) and result.netloc == 'github.com'
        except:
            logger.warning(f"Invalid GitHub URL: {url}")
            return False

    def _validate_presentation_file(self, file_data: Dict[str, Any]) -> bool:
        """Validate the presentation file data."""
        allowed_extensions = ['.ppt', '.pptx', '.pdf']
        if 'name' not in file_data or 'content' not in file_data:
            logger.warning("Missing name or content in presentation file data")
            return False
        if not any(f6ile_data['name'].lower().endswith(ext) for ext in allowed_extensions):
            logger.warning(f"Invalid presentation file type: {file_data['name']}")
            return False
        if len(file_data['content']) > 10 * 1024 * 1024:  # 10 MB limit
            logger.warning(f"Presentation file too large: {file_data['name']}")
            return False
        return True