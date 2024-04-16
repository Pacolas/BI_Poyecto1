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

schedules = Table(
    "schedules",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True, index=True),
    Column("startday", String(), index=True),
    # password = Column(String)
    Column("endday", String(), index=True),
    Column("starttime", Time()),
    Column("endtime", Time(), index=True),
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

appointments = Table(
    "appointments",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True, index=True),
    Column("date", Date(), index=True),
    Column("time", Time()),
    Column("duration", Integer()),
    Column("address", String()),
    Column("patient_id", BigInteger(), ForeignKey("patients.id"),nullable=True),
    Column("doctor_id", BigInteger(), ForeignKey("doctors.id")),
    Column("service_id", BigInteger(), ForeignKey("services.id")),
)
services = Table(
    "services",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True),
    Column("speciality", String(), index=True, unique=True),
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
