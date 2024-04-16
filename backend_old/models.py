from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Time,
    Table,
    Date,
    ForeignKey,
    Integer,
    Float,
)
from sqlalchemy import Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
training_id_seq = Sequence('training_id_seq')
version_id_seq = Sequence('version_id_seq')

# Crear la tabla 'trainings' con el ID usando la secuencia
trainings = Table(
    "trainings",
    Base.metadata,
    Column("id", BigInteger(), training_id_seq, primary_key=True, index=True),
    Column("description", String()),
    Column("calification", Integer(), index=True),
    Column("version", String(), index=True)
)
versions = Table(
    "versions",
    Base.metadata,
    Column("id", BigInteger(), version_id_seq, primary_key=True, index=True),
    Column("name", String(),  index=True)
)


predictions = Table(
    "predictions",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True, index=True),
    Column("creator", String(), index=True),
    Column("description", String(), index=True),
    Column("calification", Integer()),
    Column("version", String(), index=True)
)


metrics = Table(
    "metrics",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True, index=True),
    Column("name", String(), index=True),
    # password = Column(String)
    Column("percent", Float(), index=True),
    Column("version", String(), index=True)

)
