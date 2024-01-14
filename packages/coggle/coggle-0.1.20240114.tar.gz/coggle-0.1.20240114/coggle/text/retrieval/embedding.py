from typing import List, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize


class TextEmbedding:
    def __init__(self, 
        encoder : Any, 
        doc_ids : List[Any]=None, 
        documents : List[List[str]]=None, 
        device : str='cpu'
    ):
        """
        初始化TextEmbedding对象，用于文本编码与检索
        
        参数:
        - encoder: 编码器模型名称 或 模型路径
        - doc_ids: 文档名称
        - documents: 文档内容
        - device: 设备（CPU 或 GPU）
        """
        self.total_size = 0
        self.total_feats: np.ndarray = None
        self.doc_id_list: np.ndarray = np.array([], dtype=object)

        if isinstance(encoder, str):
            self.encoder_model = SentenceTransformer(encoder)

        if doc_ids is not None:
            if len(doc_ids) != len(documents):
                raise Exception("the count of doc_ids do not math documents!")
            
            self.batch_add_documents(doc_ids, documents)

    def update_document(self, doc_id: Any, document: str) -> bool:
        if sum(doc_id == self.doc_id_list) == 0:
            return False

        idx = np.where(doc_id == self.doc_id_list)[0]
        self.total_feats[idx] = self.encoder_model.encode(document)

        return True

    def add_document(self, doc_id: str, document: str) -> bool:
        self.doc_id_list = np.array(list(self.doc_id_list) + [doc_id], dtype=object)
        doc_feat = self.encoder_model.encode(document)
        doc_feat = doc_feat.reshape(1,-1)
        doc_feat = normalize(doc_feat)
        
        if self.total_size is None:
            self.total_feats = doc_feat.reshape(1,-1)
        else:
            self.total_feats = np.vstack([self.total_feats, doc_feat])

    def batch_add_documents(self, doc_ids:List[str], documents:List[List[str]]) -> bool:
        """
        批量添加文档
        
        参数:
        - doc_ids: 文档名称
        - documents: 文档内容
        """
        self.doc_id_list = np.array(list(self.doc_id_list) + doc_ids, dtype=object)
        docs_feat = self.encoder_model.encode(documents)
        docs_feat = normalize(docs_feat)
        
        if self.total_feats is None:
            if docs_feat.ndim == 1:
                docs_feat = docs_feat.reshape(1, -1)
            self.total_feats = docs_feat
        else:
            self.total_feats = np.vstack([self.total_feats, docs_feat])

        self.total_size += len(doc_ids)
        return True

    def delete_document(self, doc_id: int) -> bool:
        if sum(doc_id == self.doc_id_list) == 0:
            return False
        
        idx = np.where(doc_id == self.doc_id_list)[0]
        self.total_feats = np.delete(self.total_feats, idx, 0)
        self.doc_id_list = self.doc_id_list[self.doc_id_list != doc_id]
        return True

    def query_by_text(self, query: str, top_n=10) -> List[Any]:
        query_feat = self.encoder_model.encode(query)
        query_feat = normalize(query_feat.reshape(1, -1))
        
        score = np.dot(query_feat, self.total_feats.T)[0]
        
        topn_index = score.argsort()[::-1][:top_n]
        topn_score = score[topn_index]

        return [
            (self.doc_id_list[i], round(sc, 4)) for i, sc in zip(topn_index, topn_score)
        ]
    
    def query_by_feat(self, query_feat: np.ndarray, top_n=10) -> List[Any]:
        query_feat = normalize(query_feat.reshape(1, -1))
        
        score = np.dot(query_feat, self.total_feats.T)[0]
        
        topn_index = score.argsort()[::-1][:top_n]
        topn_score = score[topn_index]

        return [
            (self.doc_id_list[i], round(sc, 4)) for i, sc in zip(topn_index, topn_score)
        ]
