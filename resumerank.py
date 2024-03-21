
from flask import Flask, session, jsonify, request, redirect, url_for, render_template, flash, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import dotenv_values
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import logging
import os
from bson import json_util


# Import utility functions
from database_utils import get_database_collections, get_or_create_database_collection, upload_resumes_with_embedding, upload_jd_with_embedding
from doc_processing import process_jd , process_resumes, process_json
from vector_operations import generate_embeddings, resumes_ranking, setup_vector_indexing, ensure_vector_index_exists

# Correctly import configuration and client initialization functions
from config import load_config, initialize_clients

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MyFlaskApp')

# Load configuration
env_path = "/home/eaint/projects/Self/azure/mongodb/example.env"
config = load_config(env_path)

# Initialize clients
aoai_client, document_analysis_client, mongo_client, model = initialize_clients(config)

# Initialize the Flask app
app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=config['flask_secret_key'],
    UPLOAD_FOLDER=os.path.join(os.getcwd(), 'uploads'),
    ALLOWED_EXTENSIONS={'pdf'},
)

# Retrieve database and collections
db, jobs_collections, applicants_resume = get_database_collections(mongo_client)

# If they don't exist, they'll be created
db, jobs_collections = get_or_create_database_collection(mongo_client, "JobDatabase", "jobs_collections")
_, applicants_resumes = get_or_create_database_collection(mongo_client, "JobDatabase", "applicants_resumes")

# Initialize the Document Analysis Client
doc_int_endpoint = config["doc_int_endpoint"]
doc_int_key = config["doc_int_key"]
document_analysis_client = DocumentAnalysisClient(endpoint=doc_int_endpoint, credential=AzureKeyCredential(doc_int_key))

# Define allowed file extensions
def allowed_file(filename):
    """Check if the file's extension is allowed."""
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload_job', methods=['GET', 'POST'])
def upload_job_description():
    if request.method == 'POST':
        # The rest of the file handling code remains the same
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Processing the file and saving to the 'jobs_collections' collection
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            try:
                jd_doc = process_jd(file_path, document_analysis_client)
                
                # generate_embeddings(process_jd) returns embeddings
                jd_embeddings = generate_embeddings(jd_doc, aoai_client, model)
                upload_jd_with_embedding(jobs_collections, jd_doc, jd_embeddings)
                flash('Job description processed and embeddings generated successfully')
            except Exception as e:
                logger.error(f'Error during jd processing or embedding generation for file {filename}: {e}', exc_info=True)
                flash('An error occurred during jd processing or embedding generation')
            
            flash('Job description uploaded successfully')
        else:
            flash('Invalid file or no file selected')
        return redirect(url_for('index'))

@app.route('/upload_resume', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        files = request.files.getlist('file')
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                try:
                    # Process each resume individually
                    resume_doc = process_resumes(file_path, document_analysis_client)  # Adjusted to handle a single file
                    if resume_doc:
                        # Generate embeddings for each processed resume
                        resume_embeddings = generate_embeddings(resume_doc, aoai_client, model)
                        if resume_embeddings:
                            # Upload each resume with its embeddings
                            upload_resumes_with_embedding(applicants_resumes, [resume_doc], [resume_embeddings])  # Adjust to accept lists
                            flash('Resume processed and embeddings generated successfully')
                            setup_vector_indexing(db)
                            ensure_vector_index_exists(db, 'applicants_resumes')
                            ensure_vector_index_exists(db, 'jobs_collections') 
                            ranked_resumes = resumes_ranking(db, 'jobs_collections', 'applicants_resumes', num_results=1)
                            final_resumes = process_json(ranked_resumes)
                            return final_resumes
                        else:
                            flash('Failed to generate embeddings for resume')
                    else:
                        flash('Failed to process resume')
    
                except Exception as e:
                    logger.error(f'Error during resume processing or embedding generation for file {filename}: {e}', exc_info=True)
            return redirect(url_for('display_results'))
        return redirect(url_for('index'))
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
@app.route('/display_results', methods=['GET', 'POST'])
def display_results():
    ranked_resumes = resumes_ranking(db, 'jobs_collections', 'applicants_resumes', num_results=1)
    final_resumes = process_json(ranked_resumes)
    return render_template('display_results.html', final_resumes=final_resumes)

@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5111)  # Consider setting debug=False for production