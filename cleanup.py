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
    print(deleted_database_instance)
    logger.info("Database instance deleted!\n")

async def delete_database(database_name: str, instance_name: str):
    logger.info(f"Deleting database {database_name} from instance {instance_name}.")
    deleted_database = subprocess.check_output(
        ["gcloud", "sql", "databases", "delete", f"{database_name}", "--instance", f"{instance_name}"]
    )
    print(deleted_database)
    logger.info("Database deleted!\n")


async def main():
    await delete_database_instance(DATABASE)
    await delete_database(DATABASE, INSTANCE)
    

if __name__=="__main__":
    main()