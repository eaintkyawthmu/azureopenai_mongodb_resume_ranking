# Handles loading of configurations and initialization of clients
import urllib
from dotenv import dotenv_values
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from openai import AzureOpenAI
import pymongo

def load_config(env_path):
    """Load environment variables from a specified .env file."""
    config = dotenv_values(env_path)
    return config

def initialize_clients(config):
    """Initialize AzureOpenAI, DocumentAnalysisClient, and MongoDB clients using the loaded configuration."""
    aoai_client = AzureOpenAI(
        api_key=config['openai_api_key'],
        azure_endpoint=config['openai_api_endpoint'],
        api_version=config['openai_api_version'],
    )

    model = config['openai_embeddings_model']
    
    document_analysis_client = DocumentAnalysisClient(
        endpoint=config["doc_int_endpoint"],
        credential=AzureKeyCredential(config["doc_int_key"])
    )

    mongo_conn = f"mongodb+srv://{urllib.parse.quote(config['cosmos_db_mongo_user'])}:{urllib.parse.quote(config['cosmos_db_mongo_pwd'])}@{config['cosmos_db_mongo_server']}?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
    mongo_client = pymongo.MongoClient(mongo_conn)

    return aoai_client, document_analysis_client, mongo_client, model