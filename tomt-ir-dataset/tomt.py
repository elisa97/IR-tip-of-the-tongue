"""This python file registers a new ir_datasets class 'pangrams'.
   You can find the ir_datasets documentation here: https://github.com/allenai/ir_datasets/.
   This file is intended to work inside the Docker image produced during this tutorial (the Dockerfile copies it and the other files loaded below to the correct locations).
"""
import ir_datasets
from ir_datasets.formats import JsonlDocs, TrecQrels, BaseQueries
from typing import NamedTuple, Dict, List, Any, Optional
from ir_datasets.datasets.base import Dataset
from xml.etree.ElementTree import parse, Element, ElementTree

class TomtDocument(NamedTuple):
    doc_id: str
    text: str
    
    def default_text(self):
        return self.text

class TomtQuery(NamedTuple):
    query_id: str
    title: str
    description: str
    narrative: str
    positiveQueries: List[str]

    def default_text(self):
        return self.title

class TomtQueries(BaseQueries):
    _source: Any

    def __init__(
            self,
            source: Any,
            namespace: Optional[str] = None,
            language: Optional[str] = None,
    ):
        self._source = source
        self._namespace = namespace
        self._language = language

    def queries_path(self):
        return self._source.path()

    def queries_iter(self):
        with self._source.stream() as file:
            tree: ElementTree = parse(file)
            root: Element = tree.getroot()
            assert root.tag == "topics"

            for element in root:
                element: Element
                assert element.tag == "topic"
                number = int(element.attrib["number"].strip())
                title = element.findtext("title").strip()
                description = element.findtext("description") \
                    .strip().replace("\n", " ")
                narrative = element.findtext("narrative") \
                    .strip().replace("\n", " ")
                positiveQueries = element.findtext("positiveQueries").split(',')
                positiveQueries = [i.strip() for i in positiveQueries]
                yield TomtQuery(
                    str(number),
                    title,
                    description,
                    narrative,
                    positiveQueries
                )

    def queries_cls(self):
        return TomtQuery

    def queries_lang(self):
        return "en"

ir_datasets.registry.register('tomt', Dataset(
    JsonlDocs(ir_datasets.util.PackageDataFile(path='datasets_in_progress/documents.jsonl'), doc_cls=TomtDocument, lang='en'),
    TomtQueries(ir_datasets.util.PackageDataFile(path='datasets_in_progress/topics.xml')),
    TrecQrels(ir_datasets.util.PackageDataFile(path='datasets_in_progress/qrels.txt'), {0: 'Not Relevant', 1: 'Relevant', 2: 'Highly Relevant'})
))
