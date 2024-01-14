import ssl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from instarest.core.config import get_core_settings

if get_core_settings().db_cert_path is None:
    connect_args = {}
else:
    ssl_context = ssl.create_default_context(cafile=get_core_settings().db_cert_path)
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    connect_args = {"ssl": ssl_context}

engine = create_engine(
    get_core_settings().sqlalchemy_database_uri,
    connect_args=connect_args,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
