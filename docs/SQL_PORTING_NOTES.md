# SQL porting notes

The implementation uses SQLite so the project runs without a server. The date conversion uses `substr` because the legacy date is stored as `DD/MM/YYYY`. In SQL Server, use `TRY_CONVERT(date, legacy_date, 103)`; in PostgreSQL, use `to_date(legacy_date, 'DD/MM/YYYY')`.

The duplicate-safe queries use `ROW_NUMBER()`, available in current SQLite, SQL Server, and PostgreSQL. Replace `rowid` ordering with a load timestamp or source-file sequence in a production system.
