# Use the official Neo4j Docker image
FROM neo4j:latest

# Set the Neo4j username and password
ENV NEO4J_AUTH=neo4j/neo4jpasswd

# Expose the Neo4j ports
EXPOSE 7474 7473 7687
