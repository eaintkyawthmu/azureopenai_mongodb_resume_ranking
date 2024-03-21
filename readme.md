# Job Application Processing and Ranking System 

This repository contains the code for a system designed to process and rank job applications using Azure's AI for document analysis and MongoDB for data storage. The system extracts information from resumes and job descriptions, generates embeddings for textual content, and ranks resumes based on their relevance to a given job description.

It is a Flask application that processes and ranks resumes based on job descriptions. It uses Azure's Document Analysis Client for document processing, and a MongoDB database for storing job descriptions and resumes. The application also generates embeddings for the processed documents using a pre-trained model, and ranks resumes based on these embeddings.

## Features

- Upload job descriptions and resumes in PDF format.
- Process and store job descriptions and resumes in a MongoDB database.
- Generate embeddings for the processed documents using a pre-trained model.
- Rank resumes based on these embeddings.

## Installation

1. Clone the repository:
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
 You'll need to provide your Azure and MongoDB credentials.

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

1. Run the Flask application:
2. Open your web browser and navigate to `http://localhost:5111`.
3. Use the upload forms to upload job descriptions and resumes.
4. The application will process the documents, generate embeddings, and rank the resumes.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
