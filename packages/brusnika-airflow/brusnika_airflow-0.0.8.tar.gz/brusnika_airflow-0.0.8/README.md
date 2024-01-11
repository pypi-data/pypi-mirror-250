# Brusnika Airflow Package

This Python package contains a set of frequently used functions for using in DAGs.

## Table of Contents

1. [Quick Start]
2. [Functions]
   - grants_for_table
   - generate_table_name_for_temp_store
   - create_empty_table_like_this
   - copy_data_between_tables
   - copy_data_between_tables_without_trancate
   - table_exists

## Quick Start

Install the package:

```bash
pip install brusnika-airflow
```



Example of usage:
```
import brusnika_airflow

tablename = brusnika_airflow.generate_table_name_for_temp_store('temp_tablename')
```

## Functions

- `grants_for_table(pg_hook, schema, table)`: Grants privileges to a user on a specific table.

- `generate_table_name_for_temp_store(table_prefix)`: Generates a temporary table name for storing data temporarily.

- `create_empty_table_like_this(pg_hook, source_schema, source_table, destination_schema, destination_table)`: Creates an empty table with the same structure as the source table.

- `copy_data_between_tables(pg_hook, source_schema, source_table, destination_schema, destination_table)`: Truncate data in the destination table. Copies data from the source table to the destination table and then deletes the source table.

- `copy_data_between_tables_without_trancate(pg_hook, source_schema, source_table, destination_schema, destination_table)`: Copies data from the source table to the destination table and then deletes the source table.

- `copy_data_between_tables_with_deleting_data(pg_hook, source_schema, source_table, destination_schema, destination_table, delete_clause)`: Delete data in the destination table with use delete_clause condition. Copies data from the source table to the destination table and then deletes the source table.

- `table_exists(pg_hook, schema, table)`: Checks if a table exists in a given schema.

- `dtypes_for_sql(dataframe, json_columns)`: Create dtype for dataframe with json.
