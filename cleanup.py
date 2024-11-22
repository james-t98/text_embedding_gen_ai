import subprocess
from utils.logger import Logging
from config import (
    INSTANCE,
    DATABASE
)

logger = Logging()

def delete_database_instance(instance_name: str):
    logger.info(f"Deleting database instance {instance_name}.")
    try:    
        instances = subprocess.check_output(["gcloud", "sql", "instances", "list", "--format=value(NAME)"], text=True).split()
        if instance_name in instances:
            deleted_database_instance = subprocess.check_output(
                ["gcloud", "sql", "instances", "delete", f"{instance_name}"]
            )
        else:
            logger.error("Cloud SQL Instance not found!")
    except subprocess.CalledProcessError as e:
        logger.error(f"Command to check if database exists failed with return code {e.returncode}\n")

    
    logger.info("Database instance deleted!\n")

def delete_database(database_name: str, instance_name: str):
    logger.info(f"Deleting database {database_name} from instance {instance_name}.")
    try:
        databases = (subprocess.check_output(["gcloud" , "sql" , "databases" , "list", f"--instance={instance_name}", "--format=value(NAME)"], text=True)).split()
        if database_name in databases:
            deleted_database = subprocess.check_output(
                ["gcloud", "sql", "databases", "delete", f"{database_name}", "--instance", f"{instance_name}"]
            )
        else:
            logger.error("Database not found!\n")
    except subprocess.CalledProcessError as e:
        logger.error(f"Command to check if database exists failed with return code {e.returncode}\n") 
    logger.info("Database deleted!\n")


def main():
    delete_database(DATABASE, INSTANCE)
    delete_database_instance(INSTANCE)
    

if __name__=="__main__":
    main()