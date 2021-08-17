from sqlalchemy.orm import declarative_base, registry

from sqlalchemy import Column, String, Integer, Date

Base: registry = declarative_base()


class Hadith(Base):
    __tablename__ = 'hadith'

    id = Column(Integer, primary_key=True)
    chapter_number = Column(Integer)
    chapter_arabic = Column(String)

    section_number = Column(String)
    section_arabic = Column(String)

    hadith_number = Column(Integer)

    arabic_hadith = Column(String)
    arabic_isnad = Column(String)
    arabic_matn = Column(String)

    arabic_grade = Column(String)

    author = Column(String)

    def __repr__(self):
        return f"Hadith (id={self.id!r}, name={self.arabic_matn[:100]!r})"
