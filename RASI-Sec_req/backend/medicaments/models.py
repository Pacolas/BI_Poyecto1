from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Table,
    Integer,
    Float,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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

medicaments = Table(
    "medicaments",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True, index=True),
    Column("name", String(), index=True),
    Column("brand", String(), index=True),
    # password = Column(String)
    Column("quantity", Float()),
    Column("unit", String()),
    Column("ingredients", String()),
    Column("contains", BigInteger()),
)

med_avaliability = Table(
    "medicaments_avaliable",
    Base.metadata,
    Column("id_ips", BigInteger(), primary_key=True, index=True),
    Column("id_medicament", BigInteger(), primary_key=True, index=True),
    # password = Column(String)
    Column("avaliable", Integer()),
    Column("price", Float()),
)

log = Table(
    "log",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True, index=True),
    Column("name", String(), primary_key=True, index=True),
    Column("action", String(), primary_key=True, index=True),
    Column("datetime", String()),
    Column("medicament_id", Float()),

)
