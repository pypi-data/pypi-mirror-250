
__all__ = ["UpsertFactory"]

from sqlalchemy import Table, UniqueConstraint, PrimaryKeyConstraint
from dfupsert.util import Driver

MSSQL_SOURCE = "source"
MSSQL_TARGET = "target"


class SQLTemplate:
    mysql = """
INSERT INTO {target_table} ({target_columns})
SELECT {source_columns}   
FROM {temp_table}
ON DUPLICATE KEY UPDATE 
    {update_clause};
    """

    postgresql = """
INSERT INTO {target_table} ({target_columns})
SELECT {source_columns}
FROM {temp_table}
ON CONFLICT ({confilict_conditions}) DO UPDATE SET 
    {update_clause};
    """

    mssql = """
MERGE INTO {target_table} AS %s
USING {temp_table} AS %s
ON {conflict_conditions}
WHEN MATCHED THEN
    UPDATE SET {update_clause}
WHEN NOT MATCHED THEN
    INSERT ({target_columns})
    VALUES ({insert_clause});
    """ % (MSSQL_TARGET, MSSQL_SOURCE)


class BasePattern:
    """Base class for the clauses."""

    def __init__(
            self,
            table: Table,
            temp_table: Table = None,
            subset: list = None
    ) -> None:
        self.table = table
        self.temp_table = temp_table
        if subset is None:
            subset = [col.name for col in self.table.columns]
        self.subset = subset
        self.target_table = self.table.schema + "." + self.table.name

    def _get_unique_constraints(self, mode="first") -> list:
        """Get the unique constraint of the table."""
        unique_constraints = []
        for constraint in self.table.constraints:
            if isinstance(constraint, PrimaryKeyConstraint) or isinstance(constraint, UniqueConstraint):
                temp = [col.name for col in constraint.columns]
                unique_constraints.append(temp)

        for index in self.table.indexes:
            if index.unique:
                temp = [col.name for col in index.columns]
                unique_constraints.append(temp)
        if mode == "first":
            for unique_constraint in unique_constraints:
                if self.subset is not None:
                    if set(unique_constraint).issubset(set(self.subset)):
                        return unique_constraint
                else:
                    raise KeyError("subset must contain the unique constraint.")
        elif mode == "all":
            return [unique_constraint for unique_constraint in unique_constraints if
                    set(unique_constraint).issubset(set(self.subset))]
        else:
            raise ValueError("mode must be first or all.")

    def get_insert_columns_stmt(self, source=False) -> str:
        """Get the insert columns statement."""
        if source:
            prefix = MSSQL_SOURCE + "."
        else:
            prefix = ""
        return ", ".join(
            [
                f"{prefix}{col}"
                for col in self.subset
            ]
        )


class MSSQLUpsert(BasePattern):
    PATTERN = SQLTemplate.mssql

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.temp_table = self.temp_table.schema + "." + self.temp_table.name
        self.constraints = self._get_unique_constraints(mode="all")

    def get_conflict_stmt(self) -> str:
        unique_constraints = self._get_unique_constraints(mode="all")
        conflict_stmt_units = [
            " AND ".join(
                [
                    f"{MSSQL_TARGET}.{col} = {MSSQL_SOURCE}.{col}"
                    for col in unique_constraint
                ]
            ) for unique_constraint in unique_constraints
        ]
        return " OR ".join("( %s )" % unit for unit in conflict_stmt_units)

    def get_update_columns_stmt(self) -> str:
        constraint_columns = [col for constraint in self.constraints for col in constraint]
        return ", ".join(
            [
                f"{MSSQL_TARGET}.{col} = {MSSQL_SOURCE}.{col}"
                for col in self.subset
                if col not in constraint_columns
            ]
        )

    @property
    def stmt(self) -> str:
        return self.PATTERN.format(
            target_table=self.target_table,
            temp_table=self.temp_table,
            conflict_conditions=self.get_conflict_stmt(),
            target_columns=self.get_insert_columns_stmt(source=False),
            insert_clause=self.get_insert_columns_stmt(source=True),
            update_clause=self.get_update_columns_stmt()
        )


class MySQLUpsert(BasePattern):
    PATTERN = SQLTemplate.mysql

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.temp_table = self.temp_table.name
        self.constraints = self._get_unique_constraints(mode="first")

    def get_update_columns_stmt(self) -> str:
        return ',\n\t'.join(
            [
                f"{col} = VALUES({col})"
                for col in self.subset
            ]
        )

    @property
    def stmt(self) -> str:
        return self.PATTERN.format(
            target_table=self.target_table,
            temp_table=self.temp_table,
            target_columns=self.get_insert_columns_stmt(),
            source_columns=self.get_insert_columns_stmt(),
            update_clause=self.get_update_columns_stmt()
        )


class PostgreSQLUpsert(BasePattern):
    PATTERN = SQLTemplate.postgresql

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.temp_table = self.temp_table.name
        self.constraints = self._get_unique_constraints(mode="first")

    def get_update_columns_stmt(self) -> str:
        return ',\n\t'.join(
            [
                f"{col} = EXCLUDED.{col}"
                for col in self.subset
            ]
        )

    def get_conflict_stmt(self) -> str:
        return ", ".join(self.constraints)

    @property
    def stmt(self) -> str:
        return self.PATTERN.format(
            target_table=self.target_table,
            temp_table=self.temp_table,
            confilict_conditions=self.get_conflict_stmt(),
            target_columns=self.get_insert_columns_stmt(),
            source_columns=self.get_insert_columns_stmt(),
            update_clause=self.get_update_columns_stmt()
        )


class UpsertFactory:
    MAP = {
        "mssql": MSSQLUpsert,
        "postgresql": PostgreSQLUpsert,
        "mysql": MySQLUpsert
    }

    def __init__(self, driver) -> None:
        self.driver = driver
        self.upsert = self._make_upsert(self.driver)

    @staticmethod
    def _make_upsert(driver: Driver) -> [MSSQLUpsert, MySQLUpsert, PostgreSQLUpsert]:
        result = UpsertFactory.MAP.get(driver.name)
        if result:
            return result
        else:
            raise NotImplementedError("Driver %s is not implemented!")
