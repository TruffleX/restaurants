import time
from SPARQLWrapper import SPARQLWrapper, JSON, CSV
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DBPediaClient:
    prefixes = {
        "dbr": "<http://dbpedia.org/resource/>",
        'dbo': '<http://dbpedia.org/ontology/>',
        'dbp': '<http://dbpedia.org/property/>',
        'dct': '<http://purl.org/dc/terms/>',
        'dbc': '<http://dbpedia.org/resource/Category:>',
        'rdf': '<http://www.w3.org/1999/02/22-rdf-syntax-ns#>',
        'owl': '<http://www.w3.org/2002/07/owl#>',
        'wikidata': '<http://www.wikidata.org/entity/>',
    }

    def __init__(self):
        self.client = SPARQLWrapper("http://dbpedia.org/sparql")

    @staticmethod
    def with_prefixes(query):
        header = "\n".join([f"PREFIX {key}: {value}" for key, value in DBPediaClient.prefixes.items()])

        return f"""
        {header}

        {query}

        """

    @staticmethod
    def paginate(query, i, paginator_size=10000):
        return f"""
        {query}
        LIMIT {paginator_size} OFFSET {i * paginator_size}
        """

    @staticmethod
    def rows_from_result(result):
        return result['results']['bindings']

    def get(self, query, format=JSON, paginator_size=10000, max_rows=1000000):
        page = 0
        query = self.with_prefixes(query)
        paginated_query = self.paginate(query, page, paginator_size)

        self.client.setQuery(paginated_query)
        self.client.setReturnFormat(format)

        result = self.client.query().convert()
        results = self.rows_from_result(result)

        while len(self.rows_from_result(result)) > 0 and (page + 1) * paginator_size < max_rows:
            logging.info(f"Paginating query, currently have {len(results)} rows")
            page += 1

            paginated_query = self.paginate(query, page, paginator_size)
            self.client.setQuery(paginated_query)
            result = self.client.query().convert()

            results.extend(self.rows_from_result(result))
            time.sleep(.1)

        return results