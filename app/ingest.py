from pathlib import Path
from embeddings import create_embeddings
from pgvector import Vector

from db import get_connection
import fitz


DOCUMENT_FOLDER = Path("documents")

# Function iterates through pages stroing data as text and parsing page number and content

def extract_pdf(path: Path):

    document = fitz.open(path)

    pages = []

    for page_number, page in enumerate(
        document,
        start=1
    ):

        text = page.get_text("text")

        if text.strip():

            pages.append({
                "page_number": page_number,
                "text": text
            })

    return pages

# This fucntion defines how big chunks are going to be and how to store them
def chunk_text(
    text: str,
    chunk_size: int = 400,
    overlap: int = 80
):
# This iterates through all of the wrods within the chunk and appends them together in a list
    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        )

        chunks.append(chunk)

        if end >= len(words):
            break

        start += chunk_size - overlap

    return chunks

# This is parsing the information out of the chunks that were stored previously
def process_pdf(path: Path):

    pages = extract_pdf(path)

    processed_chunks = []

    for page in pages:

        page_chunks = chunk_text(
            page["text"]
        )

        for index, content in enumerate(
            page_chunks
        ):

            processed_chunks.append({
                "source_name": path.name,
                "page_number": page["page_number"],
                "chunk_index": index,
                "content": content
            })

    return processed_chunks

# This turns the chunks in to embeds that will be stored as 1536 numbers in the database
def embed_chunks(chunks):

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embeddings = create_embeddings(texts)

    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        chunk["embedding"] = embedding

    return chunks

# This function saves the chunks and their embeddings to the database
def save_chunks(chunks):

    with get_connection() as conn:

        with conn.cursor() as cursor:

            for chunk in chunks:

                cursor.execute(
                    """
                    INSERT INTO document_chunks
                    (
                        source_name,
                        page_number,
                        chunk_index,
                        content,
                        embedding
                    )

                    VALUES (%s, %s, %s, %s, %s)
                    """,

                    (
                        chunk["source_name"],
                        chunk["page_number"],
                        chunk["chunk_index"],
                        chunk["content"],
                        Vector(chunk["embedding"])
                    )
                )

        conn.commit()

# This function orchestrates the entire ingestion process for a single document, from processing to saving to the database
def ingest_document(path: Path):

    print(f"Processing {path.name}")

    chunks = process_pdf(path)

    print(
        f"Created {len(chunks)} chunks"
    )

    chunks = embed_chunks(chunks)

    print("Created embeddings")

    save_chunks(chunks)

    print("Saved to database")


# This function iterates through all PDF documents in the designated folder and ingests them one by one
def ingest_all_documents():

    for path in DOCUMENT_FOLDER.glob("*.pdf"):

        ingest_document(path)


if __name__ == "__main__":

    ingest_all_documents()