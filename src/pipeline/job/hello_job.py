from dagster import op, job


@op
def hello_op():
    print("***********************Hello, Dagster!*******************")
    return "Hello, Dagster!"


@job
def hello_job():
    hello_op()


if __name__ == "__main__":
    # Execute the job in-process.
    result = hello_job.execute_in_process()
    print(result)
