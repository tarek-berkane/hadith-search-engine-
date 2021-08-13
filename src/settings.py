from whoosh.fields import *

from src.analyzer import analyzer
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
    hadith=TEXT(analyzer=analyzer),
    hadith_id=NUMERIC,
    hadith_matn=TEXT(stored=True, analyzer=analyzer),
    hadith_isnad=TEXT(stored=True, analyzer=analyzer),
    hadith_grade=TEXT(stored=True, analyzer=analyzer),
    hadith_author=TEXT(stored=True)
)
