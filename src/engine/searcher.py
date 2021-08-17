from whoosh.index import open_dir
from whoosh.qparser import QueryParser, OrGroup
from whoosh.query import Phrase

from whoosh.searching import highlight

from src.settings import hadith_schema

reader = open_dir('hadith_dir', schema=hadith_schema)


def search(query, type):
    query = query

    with reader.searcher() as searcher:
        if type == 'or':
            query = QueryParser("hadith_matn", reader.schema, group=OrGroup).parse(query)
        else:
            query = QueryParser("hadith_matn", reader.schema).parse(query)

        results = searcher.search(query, terms=True)

        result_list = [item['hadith_id'] for item in results]

        # TODO: return list [remove reuslt key]
        return {
            "result": result_list
        }
