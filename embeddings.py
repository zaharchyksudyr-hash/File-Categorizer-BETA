
# аналогічно basic_categorizer.py є тестовим рішенням, але лише з бібліотекою sentence-transformers для векторних представлень embeddings.

# from __future__ import annotations
#
# import hashlib
# import json
# from dataclasses import dataclass
# from functools import lru_cache
# from pathlib import Path
#
# import numpy as np
# 
# Для кожного тексту створюється унікальний SHA1-хеш.
# 
# def _sha1(s: str) -> str:
#     return hashlib.sha1(s.encode('utf-8')).hexdigest()
#
# @lru_cache(maxsize=4)
# def _load_model(model_name: str):
#     try:
#         from sentence_transformers import SentenceTransformer
#         print("MODEL LOAD", model_name)
#         return SentenceTransformer(model_name)
#     except Exception as e:
#         raise RuntimeError(f"Failed to load embedding model: {e}")
#
# @dataclass(frozen=True)
# class EmbeddingResult:
#     vector: np.ndarray
#     model_name: str
#
# Ініціалізація embeddings моделі sentence-transformers 
# 
# class Embedder:
#
#         def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", cache_dir: str = "data/cache"):
#             self.model_name = model_name
#             self.cache_dir = Path(cache_dir)
#             self.cache_dir.mkdir(parents=True, exist_ok=True)
#
#         def _get_model(self):
#             return _load_model(self.model_name)
#
#  Тут відбувається генерація ембеддинга одного тексту
# Ця частина забезпечує кешування як самої моделі (через lru_cache), так і вже обчислених ембеддингів (у JSON-файлах), 
# підтримує побудову векторів для одного або кількох текстів та надає функцію для обчислення косинусної схожості(cosine_similarity), яка використовується для оцінки семантичної близькості текстів.
# 
#         def embed_text(self, text: str) -> EmbeddingResult:
#             text = (text or "").strip()
#             model = self._get_model()
#
#             if not text:
#                 dim = model.get_sentence_embedding_dimension()
#                 return EmbeddingResult(vector=np.zeros(dim, dtype=np.float32), model_name=self.model_name)
#
#             key = _sha1(self.model_name + "|" + text)
#             cache_path = self.cache_dir / f"{key}.json"
#
#             if cache_path.exists():
#                 try:
#                     data = json.loads(cache_path.read_text(encoding="utf-8"))
#                     vec = np.array(data["vector"], dtype=np.float32)
#                     return EmbeddingResult(vector=vec, model_name=data["model_name"])
#                 except Exception:
#                     pass
#
#             vec = model.encode(text, normalize_embeddings=True)
#             vec = np.array(vec, dtype=np.float32)
#             try:
#                 cache_path.write_text(
#                     json.dumps({"model_name": self.model_name, "vector": vec.tolist()}, ensure_ascii=False),
#                     encoding="utf-8",
#                 )
#             except Exception:
#                 pass
#             return EmbeddingResult(vector=vec, model_name=self.model_name)
#
#         def embed_many(self, texts: list[str]) -> np.ndarray:
#             model = self._get_model()
#             cleaned = [(t or "").strip() for t in texts]
#             vecs = model.encode(cleaned, normalize_embeddings=True)
#             return np.array(vecs, dtype=np.float32)
#
# def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
#     if a.size == 0 or b.size == 0:
#         return 0.0
#     denom = np.linalg.norm(a) * np.linalg.norm(b)
#     if denom == 0:
#         return 0.0
#     return float(np.dot(a, b) / denom)
