"""
This module provides functionality for upserting data from a Pandas DataFrame into a SQL table defined by SQLAlchemy. It facilitates efficient synchronization of large datasets from DataFrame to SQL tables, especially useful in scenarios where data integrity and efficiency are crucial.

Components:
1. `Upsert` class:
   - Manages the dfupsert process for a given DataFrame into a specified SQLAlchemy table object.
   - Automatically handles the creation of temporary tables and the merging of data from the DataFrame into the target table.
   - Supports multiple database engines, adaptable to various database systems.

2. `dfupsert` function:
   - A utility function that simplifies the use of the `Upsert` class.
   - Instantiates and executes the dfupsert process using the provided DataFrame and SQLAlchemy table object.

Features:
- Chunked data handling for managing large datasets.
- Compatibility with different SQLAlchemy supported databases like MySQL, PostgreSQL, etc.
- Error handling to address issues during data synchronization.

Prerequisites:
- Pandas: for DataFrame operations.
- SQLAlchemy: for database interactions.

Example Usage:
    from pandas import DataFrame
    from sqlalchemy import create_engine, MetaData, Table
    from your_module_name import dfupsert

    # Database engine setup
    engine = create_engine('your-database-connection-string')
    metadata = MetaData(bind=engine)
    table = Table('your_table_name', metadata, autoload=True)

    # Sample DataFrame
    df = DataFrame({'column1': [1, 2, 3], 'column2': ['A', 'B', 'C']})

    # Perform dfupsert
    dfupsert(df, engine, table)

Note: Ensure 'your_module_name' and other placeholders are replaced with the actual values.

Designed for applications where regular data updates to SQL tables are required, this module offers an optimized solution to handle such operations seamlessly.
"""

__all__ = ["Upsert", "upsert"]

from pandas import DataFrame
from sqlalchemy import Connection, Engine, text, Table
from sqlalchemy.orm import DeclarativeBase
from typing import Union
from .util import get_template, Driver
from .factory import UpsertFactory


class Upsert:
    """A class for upserting a DataFrame to a table."""

    def __init__(
            self,
            df: DataFrame,
            con: Union[Connection, Engine],
            table: Union[Table, DeclarativeBase, str],
            chunksize: int = 2000
    ) -> None:
        self.df = df
        self.con = con
        self.table = table
        self.chunksize = chunksize
        self.driver = Driver(con)
        self._get_templates(table, df)

    def __call__(self, *args, **kwargs):
        """Run the dfupsert process."""
        if isinstance(self.con, Engine):
            with self.con.connect() as conn:
                self.run(conn)
                conn.commit()
        elif isinstance(self.con, Connection):
            self.run(self.con)

    def _get_templates(self, table, df):
        """Get the templates for the target and temp tables."""
        model = self.driver.get_table(table)
        self.target = get_template(table=model, driver=self.driver, is_temp=False)
        self.temp = get_template(table=model, driver=self.driver, is_temp=True)
        self.target_table = f"{self.target.schema}.{self.target.name}"
        schema_prefix = f"{self.temp.schema}." if self.temp.schema else ""
        self.temp_table = f"{schema_prefix}{self.temp.name}"
        self.subset = list(set(df.columns).intersection([col.name for col in self.target.columns]))

    def _create_tables(self, conn: Connection):
        """Create the target and temp tables."""
        self.target.create(conn, checkfirst=True)
        self.temp.create(conn)

    def _insert_to_temp_table(self, conn: Connection):
        """Insert the DataFrame to the temp table."""
        schema = None if self.driver.name in ("mysql", "postgresql") else self.temp.schema
        data_types = {col.name: col.type for col in self.temp.columns}
        self.df[self.subset].to_sql(
            self.temp.name,
            conn,
            schema=schema,
            if_exists="append",
            index=False,
            chunksize=self.chunksize,
            dtype=data_types
        )
        return

    def _update_to_target_table(self, conn: Connection):
        """Update the target table from the temp table."""
        upsert_ = UpsertFactory(self.driver).upsert
        stmt = upsert_(self.target, self.temp, self.subset).stmt
        conn.execute(text(stmt))

    def run(self, conn: Connection):
        """Run the dfupsert process."""
        self._create_tables(conn)
        self._insert_to_temp_table(conn)
        self._update_to_target_table(conn)


def upsert(
        df: DataFrame,
        con: Union[Connection, Engine],
        table: Union[Table, DeclarativeBase, str],
        chunksize: int = 1000
) -> None:
    """Upsert a DataFrame to a table.

    Args:
        df (DataFrame): The DataFrame to dfupsert.
        con (Union[Connection, Engine]): The database connection or engine.
        table (Union[Table, DeclarativeBase]): The target table.
        chunksize (int, optional): Number of rows per chunk for insertion. Defaults to 1000.
    """
    upsert_proc = Upsert(df=df, con=con, table=table, chunksize=chunksize)
    upsert_proc()
