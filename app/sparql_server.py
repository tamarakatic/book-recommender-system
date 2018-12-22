from SPARQLWrapper import SPARQLWrapper, JSON

SPARQL_SERVER_URL = 'http://192.168.0.20:3030/books/'
ONTOLOGY_URI = '<http://www.semanticweb.org/tamara/ontologies/2018/11/untitled-ontology-3#>'

sparql = SPARQLWrapper(SPARQL_SERVER_URL)


def get_course_books(course_name):
    query =  """
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
    """.format(ontology=ONTOLOGY_URI, course_name=course_name)

    response = _execute_query(query)
    books = [
        {'book_name': item['bookName']['value'],
        'author': item['author']['value']}
        for item in response
    ]
    return books


def _execute_query(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()
    return response['results']['bindings']
