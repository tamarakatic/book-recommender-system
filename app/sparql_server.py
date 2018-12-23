from SPARQLWrapper import SPARQLWrapper, JSON
import langdetect

from recommender import Book
import config


sparql = SPARQLWrapper(config.SPARQL_SERVER_URL)


def get_course_books(course_name):
    query = """
    PREFIX uni: {ontology}
    SELECT ?bookName ?author
    WHERE {{
      ?course a uni:Course .
      ?course uni:name ?courseName .
      FILTER(str(?courseName) = "{course_name}")
      ?course uni:hasBook ?book .
      ?book uni:name ?bookName .
      ?book uni:author ?author .
    }}
    """.format(ontology=config.ONTOLOGY_URI, course_name=course_name)

    response = _execute_query(query)
    books = {
        Book(title=item['bookName']['value'],
             author=item['author']['value'],
             language=langdetect.detect(item['bookName']['value']))
        for item in response
    }
    return books


def _execute_query(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()
    return response['results']['bindings']
