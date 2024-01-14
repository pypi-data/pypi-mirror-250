from typing import List, Any
import numpy as np
import cv2
from sklearn.preprocessing import normalize
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

class ColorHistogram:
    def __init__(self, 
        img_ids:List[Any]=None, 
        img_paths:List[List[str]]=None,
    ):
        """
        初始化ColorHistogram对象，用于图像检索
        
        参数:
        - img_ids: 图像名称 或 图像任意信息
        - img_paths: 图像路径
        - color_space: 
        """
        self.total_size = 0
        self.total_feats: np.ndarray = None

        self.cpu_count = cpu_count()
        self.img_id_list: np.ndarray = np.array([], dtype=object)

        if img_ids is not None:
            if len(img_ids) != len(img_paths):
                raise Exception("the count of img_ids do not math img_paths!")
            
            self.batch_add_documents(img_ids, img_paths)

    def encode(self, img_path:str) -> np.ndarray:
        img = cv2.imread(img_path)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
        return hist
    
    def update_image(self, img_id: Any, img_path: str) -> bool:
        if sum(img_id == self.img_id_list) == 0:
            return False

        idx = np.where(img_id == self.img_id_list)[0]
        self.total_feats[idx] = self.encode(img_path)

        return True

    def add_image(self, img_id: Any, img_path: str) -> bool:
        self.img_id_list = np.array(list(self.img_id_list) + [img_id], dtype=object)
        doc_feat = self.encode(img_path)
        doc_feat = doc_feat.reshape(1,-1)
        doc_feat = normalize(doc_feat)
        
        if self.total_feats is None:
            self.total_feats = doc_feat.reshape(1,-1)
        else:
            self.total_feats = np.vstack([self.total_feats, doc_feat])

    def batch_add_images(self, img_ids:List[str], img_paths:List[str]) -> bool:
        """
        批量添加文档
        
        参数:
        - doc_ids: 文档名称
        - documents: 文档内容
        """
        self.img_id_list = np.array(list(self.img_id_list) + img_ids, dtype=object)

        if len(img_paths) < 10:
            with ProcessPoolExecutor(max_workers=1) as executor:
                result = list(executor.map(self.encode, img_paths))
        else:
            with ProcessPoolExecutor(max_workers=self.cpu_count) as executor:
                result = list(executor.map(self.encode, img_paths))

        result = np.array(result)
        result = normalize(result)
        
        if self.total_feats is None:
            if result.ndim == 1:
                result = result.reshape(1, -1)
            self.total_feats = result
        else:
            self.total_feats = np.vstack([self.total_feats, result])

    def delete_image(self, img_id: int) -> bool:
        if sum(img_id == self.img_id_list) == 0:
            return False
        
        idx = np.where(img_id == self.img_id_list)[0]
        self.corpus_feats = np.delete(self.corpus_feats, idx, 0)
        self.img_id_list = self.img_id_list[self.img_id_list != img_id]
        return True

    def query_by_image(self, img_path: str, top_n=10) -> List[Any]:
        query_feat = self.histogram_feat(img_path)
        query_feat = normalize(query_feat.reshape(1, -1))
        
        score = np.dot(query_feat, self.corpus_feats.T)[0]
        
        topn_index = score.argsort()[::-1][:top_n]
        topn_score = score[topn_index]

        return [
            (self.doc_id_list[i], round(sc, 4)) for i, sc in zip(topn_index, topn_score)
        ]
    
    def query_by_feat(self, query_feat: np.ndarray, top_n=10) -> List[Any]:
        query_feat = normalize(query_feat.reshape(1, -1))
        
        score = np.dot(query_feat, self.corpus_feats.T)[0]
        
        topn_index = score.argsort()[::-1][:top_n]
        topn_score = score[topn_index]

        return [
            (self.doc_id_list[i], round(sc, 4)) for i, sc in zip(topn_index, topn_score)
        ]
