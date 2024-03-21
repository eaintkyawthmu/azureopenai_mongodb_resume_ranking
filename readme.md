```markdown
# Job Application Processing and Ranking System

This repository contains the code for a system designed to process and rank job applications using Azure's AI for document analysis and MongoDB for data storage. The system extracts information from resumes and job descriptions, generates embeddings for textual content, and ranks resumes based on their relevance to a given job description.

## Overview

The system is composed of several key components:

- `config.py`: Handles loading of configurations and initialization of clients for Azure AI services and MongoDB.
- `database_utils.py`: Contains utility functions for interacting with MongoDB, including database and collection initialization, and uploading documents along with their embeddings.
- `doc_processing.py`: Manages the processing of job descriptions (JD) and resumes, extracting textual content using Azure's Document Analysis.
- `vector_operations.py`: Responsible for generating embeddings for textual content, setting up vector search indexes in MongoDB, and ranking resumes based on their similarity to job descriptions.

## Features

- Text extraction from resumes and job descriptions using Azure Document Analysis.
- Generation of textual embeddings using Azure OpenAI.
- Storage of documents and embeddings in MongoDB with support for vector search indexing.
- Ranking of resumes based on their relevance to a job description.

## Setup

### Requirements

- Python 3.8+
- Azure account with access to Azure AI services.
- MongoDB account (Atlas recommended).

### Installation

1. Clone this repository.
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Set up a `.env` file with your Azure and MongoDB credentials:

```
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_ENDPOINT=your_openai_api_endpoint
OPENAI_API_VERSION=your_openai_api_version
OPENAI_EMBEDDINGS_MODEL=your_openai_embeddings_model
DOC_INT_ENDPOINT=your_document_intelligence_endpoint
DOC_INT_KEY=your_document_intelligence_key
COSMOS_DB_MONGO_USER=your_mongodb_username
COSMOS_DB_MONGO_PWD=your_mongodb_password
COSMOS_DB_MONGO_SERVER=your_mongodb_server
```

### Usage

1. Initialize the system by loading the configuration and setting up the database and AI clients:

```python
from config import load_config, initialize_clients

config = load_config(".env")
aoai_client, document_analysis_client, mongo_client, model = initialize_clients(config)
```

2. Process job descriptions and resumes using the `doc_processing` module.
3. Use the `database_utils` module to upload documents and their embeddings to MongoDB.
4. Rank resumes for a given job description using the `vector_operations` module.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
