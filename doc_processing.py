import logging
import time
from vector_operations import resumes_ranking
import json
from bson.json_util import dumps, LEGACY_JSON_OPTIONS

logger = logging.getLogger('doc_processing')

def process_jd(file_path, document_analysis_client):
    """Process resume PDF to extract text using Azure Document Intelligence."""
    try:
        #upload resume pdf
        with open(file_path, "rb") as f:
            poller = document_analysis_client.begin_analyze_document("prebuilt-document", document=f, locale="en-US")
        doc_components = poller.result()
        document = doc_components.content
        return document
    except Exception as e:
        logger.error(f"Error processing job descriptions: {e}")
        return None


def process_resumes(file_path, document_analysis_client):
    """Process resume PDF to extract text using Azure Document Intelligence."""
    try:
        #upload resume pdf
        with open(file_path, "rb") as f:
            poller = document_analysis_client.begin_analyze_document("prebuilt-document", document=f, locale="en-US")
        doc_components = poller.result()
        document = doc_components.content
        return document
    except Exception as e:
        logger.error(f"Error processing resume: {e}")
        return None

def process_json(json_docs):
    """Process a cursor to extract text from 'document_data' and serialize to JSON.

    Parameters:
    - cursor: The cursor returned by the resumes_ranking function.

    Returns:
    A JSON string representing the list of extracted 'document_data' fields.
    """
    result_docs = []
    try:
        for result in json_docs:
            similarity_score = result['similarityScore']
            document_data = result['document']['document_data']
            logger.info(f"Similarity score: {similarity_score} , Document data: {document_data}")
            result_docs.append(document_data)
        return result_docs

        
    except Exception as e:
        logger.error(f"Error processing resume JSON: {e}")
        return None
        
# def export_doc(serialized_docs):
#     # Load the JSON string to access the text data
#     text_data = json.loads(serialized_docs)

#     # Assuming 'text_data' is a list of text strings
#     text_content = "\n".join(text_data)  # Join text strings with newlines

#     # Export the text content to a .txt file
#     try:
#         output_file_path = "./uploads/ranked_resumes.txt"
#         with open(output_file_path, "w") as f:
#             f.write(text_content)
#         logger.info(f"Text exported to {output_file_path}")
#     except Exception as e:
#         logger.error(f"Error exporting text to .txt file: {e}")
