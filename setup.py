import subprocess
from utils.logger import Logging
from utils.loader import get_CSVLoader
from utils.prompt_engineering import init_prompts
from langchain_google_cloud_sql_pg import PostgresEngine, PostgresChatMessageHistory
from langchain_google_vertexai import VertexAIEmbeddings, VertexAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_google_cloud_sql_pg import PostgresVectorStore
from langchain_google_cloud_sql_pg import Column
import uuid
from config import (
    PROJECT_ID,
    REGION,
    INSTANCE,
    DATABASE,
    PASSWORD, 
    metadata,
    EMBEDDING_MODEL,
    USER,
    LLM,
    VECTOR_TABLE_NAME,
    CHAT_MEMORY_TABLE_NAME
)

logger = Logging()
loader = None
embedding_service = None
pg_engine = None
vector_store = None
llm = None
chat_history = None
rag_chain = None

def create_database_instance(instance_name: str, region: str, password: str):
    logger.info("Creating new Postgres Cloud SQL Instance...")
    created_database = (subprocess.check_output(["gcloud" , "sql" , "instances" , 
                                                 "create", f"{instance_name}", "--database-version=POSTGRES_15",
                                                 "--region", f"{region}", "--cpu=1", "--memory=4GB",
                                                 "--root-password", f"{password}", 
                                                 "--database-flags=cloudsql.iam_authentication=On"]))
    logger.info("Postgres Cloud SQL Instance created!\n")
    pass

def database_instance_exists(instance_name: str):
    logger.info("Checking if Cloud SQL Instance exists...")   
    try:    
        instances = subprocess.check_output(["gcloud", "sql", "instances", "list", "--format=value(NAME)"], text=True).split()
        if instance_name in instances:
            logger.info("Found existing Postgres Cloud SQL Instance!\n")
        else:
            logger.warning("Cloud SQL Instance not found!")
            # Ask if user would like to create instance?
            create_db_instance = input("Would you like to create a new Cloud SQL Instance? (y/n): ")
            if create_db_instance.lower() == "y":
                create_database_instance(INSTANCE, REGION, PASSWORD)
            else:
                logger.info("Exiting...\n")
                exit()    
    except subprocess.CalledProcessError as e:
        logger.error(f"Command to check if database exists failed with return code {e.returncode}\n")

def create_database(database_name: str, instance_name: str):
    logger.info("Creating new Cloud SQL Database...")
    created_database = (subprocess.check_output(["gcloud" , "sql" , "databases" , "create", f"{database_name}", "--instance", f"{instance_name}"]))
    logger.info("Cloud SQL Database created!\n")

def database_exists(database_name: str, instance_name: str):
    logger.info("Checking if Cloud SQL Database exists...")
    try:
        databases = (subprocess.check_output(["gcloud" , "sql" , "databases" , "list", f"--instance={instance_name}", "--format=value(NAME)"], text=True)).split()
        if database_name not in databases:
            logger.info("Database not found!\n")
            create_db = input("Would you like to create a new Postgres Cloud SQL Database? (y/n): ")
            if create_db.lower() == "y":
               create_database(DATABASE, INSTANCE)
            else:
                logger.info("Exiting...\n")
                exit()
        else:
            logger.info("Database found!\n")
    except subprocess.CalledProcessError as e:
        logger.error(f"Command to check if database exists failed with return code {e.returncode}\n")

def define_embedding_service(model_name: str,project_id: str) -> VertexAIEmbeddings:
    logger.info("Defining embedding service...")
    embedding_model = VertexAIEmbeddings(
        model_name=model_name,
        project=project_id,
    )
    logger.info("Embedding service defined!\n")
    return embedding_model

def define_pg_engine(project_id: str, instance: str, region: str, database: str, user: str, password: str) -> PostgresEngine:
    logger.info("Defining Postgres Engine Object...")
    pg_engine = PostgresEngine.from_instance(
        project_id=project_id,
        instance=instance,
        region=region,
        database=database,
        user=user,
        password=password,
    )
    logger.info("Postgres Engine defined!\n")
    return pg_engine

