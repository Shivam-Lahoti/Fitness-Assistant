import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Pinecone index name
PINECONE_INDEX_NAME = "fitness-assistant"

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Data paths
RAW_DATA_PATH = "data/fitness_data.csv"
CLEANED_DATA_PATH = "data/cleaned_fitness_data.txt"

# Evaluation settings
TOP_K = 5  # Number of top results to return
