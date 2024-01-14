from sqlalchemy import MetaData, Column, UUID
from sqlalchemy.orm import as_declarative, declared_attr
from uuid import uuid4
from ..core.config import get_core_settings

# see here for setting the default schema: https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html
metadata_obj = MetaData(schema=get_core_settings().db_schema_name)


@as_declarative(metadata=metadata_obj)
class DeclarativeBase:
    # all models have UUIDv4 IDs
    id = Column(UUID, primary_key=True, unique=True, default=uuid4)
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        # pylint: disable=no-self-argument
        return cls.__name__.lower()
