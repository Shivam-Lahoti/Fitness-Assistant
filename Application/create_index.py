from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Define the index name
INDEX_NAME = "fitness-vector-search"

# Create the index with vector search support
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
