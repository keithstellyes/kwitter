-- if there are tweets with duplicate ID's, this will return row(s)
-- if no duplicates, this will return no rows.
-- https://stackoverflow.com/questions/2594829/finding-duplicate-values-in-a-sql-table
-- this in of itself is not valid SQL,
select * from {table_name} group by {id_column} having(count({id_column}) > 1);