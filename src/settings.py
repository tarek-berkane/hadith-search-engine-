from whoosh.fields import *

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from src.engine.analyzer import analyzer
import os

base_dir = os.path.realpath(os.path.curdir)
raw_file = "./raw/raw data"
build_file = "./raw/data"
indexing_dir = 'hadith_dir'

# fields id in csv
CHAPTER_NUMBER = 0
CHAPTER_ENGLISH = 1
CHAPTER_ARABIC = 2
SECTION_NUMBER = 3
SECTION_ENGLISH = 4
SECTION_ARABIC = 5
HADITH_NUMBER = 6
ENGLISH_HADITH = 7
ENGLISH_ISNAD = 8
ENGLISH_MATN = 9
ARABIC_HADITH = 10
ARABIC_ISNAD = 11
ARABIC_MATN = 12
ARABIC_COMMENT = 13
ENGLISH_GRADE = 14
ARABIC_GRADE = 15

hadith_schema = Schema(
    # hadith=TEXT(analyzer=analyzer),
    hadith_id=NUMERIC(stored=True),
    hadith_matn=TEXT(analyzer=analyzer),
    hadith_isnad=TEXT(analyzer=analyzer),
    hadith_grade=TEXT(analyzer=analyzer),
    hadith_author=TEXT()
)

# ----------------------
# DATABASE
# ----------------------


# For testing
# ------------------------------------------------------------------
MEMORY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
memory_engine = create_async_engine(MEMORY_DATABASE_URL, future=True, echo=True)
async_session_memory = sessionmaker(memory_engine, expire_on_commit=False, class_=AsyncSession)
# ------------------------------------------------------------------

# For production
# ------------------------------------------------------------------
DATABASE_URL = "sqlite+aiosqlite:///./hadith.db"
engine = create_async_engine(DATABASE_URL, future=True, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

ALLOWED_COURSES = ["course", 'tp', 'td']
ALLOWED_Days = ["sunday", 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

DONE_CODE = 0
ERROR_CODE = 1
BAD_ARGUMENTS = 2
