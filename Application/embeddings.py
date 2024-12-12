from sentence_transformers import SentenceTransformer
import pinecone
import os

# Load the embedding model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def preprocess_data(data_path):
    with open(data_path, 'r') as file:
        texts = file.readlines()
    embeddings = model.encode(texts, show_progress_bar=True)
    return texts, embeddings

def index_data_to_pinecone(texts, embeddings, index_name='fitness-assistant'):
    pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment=os.getenv('PINECONE_ENVIRONMENT'))
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=len(embeddings[0]))
    index = pinecone.Index(index_name)
    for i, (text, embedding) in enumerate(zip(texts, embeddings)):
        index.upsert([(str(i), embedding, {"text": text})])
    print("Data indexed successfully!")

