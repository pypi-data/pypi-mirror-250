from pyspark.sql import DataFrame
def write_dataframe_to_s3(bucket_name: str, output_folder: str, df: DataFrame) -> None:
    """Write a PySpark DataFrame to S3 in CSV."""
    write_options = {"header": True}
    df.write.format("csv").options(**write_options).save(f"s3://{bucket_name}/{output_folder}")