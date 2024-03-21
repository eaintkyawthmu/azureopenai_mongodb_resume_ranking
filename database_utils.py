import logging
import pymongo
import datetime
from vector_operations import setup_vector_indexing
from doc_processing import process_jd, process_resumes
from config import initialize_clients

logger = logging.getLogger('database_utils')

def get_mongo_client():
    """Initialize and return a MongoDB client instance based on loaded configuration."""
    _, _, mongo_client = initialize_clients(mongo_client)
    return mongo_client

def get_or_create_database_collection(client, database_name, collection_name):
    """Ensure the specified database and collection exist, create if not."""
    try:
        db = client[database_name]
        collection = db[collection_name]

        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            logger.info(f"Collection '{collection_name}' created.")
        else:
            logger.info(f"Collection '{collection_name}' already exists.")

        return db, collection
    except Exception as e:
        logger.error(f"An error occurred while accessing or creating the collection '{collection_name}': {e}")
        return None, None

def get_database_collections(mongo_client, database_name="JobDatabase"):
    """Get specified collections from the database."""
    try:
        db = mongo_client[database_name]
        jobs_collections = db['jobs_collections']
        applicants_resumes = db['applicants_resumes']
        return db, jobs_collections, applicants_resumes
    except Exception as e:
        logger.error(f"An error occurred while retrieving collections from '{database_name}': {e}")
        return None, None, None

def upload_jd_with_embedding(jobs_collections, jd_doc, jd_embeddings):
    """Upload a document and its embeddings to MongoDB."""
    try:
        jd_document = {
            "document_data": jd_doc,  # Any metadata or text associated with the document
            "contentVector": jd_embeddings,  # The generated embeddings for the document
            "created_at": datetime.datetime.now()  # Timestamp for the document upload
        }
        jd_result = jobs_collections.insert_one(jd_document)
        logger.info(f"Document with embeddings uploaded successfully: {jd_result.inserted_id}")
        return jd_result.inserted_id
    except pymongo.errors.BulkWriteError as e:
        logger.error(f"Failed to upload document with embeddings: {e.details}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while uploading document with embeddings: {e}")

def upload_resumes_with_embedding(applicants_resumes, resumes_docs, resumes_embeddings):
    """Upload documents and their embeddings to MongoDB."""
    # Assuming resumes_docs and resumes_embeddings are lists of equal length
    for doc, embedding in zip(resumes_docs, resumes_embeddings):
        try:
            res_document = {
                "document_data": doc,
                "contentVector": embedding,
                "created_at": datetime.datetime.now()
            }
            result = applicants_resumes.insert_one(res_document)
            logger.info(f"Document with embeddings uploaded successfully: {result.inserted_id}")
        except Exception as e:
            logger.error(f"An unexpected error occurred while uploading document with embeddings: {e}")

# if __name__ == "__main__":
#     #Just for testing purpose
#     logger.info("Testing database utilities module")

#     # Initialize MongoDB client
#     mongo_client = get_mongo_client()

#     # Create a new collection or ensure it exists
#     db_name = "JobDatabase"
#     collection_name = "ExampleCollection"
#     db, collection = get_or_create_database_collection(mongo_client, db_name, collection_name)
#     if db and collection:
#         logger.info(f"Successfully accessed or created collection: {collection_name} in database: {db_name}")
#     else:
#         logger.error("Failed to access or create the collection.")