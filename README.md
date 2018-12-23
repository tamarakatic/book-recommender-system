# Book Recommender System

Recommend books to students based on selected course.

## Requirements

* `python 3`, `pip`
* [Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/)

## Installation

Clone repo:

```bash
git clone https://github.com/tamarakatic/book-recommender-system.git
cd book-recommender-system/
```

Make virtualenv and install requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Follow [instructions](https://jena.apache.org/documentation/fuseki2/fuseki-quick-start.html) to
start Jena Fuseki server and load data [file](./data/owl/coursebook.owl).

Train recommender system:

```bash
python -m recommender --train
```

Set SPARQL server URL and Run Flask server:

```bash
SPARQL_SERVER_URL=<url_to_jena_fuseki_server> python run.py

e.g.

SPARQL_SERVER_URL=http://localhost:3030/books/ python run.py
```

Go to start [page](http://localhost:5000/). 
