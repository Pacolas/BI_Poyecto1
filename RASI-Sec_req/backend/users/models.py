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
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
patients = Table(
    "patients",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True, index=True),
    Column("name", String(), index=True),
    # password = Column(String)
    Column("birth", Date(), index=True),
    Column("gender", String()),
    Column("pnumber", BigInteger()),
    Column("email", String()),
    Column("resume", String()),
    Column("hash", String(), nullable=True),
)



doctors = Table(
    "doctors",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True, index=True),
    Column("name", String(), index=True),
    # password = Column(String)
    Column("birth", String(), index=True),
    Column("gender", String()),
    Column("pnumber", BigInteger()),
    Column("email", String()),
)

eps = Table(
    "eps",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True, index=True),
    Column("name", String(), index=True),
    # password = Column(String)
    Column("pnumber", BigInteger()),
    Column("email", String()),
    Column("address", String()),
)

ips = Table(
    "ips",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True, index=True),
    Column("name", String(), index=True),
    # password = Column(String)
    Column("pnumber", BigInteger()),
    Column("email", String()),
    Column("address", String()),
)

admin = Table(
    "admin",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True, index=True),
    Column("name", String(), index=True),
    # password = Column(String)
    Column("pnumber", BigInteger()),
    Column("email", String()),
    Column("address", String()),
    Column("permissions", Integer()),
)
