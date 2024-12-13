import os
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

# Initialize Elasticsearch and embedding model
es = Elasticsearch("http://localhost:9200")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Elasticsearch index name
INDEX_NAME = "fitness-vector-search"

# Function to create the Elasticsearch index
def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(
            index=INDEX_NAME,
            body={
                "mappings": {
                    "properties": {
                        "embedding": {"type": "dense_vector", "dims": 384},
                        "text": {"type": "text"}
                    }
                }
            }
        )
        print(f"Index '{INDEX_NAME}' created successfully.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")

# Function to load data from a .txt file
def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

# Function to index data into Elasticsearch
def add_to_index(data):
    embeddings = model.encode(data).tolist()
    for i, (text, embedding) in enumerate(zip(data, embeddings)):
        doc_id = f"{hash(text)}"  # Use hash of the text as a unique ID
        es.index(
            index=INDEX_NAME,
            id=doc_id,
            body={"text": text, "embedding": embedding}
        )
    print(f"Indexed {len(data)} documents successfully.")

# Function to query the Elasticsearch index
def query_index(query, top_k=5):
    query_embedding = model.encode([query]).tolist()[0]
    response = es.search(
        index=INDEX_NAME,
        body={
            "size": top_k,
            "_source": ["text"],
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": query_embedding}
                    }
                }
            }
        }
    )
    return [
        {"text": hit["_source"]["text"], "score": hit["_score"]}
        for hit in response["hits"]["hits"]
    ]

if __name__ == "__main__":
    # Step 1: Create Elasticsearch index
    create_index()

    # Step 2: Load and index data from all `.txt` files in the `data` folder
    data_folder = "data"
    if os.path.exists(data_folder):
        txt_files = [f for f in os.listdir(data_folder) if f.endswith(".txt")]
        if txt_files:
            for file_name in txt_files:
                file_path = os.path.join(data_folder, file_name)
                print(f"Processing file: {file_name}")
                data = load_data(file_path)
                if data:
                    print(f"Loaded {len(data)} lines from {file_name}.")
                    add_to_index(data)
                else:
                    print(f"No data found in {file_name}.")
        else:
            print("No .txt files found in the 'data' folder.")
    else:
        print(f"Data folder '{data_folder}' not found.")


