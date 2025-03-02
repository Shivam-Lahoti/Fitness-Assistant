# Use the official Elasticsearch image
FROM docker.elastic.co/elasticsearch/elasticsearch:8.10.1

# Expose the Elasticsearch port
EXPOSE 9200

# Set environment variables
ENV discovery.type=single-node

# Default command to run Elasticsearch
CMD ["bin/elasticsearch"]
