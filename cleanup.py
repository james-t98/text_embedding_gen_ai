import subprocess
from utils.logger import Logging
from config import (
    INSTANCE,
    DATABASE
)

logger = Logging()

def delete_database_instance(instance_name: str):
    logger.info(f"Deleting database instance {instance_name}.")
    deleted_database_instance = subprocess.check_output(
        ["gcloud", "sql", "instances", "delete", f"{instance_name}"]
    )
    logger.info("Database instance deleted!\n")

def delete_database(database_name: str, instance_name: str):
    logger.info(f"Deleting database {database_name} from instance {instance_name}.")
    deleted_database = subprocess.check_output(
        ["gcloud", "sql", "databases", "delete", f"{database_name}", "--instance", f"{instance_name}"]
    )
    logger.info("Database deleted!\n")


def main():
    delete_database(DATABASE, INSTANCE)
    delete_database_instance(INSTANCE)
    

if __name__=="__main__":
    main()