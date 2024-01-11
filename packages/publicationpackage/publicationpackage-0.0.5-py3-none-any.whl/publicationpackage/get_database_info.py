def get_database_info(database_name, show_tables=True, show_columns=True, specific_table=None, specific_column=None):
    client = boto3.client('glue', region_name='eu-west-1')

    # Get database information
    response_get_databases = client.get_databases()
    database_list = response_get_databases['DatabaseList']

    for database_dict in database_list:
        current_database_name = database_dict['Name']
        if database_name not in current_database_name:
            continue

        print('\nDatabase Name: ' + current_database_name)

        if show_tables:
            # Get tables information
            response_get_tables = client.get_tables(DatabaseName=current_database_name)
            table_list = response_get_tables['TableList']

            for table_dict in table_list:
                table_name = table_dict['Name']

                # Check if a specific table is specified
                if specific_table and specific_table != table_name:
                    continue

                print('\n-- Table Name: ' + table_name)

                if show_columns:
                    # Get columns information
                    response_get_columns = client.get_table(DatabaseName=current_database_name, Name=table_name)
                    column_list = response_get_columns['Table']['StorageDescriptor']['Columns']

                    print('   Columns:')
                    for column in column_list:
                        column_name = column['Name']

                        # Check if a specific column is specified
                        if specific_column and specific_column != column_name:
                            continue

                        column_type = column['Type']
                        print(f'   - Name: {column_name}, Type: {column_type}')

