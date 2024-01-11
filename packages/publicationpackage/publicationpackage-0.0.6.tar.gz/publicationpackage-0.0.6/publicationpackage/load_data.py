def load_data(database_name: str, table_name: str, partitions: dict = {}) -> DataFrame:
    """Load data from the Glue Catalog and convert it to a Spark dataframe.
    If the table does not have a partition, use the default empty dictionary"""
    dyf = load_table_from_catalog(database_name, table_name, partitions) 
    df = dyf.toDF()
    df.createOrReplaceTempView(f"`{database_name}.{table_name}`")
    print(f"Created or replaced the temp view `{database_name}.{table_name}`")
    return df

