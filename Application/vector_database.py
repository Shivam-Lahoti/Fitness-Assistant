from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import os

# Initialize Elasticsearch and SentenceTransformer
es = Elasticsearch(
    "http://localhost:9200",  
   
)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Define the index name
INDEX_NAME = "fitness-vector-search"


def create_index():
    """
    Create an Elasticsearch index with vector search support.
    """
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(
            index=INDEX_NAME,
            body={
                "mappings": {
                    "properties": {
                        "embedding": {
                            "type": "dense_vector",
                            "dims": 384
                        },
                        "text": {
                            "type": "text"
                        }
                    }
                }
            }
        )
        print(f"Index '{INDEX_NAME}' created successfully!")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")


def load_data(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def add_to_index(data):

    embeddings = model.encode(data).tolist()
    for i, (text, embedding) in enumerate(zip(data, embeddings)):
        es.index(
            index=INDEX_NAME,
            id=i,
            body={
                "text": text,
                "embedding": embedding
            }
        )
    print(f"Added {len(data)} items to the index '{INDEX_NAME}'.")


def query_index(query_text, top_k=5):

    query_embedding = model.encode([query_text]).tolist()[0]
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

    # Step 2: Load data from the `data` folder
    data_file = os.path.join("data", "fitness_data.txt")
    if os.path.exists(data_file):
        data = load_data(data_file)
        if data:
            print(f"Loaded {len(data)} lines of text from {data_file}")
            # Step 3: Add data to the Elasticsearch index
            add_to_index(data)
        else:
            print("No data found in the file.")
    else:
        print(f"Data file '{data_file}' not found.")

    # Step 4: Query the index
    query = "Best exercises for beginners"
    results = query_index(query)
    print("Query Results:")
    for result in results:
        print(f"Text: {result['text']}, Score: {result['score']}")
