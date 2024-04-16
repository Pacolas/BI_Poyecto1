from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Time,
    Table,
    Date,
    ForeignKey,
    Integer,

)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()




appointments = Table(
    "appointments",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True, index=True),
    Column("date", Date(), index=True),
    Column("time", Time()),
    Column("duration", Integer()),
    Column("address", String()),
    Column("patient_id", BigInteger(),nullable=True),
    Column("doctor_id", BigInteger()),
    Column("service_id", BigInteger(), ForeignKey("services.id")),
)
services = Table(
    "services",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True),
    Column("speciality", String(), index=True, unique=True),
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
