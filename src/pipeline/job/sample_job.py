# sample_job.py
import math
from dagster import op, job
from src.utils.logger_config import LoggerConfigurator

# Instantiating LoggerConfigurator automatically configures logging.
logger = LoggerConfigurator.get_dagster_logger()


@op
def get_message():
    return "Hello, Dagster!"


@op
def print_message(message: str):
    logger.info(message)
    for counter in range(1, 1001):
        logger.info(f"Counter: {counter}, Log: {math.log(counter)}")
    # for counter in range(1, 11):
    #     logger.debug(f"Counter: {counter}, Log: {math.log(counter)}")


@job
def hello_job():
    # Compose the ops: get the message and pass it to print_message.
    message = get_message()
    print_message(message)
