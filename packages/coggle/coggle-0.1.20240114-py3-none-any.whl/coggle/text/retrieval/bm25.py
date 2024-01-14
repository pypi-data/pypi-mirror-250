import math
from collections import defaultdict
from typing import List, Tuple, Any, Union


class BM25Okapi:
    def __init__(self,
        doc_ids : Union[List[str], None] = None,
        documents : Union[List[List[str]], None] = None,
        k1 : float =1.5, b : float =0.75, epsilon : float =0.25
    ) -> None:
        self.total_size : int = 0
        self.invert_index : dict = defaultdict(List[int])
        self.idf : dict = defaultdict(float)
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        self.doc_lengths : dict = {}
        self.average_doc_length = 0
        self.total_doc_length = 0

        self._up2date = False
        self._max_doc_id = 0
        self._doc_id_set : dict = defaultdict(List[str])

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

        doc_length = len(document)
        self.total_doc_length -= self.doc_lengths[doc_id]
        self.total_doc_length += doc_length
        self.doc_lengths[doc_id] = doc_length
        self._doc_id_set[doc_id] = document
        return True

    def add_document(self, doc_id: Any, document: List[str]) -> bool:
        frequencies : dict = defaultdict(int)
        doc_length = len(document)

        self.doc_lengths[doc_id] = doc_length
        self.total_doc_length += doc_length

        for word in document:
            frequencies[word] += 1

        for word, freq in frequencies.items():
            if word not in self.invert_index:
                self.invert_index[word] = []
            self.invert_index[word].append((doc_id, freq))

        self._up2date = False
        self.total_size +=1
        self._doc_id_set[doc_id] = document
        return True

    def delete_document(self, doc_id: int) -> bool:
        if doc_id not in self._doc_id_set:
            return False

        for term, freq in self.invert_index.items():
            self.invert_index[term] = [(d_id, f) for d_id, f in freq if d_id != doc_id]

        self.total_doc_length -= self.doc_lengths[doc_id]
        del self.doc_lengths[doc_id]
        del self._doc_id_set[doc_id]
        self.total_size -= 1
        return True

    def delete_term(self, term: str) -> bool:
        if term not in self.invert_index:
            return False

        doc_ids_term_count = sum([freq for _, freq in self.invert_index[term]])
        self.total_doc_length -= doc_ids_term_count
        del self.invert_index[term]
        return True

    def _update_idf(self):
        for word, postings in self.invert_index.items():
            df = len(postings)
            idf = math.log((self.total_size - df + 0.5) / (df + 0.5) + 1.0)
            self.idf[word] = idf

    def query(self, query: List[str], top_n=None) -> List[Tuple[int, float]]:
        if not self._up2date:
            self._update_idf()
            self._up2date = True
        
        scores : dict = defaultdict(float)
        for q in query:
            if q in self.invert_index:
                idf = self.idf[q]
                for doc_id, freq in self.invert_index[q]:
                    doc_len = self.doc_lengths[doc_id]
                    scores[doc_id] += idf * (freq * (self.k1 + 1) /
                                             (freq + self.k1 * (1 - self.b + self.b * doc_len / self.total_doc_length * self.total_size)))

        doc_ids_with_scores = [(i, score) for i, score in scores.items()]
        doc_ids_with_scores.sort(key=lambda x: x[1], reverse=True)

        if top_n is not None:
            doc_ids_with_scores = doc_ids_with_scores[:top_n]

        return doc_ids_with_scores


class BM25L:
    pass


class BM25Plus:
    pass


class BM25Adpt:
    pass


class BM25T:
    pass
