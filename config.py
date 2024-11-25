from utils.logger import Logging

# General Project Variables
PROJECT_ID = "sublime-delight-436909-i0"
REGION = "europe-west4"

# CloudSQL PostgreSQL General Variables
INSTANCE = "langchain-quickstart-instance"
DATABASE = "langchain-quickstart-db"
STORAGE_BUCKET = "langchain-quickstart-bucket"
BLOB = "movies.csv"
TABLE_NAME = ""

# Vector Store Variables
VECTOR_TABLE_NAME = "movie_vector_table_samples_example"
CHAT_MEMORY_TABLE_NAME = "chat_memory_store_example"

USER = "postgres"
PASSWORD = "password"

EMBEDDING_MODEL = "textembedding-gecko@003"
LLM = "gemini-pro"

metadata = [
        "show_id",
        "type",
        "country",
        "date_added",
        "release_year",
        "rating",
        "duration",
        "listed_in",
    ]

def display_configuration():
    logger = Logging()
    logger.info("Logging environment variables:\n")
    logger.info(f"PROJECT_ID: {PROJECT_ID}")
    logger.info(f"REGION: {REGION}")
    logger.info(f"INSTANCE: {INSTANCE}")
    logger.info(f"DATABASE: {DATABASE}")
    logger.info(f"STORAGE_BUCKET: {STORAGE_BUCKET}")
    logger.info(f"TABLE_NAME: {TABLE_NAME}")
    logger.info(f"USER: {USER}")
    logger.info(f"PASSWORD: {PASSWORD}")
    logger.info(f"VECTOR_TABLE_NAME: {VECTOR_TABLE_NAME}")
    logger.info(f"CHAT_MEMORY_TABLE_NAME: {CHAT_MEMORY_TABLE_NAME}\n")