def get_vector_store(pg_engine: PostgresEngine, embeddings_service: VertexAIEmbeddings, vector_table_name: str) -> PostgresVectorStore:
    # vector size [ 768 ]
    # overwrite_existing = [True, False]
    logger.info("Retrieving vector store...")
    vector_store = PostgresVectorStore.create_sync(
        engine=pg_engine,
        embedding_service=embeddings_service,
        table_name=vector_table_name,
        metadata_columns=[
            "show_id",
            "type",
            "country",
            "date_added",
            "release_year",
            "duration",
            "listed_in",
        ],
    )
    logger.info("Vector store retrieved!\n")
    return vector_store

def add_vector_documents(documents: list[str], vector_store: PostgresVectorStore) -> PostgresVectorStore:
    logger.info("Adding documents to vector store...")
    ids = [str(uuid.uuid4()) for _ in range(len(documents))]
    vector_store.add_documents(documents=documents, ids=ids)
    logger.info("Documents added to vector store!\n")
    return vector_store

# TODO: Implement adding a single new document to the vector store.
def add_vector_document(document: str, vector_store: PostgresVectorStore) -> PostgresVectorStore:
    logger.info("Adding document to vector store...")
    id = str(uuid.uuid4())
    vector_store.add_documents(documents=[document], ids=[id])
    logger.info("Document added to vector store!\n")
    pass

def create_chat_history(pg_engine: PostgresEngine, session_id: str, message_table_name: str) -> PostgresChatMessageHistory:
    logger.info("Creating chat history...")
    chat_history = PostgresChatMessageHistory.create_sync(
        pg_engine,
        session_id=session_id,
        table_name=message_table_name,
    )
    logger.info("Chat history created!\n")
    return chat_history

def get_llm(model_name: str, project_id: str) -> VertexAI:
    logger.info("Getting LLM...")
    llm = VertexAI(model_name=model_name, project=project_id)
    logger.info("LLM retrieved!\n")
    return llm

def prompt_model(rag_chain: ConversationalRetrievalChain, prompt: str, chat_history: PostgresChatMessageHistory) -> str:
    return rag_chain({"question": prompt, "chat_history": chat_history})["answer"]

def run_setup(number_documents: int, file_path: str, chat_session_id: str): 
    database_instance_exists(INSTANCE)
    database_exists(DATABASE, INSTANCE)

    loader = get_CSVLoader(file_path, metadata)
    documents = loader.load()
    if number_documents > 0:
        documents = documents[:number_documents]

    embedding_service = define_embedding_service(EMBEDDING_MODEL, PROJECT_ID)
    pg_engine = define_pg_engine(PROJECT_ID, INSTANCE, REGION, DATABASE, USER, PASSWORD)

    pg_engine.init_vectorstore_table(
        VECTOR_TABLE_NAME,
        vector_size=768,
        metadata_columns=[
            Column("show_id", "VARCHAR", nullable=True),
            Column("type", "VARCHAR", nullable=True),
            Column("country", "VARCHAR", nullable=True),
            Column("date_added", "VARCHAR", nullable=True), 
            Column("release_year", "VARCHAR", nullable=True),
            Column("rating", "VARCHAR", nullable=True),
            Column("duration", "VARCHAR", nullable=True),
            Column("listed_in", "VARCHAR", nullable=True),
        ],
        overwrite_existing=True, 
    )

    vector_store = get_vector_store(
        pg_engine=pg_engine,
        embeddings_service=embedding_service,
        vector_table_name=VECTOR_TABLE_NAME
    )

    vector_store = add_vector_documents(documents, vector_store)
    pg_engine.init_chat_history_table(table_name=CHAT_MEMORY_TABLE_NAME)

    chat_history = create_chat_history(pg_engine, chat_session_id, CHAT_MEMORY_TABLE_NAME)
    chat_history.clear()

    # Create SE Methodology
    # Create a method to use vector store as retriever or another retriever
    # Def get_retriever() -> RetrieverObject:
    retriever = vector_store.as_retriever(
        search_type="mmr", search_kwargs={"k": 3, "lambda_mult": 0.8}
    )

    llm = get_llm(LLM, PROJECT_ID)

    # Update this to non-depricated memory buffer
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        chat_memory=chat_history,
        output_key="answer",
        memory_key="chat_history",
        return_messages=True,
    )

    init_prompt, condensed_question_prompt = init_prompts()

    return llm, retriever, memory, init_prompt, condensed_question_prompt, chat_history, vector_store