from openai import OpenAI
from config import OPENAI_API_KEY

# This script was a test for embed response using the embeding 3 model
client = OpenAI(api_key=OPENAI_API_KEY)

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Hello from our RAG project"  
)
embedding = response.data[0].embedding
print("Embedding dimensions:", len(embedding))
print("First five values:")
print(embedding[:5])