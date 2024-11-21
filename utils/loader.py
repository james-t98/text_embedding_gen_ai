from utils.logger import Logging
from langchain_community.document_loaders.csv_loader import CSVLoader
logger = Logging()

def get_CSVLoader(file_path: str, metadata_columns: list[str]) -> CSVLoader:
    logger.info(f"Attempting to load CSV Data from: {file_path}. With columns {metadata_columns}")
    return CSVLoader(file_path=file_path, metadata_columns=metadata_columns)