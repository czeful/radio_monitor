import os 

from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import( 
    create_async_engine,
    AsyncEngine
)

load_dotenv()

TEST_DB_URL = os.getenv("TEST_DB_URL")

if not TEST_DB_URL:
    raise RuntimeError(
        "TEST_DB_URL is missing"
    )

test_engine: AsyncEngine = create_async_engine(TEST_DB_URL, echo=False)