# Hackathon Project Evaluation System

## Overview

The Hackathon Project Evaluation System is designed to streamline the evaluation process for hackathon submissions. It includes modules for data ingestion, code review, and presentation screening, ensuring a comprehensive and fair assessment of each project.

## Features

- **Data Ingestion**: Validates and stores hackathon submissions, ensuring all required data is present.
- **Code Review**: Analyzes code quality, functionality, performance, security, testing, innovation, and technical complexity.
- **Presentation Screening**: Evaluates presentation content for clarity, relevance to themes, innovation, technical feasibility, sustainability, and overall impact.

## Installation

To set up the project, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/hackathon-evaluation.git
   cd hackathon-evaluation
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Data Ingestion

The `data_ingestion` module handles the validation and storage of hackathon submissions.

- **SubmissionHandler**: Manages the submission process.
- **DataValidator**: Validates the structure and content of submissions.
- **StorageService**: Stores valid submissions.

### Code Review

The `code_review` module evaluates the code quality and functionality of submissions.

- **ChunkExtractor**: Splits code into manageable chunks for review.
- **CodeAnalyser**: Analyzes code chunks based on predefined criteria.
- **GitHandler**: Clones repositories and retrieves file content.

### Presentation Screening

The `presentation_screening` module evaluates presentation content.

- **PresentationAnalyser**: Analyzes presentation files for clarity, relevance, and impact.
- **PresentationPreprocesser**: Downloads and preprocesses presentation files.
- **FileParser**: Parses presentation files to extract text and images.

## Running the System

1. **Data Ingestion**:
   ```bash
   python -m src.data_ingestion.submission_handler
   ```

2. **Code Review**:
   ```bash
   python -m src.code_review.chunker
   python -m src.code_review.code_analyser
   ```

3. **Presentation Screening**:
   ```bash
   python -m src.presentation_screening.evaluate_pitch
   ```

## Configuration

- **API Keys**: Ensure you have the necessary API keys for external services (e.g., Groq) configured in your environment.
- **Logging**: The system uses Python's logging module. Configure logging levels as needed.

## Contact

For any questions or issues, please open an issue on the GitHub repository or contact the maintainers directly.
