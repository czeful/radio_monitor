import os
from dotenv import load_dotenv
from  sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import logging
import sys

load_dotenv()

DB_URL = os.getenv("DB_URL")


if not DB_URL:
    raise RuntimeError(
        "Database Url is missing, check your env file pls"
    )


ENGINE_OPTIONS = {}

if DB_URL.startswith('postgresql'): 

    ENGINE_OPTIONS = {
        "pool_size" : 20,
        "max_overflow" : 10,
        "pool_pre_ping" : True
    }

elif DB_URL.startswith("sqlite"):

    ENGINE_OPTIONS = {
        "connect_args" : {
            "check_same_tread": False
        }
    }

engine: Engine = create_engine(
    DB_URL,
    **ENGINE_OPTIONS)