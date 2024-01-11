def run_sql(sql_statement: str, object_name: str) -> DataFrame:
    """Run a SQL query on the temp views, resulting in a new DataFrame.
      
    :param object_name: The name to temp view to create or replace .
    """
     
    # Run sql statement
    result = spark.sql(sql_statement)
  
    # Create a view. This allows you to use the output in upcoming queries.
    result.createOrReplaceTempView(f"`{object_name}`")
    print(f"Created or replaced the temp view `{object_name}`")    
    return result

