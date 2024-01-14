from collections import defaultdict
from typing import List, Tuple, Any, Union

class TFIDF:
    def __init__(
        self,
        doc_ids : Union[List[str], None] = None,
        documents : Union[List[List[str]], None] = None
    ) -> None:
        self.total_size : int = 0
        self.invert_index : dict = defaultdict(List[int])
        self.idf : dict = defaultdict(float)

        self._doc_id_set : dict = defaultdict(List[str])
        self._up2date : bool = False

        if doc_ids is not None:
            if len(doc_ids) != len(documents):
                raise Exception("the count of doc_ids do not math documents!")

            for doc_id, document in zip(doc_ids, documents):
                self.add_document(doc_id, document)

    def update_document(self, doc_id: int, document: List[str]) -> bool:
        if doc_id not in self._doc_id_set:
            return False

        for term, freq in self.invert_index.items():
            self.invert_index[term] = [(d_id, f) for d_id, f in freq if d_id != doc_id]

        term_frequency : dict = defaultdict(int)
        for term in document:
            term_frequency[term] += 1

        for term, freq in term_frequency.items():
            self.invert_index[term].append((doc_id, freq))

        self._doc_id_set[doc_id] = document
        return True

    def add_document(self, doc_id: Any, document: List[str]) -> bool:
        term_frequency : dict = defaultdict(int)
        for term in document:
            term_frequency[term] += 1

        for term, freq in term_frequency.items():
            if term not in self.invert_index:
                self.invert_index[term] = []
            self.invert_index[term].append((doc_id, freq))

        self.total_size +=1
        self._doc_id_set[doc_id] = document
        self._up2date = False
        return True

    def delete_document(self, doc_id: int) -> bool:
        if doc_id not in self._doc_id_set:
            return False

        for term, freq in self.invert_index.items():
            self.invert_index[term] = [(d_id, f) for d_id, f in freq if d_id != doc_id]

        del self._doc_id_set[doc_id]
        self.total_size -= 1
        return True

    def delete_term(self, term: str) -> bool:
        if term not in self.invert_index:
            return False
        del self.invert_index[term]
        return True

    def _calculate_idf(self):
        for term, posting_list in self.invert_index.items():
            df = len(posting_list)
            self.idf[term] = 1 + (self.total_size / (1 + df))

    def query(self, query: List[str], top_n=None) -> List[Tuple[int, float]]:
        if not self._up2date:
            self._calculate_idf()
            self._up2date = True

        scores : dict = defaultdict(float)
        for term in query:
            if term in self.invert_index:
                idf = self.idf[term]
                for doc_id, tf in self.invert_index[term]:
                    scores[doc_id] += tf * idf

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        if top_n is not None:
            sorted_scores = sorted_scores[:top_n]
        return sorted_scores