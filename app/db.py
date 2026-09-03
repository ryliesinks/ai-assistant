import psycopg

from pgvector.psycopg import register_vector

from config import DATABASE_URL

# This function connects the database to Python which allows for the emed model to interact with database

def get_connection():

    connection = psycopg.connect(
        DATABASE_URL
    )

    register_vector(connection)

    return connection