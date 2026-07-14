import os
from dotenv import load_dotenv
from  sqlalchemy import create_engine
import logging
import sys

load_dotenv()
logging.basicConfig(level=logging.INFO)


pool_size = 20 
max_overflow = 10

db_url = os.getenv("DB_URL")

if db_url is None:
    logging.warning("Your env file is not correct")
    sys.exit(1)

engine = create_engine(f"{db_url}" , pool_size=pool_size, max_overflow=max_overflow)

