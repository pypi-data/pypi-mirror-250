from awsglue.context import GlueContext
from awsglue import DynamicFrame
from pyspark.context import SparkContext
def load_table_from_catalog(database_name: str, table_name: str, partitions: dict, sc: SparkContext) -> DynamicFrame:
    """Load a table using the Glue catalog."""
      
    predicate = f"year = {partitions['year']} AND month = {partitions['month']} AND day = {partitions['day']}" if partitions else ""
    dyf = GlueContext(sc).create_dynamic_frame_from_catalog(
        database=database_name,
        table_name=table_name,
        push_down_predicate=predicate,
        additional_options={
            "isFailFast": True,
            "useS3ListImplementation": False,
        },
    )
      
    return dyf

