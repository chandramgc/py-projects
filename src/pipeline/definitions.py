from dagster import Definitions

from src.pipeline.job.sample_job import hello_job

defs = Definitions(
    jobs=[hello_job]
)
