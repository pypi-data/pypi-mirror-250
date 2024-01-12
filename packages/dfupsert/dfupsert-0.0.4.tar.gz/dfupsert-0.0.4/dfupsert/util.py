"""
Utility functions for the dfupsert package, handling SQLAlchemy engine interactions
and dynamic SQLAlchemy table template creation.

Classes:
- Driver: Manages SQLAlchemy engine/connection objects and retrieves database dialects.
- Base: Abstract base class for table template construction.

Functions:
- get_template: Generates a table template for dfupsert operations, reflecting the
  structure of a provided SQLAlchemy table. Supports creation of temporary table templates.
- _transform_to_temp_table: Internal function to modify a template for temporary table usage.

Usage:
- Use Driver to handle different SQLAlchemy engines/connections and extract Table objects.
- Use get_template to dynamically create SQLAlchemy Table classes, replicating existing
  table structures for operations like dfupsert.

Note:
- Assumes familiarity with SQLAlchemy's core components.
- Database-agnostic, supporting various SQL dialects.
"""

__all__ = ["Driver", "get_template"]

from copy import deepcopy
from typing import Any

from sqlalchemy import (
    Table,
    PrimaryKeyConstraint,
    Column,
    Engine,
    Connection,
    MetaData, ForeignKeyConstraint
)
from sqlalchemy.orm import DeclarativeBase

UPSERT = "dfupsert"
ZIPPER = "zipper"


class Driver:
    """A class for getting the driver of a SQLAlchemy engine."""

    def __init__(self, engine_or_conn):
        self.engine_or_conn = engine_or_conn
        self.engine = self.get_engine()
        self.name = self.engine.dialect.name

    def __repr__(self):
        return f"<DatabaseDriver: {self.name}>"

    def __str__(self):
        return self.name

    def get_engine(self):
        """Get the engine from the engine_or_conn attribute."""
        if isinstance(self.engine_or_conn, Engine):
            return self.engine_or_conn
        elif isinstance(self.engine_or_conn, Connection):
            return self.engine_or_conn.engine
        else:
            raise TypeError("engine_or_conn must be Engine or Connection")

    def get_table(self, template) -> Table:
        if isinstance(template, str):
            meta_data = MetaData()
            meta_data.reflect(bind=self.engine)
            template = meta_data.tables[template.split(".")[1]]
            del meta_data
        if not isinstance(template, Table):
            template = template.__table__

        return template


def get_template(
        driver: Driver,
        table,
        is_temp=False
) -> Any:
    """Get the appropriate template

    Parameters
    ----------
    driver : Driver
        The driver for the SQLAlchemy engine.
    table : Table
        The SQLAlchemy table.
    is_temp : bool, optional
        Whether the template is for a temporary table, by default False.

    Returns
    -------
    class
        The appropriate template.
    """
    table = driver.get_table(table)

    class Base(DeclarativeBase):
        """A base class for the templates."""
        __abstract__ = True

    class Template(Base):
        __table__ = deepcopy(table)

    if is_temp:
        Template = _transform_to_temp_table(Template, driver, table.name)
    return driver.get_table(Template)


def _transform_to_temp_table(template, driver: Driver, table_name: str) -> DeclarativeBase:
    """Transform the template to a temporary table."""
    if driver.name in ("mysql", "postgresql"):
        template.__table__.schema = None
        template.__table__.name = "temp_" + table_name
        template.__table__._prefixes = ["TEMPORARY"]
    elif driver.name == "mssql":
        template.__table__.name = "#" + table_name
    else:
        raise ValueError(f"Unsupported database driver: {driver.name}")

    # temporary table should not have foreign key constraint
    template.__table__.constraints = [
        c for c in template.__table__.constraints
        if not isinstance(c, ForeignKeyConstraint)
    ]
    return template

