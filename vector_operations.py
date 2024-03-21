# Handles operations related to vector indexing and searching
import logging
from config import initialize_clients
import numpy as np

logger = logging.getLogger('vector_operations')

def generate_embeddings(document, aoai_client, model):
    """Generate embeddings for using the specified embeddings model."""
    try:
        response = aoai_client.embeddings.create(input=document, model=model)  
        embeddings =response.model_dump()
        return embeddings['data'][0]['embedding']
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
    return None

def vector_indexing(db, collection_name):
    """
    Sets up vector search indexes for both the jobs and applicants resumes collections in Cosmos DB.
    """
    collections = ["jobs_collections", "applicants_resumes"]  
    
    for COLLECTION_NAME in collections:
        try:
            # Execute the command to create indexes for each collection
            response = db.command({
                'createIndexes': COLLECTION_NAME,
                'indexes': [
                    {
                        'name': 'VectorSearchIndex',
                        'key': {"contentVector": "cosmosSearch"},
                        'cosmosSearchOptions': {
                            'kind': 'vector-ivf',
                            'numLists': 1,
                            'similarity': 'COS',
                            'dimensions': 1536  # Ensure this matches your vector dimensions
                        }
                    }
                ]
            })
            logger.info(f"Vector search index created on {COLLECTION_NAME}. Response: {response}")
        except Exception as e:
            logger.error(f"Failed to create vector search index on {COLLECTION_NAME}: {e}")

def setup_vector_indexing(db):
    """Initial setup for vector search indexing on necessary collections."""
    COLLECTION_NAMES = ["applicants_resumes", "jobs_collections"]
    for collection_name in COLLECTION_NAMES:
        vector_indexing(db, collection_name)
    logger.info("Initial indexing setup completed successfully.")

def ensure_vector_index_exists(db, collection_name):
    """Ensure the vector search index exists on the specified collection."""
    collection = db[collection_name]
    indexes = collection.index_information()
    
    # Assuming 'VectorSearchIndex' is the name of your vector search index
    if 'VectorSearchIndex' not in indexes:
        logger.info(f"Vector search index not found on {collection_name}. Creating index.")
        vector_indexing(db, collection_name)
    else:
        logger.info(f"Vector search index already exists on {collection_name}.")

def resumes_ranking(db, jobs_collections, applicants_resumes, num_results):
    """
    Perform a vector search against a target collection using the embedding vector from a source document in a source collection.

    Parameters:
    - db: The MongoDB database connection.
    - source_collection_name: The name of the collection containing the source document.
    - target_collection_name: The name of the collection to search against.
    - source_document_id: The ID of the source document whose embedding vector will be used for searching.
    - num_results: The number of search results to return.

    Returns:
    A list of search results from the target collection most similar to the source document's embedding.
    """
    logging.info(f"Performing vector search using vector from {jobs_collections}")

    # Fetch the embedding vector from the source document
    job_embedding = db.get_collection("jobs_collections").find_one({"contentVector": {"$exists": True}})["contentVector"]
    
    pipeline = [
        {
            '$search': {
                "cosmosSearch": {
                    "vector": job_embedding,
                    "path": "contentVector",
                    "k": num_results
                },
                "returnStoredSource": True }},
        {'$project': { 'similarityScore': { '$meta': 'searchScore' }, 'document' : '$$ROOT' } }
    ]

    collection = db.get_collection(applicants_resumes)
    cursor = collection.aggregate(pipeline)
    json_docs = []
    for doc in cursor:
        json_docs.append({
            'similarityScore': doc['similarityScore'],
            'document': doc['document']
        })
    return json_docs

if __name__ == "__main__":
    aoai_client, document_analysis_client, mongo_client, model = initialize_clients()
    db = mongo_client['JobDatabase']
    setup_vector_indexing(db)