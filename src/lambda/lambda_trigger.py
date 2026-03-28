import boto3

def lambda_handler(event, context):

    glue = boto3.client("glue")

    # Get uploaded file key
    key = event["Records"][0]["s3"]["object"]["key"]

    glue.start_job_run(
        JobName="travel_etl_job",
        Arguments={
            "--INPUT_KEY": key
        }
    )