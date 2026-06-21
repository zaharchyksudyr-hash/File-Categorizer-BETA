# from __future__ import annotations
#
# from dataclasses import dataclass
# from typing import Iterable
#
# from core.keywords_categorizer import (CATEGORY_KEYWORDS, MAIN_CATEGORY_DESCRIPTIONS)
# from core.embeddings import Embedder, cosine_similarity
#
#
# @dataclass(frozen=True)
# class CategoryResult:
#     main_category: str
#     subcategory: str
#     score: float
#     method: str
#
# class EmbedderCategorizer:
#     def __init__(self, embedder: Embedder, shortlist_size: int = 5, sub_shortlist_size: int = 5, embedding_threshold: float = 0.50, sub_embedding_threshold: float = 0.30, subcategory_keyword_threshold: int = 1):
#         self.embedder = embedder or Embedder()
#         self.shortlist_size = shortlist_size
#         self.sub_shortlist_size = sub_shortlist_size
#         self.embedding_threshold = embedding_threshold
#         self.sub_embedding_threshold = sub_embedding_threshold
#         self.subcategory_keyword_threshold = subcategory_keyword_threshold
#         self.main_category_vectors = None
#         self.subcategory_vectors = None
#
#     def _ensure_vectors(self) -> None:
#         if self.main_category_vectors is None:
#             self.main_category_vectors = {
#                 category: self.embedder.embed_text(description).vector
#                 for category, description in MAIN_CATEGORY_DESCRIPTIONS.items()
#             }
#
#         if self.subcategory_vectors is None:
#             self.subcategory_vectors = self._build_subcategory_vectors()
#
#     def _build_subcategory_vectors(self):
#         result = {}
#         for main_category, subcategories in CATEGORY_KEYWORDS.items():
#             result[main_category] = {}
#             for subcategory, keywords in subcategories.items():
#                 sub_text = " ".join([subcategory, *keywords])
#                 result[main_category][subcategory] = self.embedder.embed_text(sub_text).vector
#         return result
#
#     @staticmethod
#     def _normalize_text(text: str) -> str:
#         return " ".join((text or "").lower().split())
#
#     @staticmethod
#     def _count_keyword_hits(text:str, keywords: Iterable[str]) -> int:
#         text_lower = text.lower()
#         score = 0
#         for kw in keywords:
#             kw_norm = kw.strip().lower()
#             if kw_norm and kw_norm in text_lower:
#                 score += 1
#         return score
#
#     def _embedding_shortlist(self, text: str) -> list[tuple[str, float]]:
#         if not text.strip():
#             return [("Misc", 0.0)]
#         text_vector = self.embedder.embed_text(text).vector
#         scored: list[tuple[str, float]] = []
#
#         for category, category_vector in self.main_category_vectors.items():
#             score = cosine_similarity(text_vector, category_vector)
#             scored.append((category, score))
#
#         scored.sort(key=lambda x: x[1], reverse=True)
#         return scored[: self.shortlist_size]
#
#     def _keyword_main_category_from_shortlist(self, text: str, shortlist: list[tuple[str, float]]) -> tuple[str, int]:
#         best_main = "Misc"
#         best_hits = 0
#         for main_category, _emb_score in shortlist:
#             subcategories = CATEGORY_KEYWORDS.get(main_category, {})
#             total_hits = 0
#             for keywords in subcategories.values():
#                 total_hits += self._count_keyword_hits(text, keywords)
#
#             if total_hits > best_hits:
#                 best_hits = total_hits
#                 best_main = main_category
#         return best_main, best_hits
#
#     def _subcategory_embedding_shortlist(self, text: str, main_category: str) -> list[tuple[str, float]]:
#         if not text.strip():
#             return [("Misc", 0.0)]
#
#         text_vector = self.embedder.embed_text(text).vector
#         scored: list[tuple[str, float]] = []
#
#         subcategory_vectors = self.subcategory_vectors.get(main_category, {})
#         for subcategory, subcategory_vector in subcategory_vectors.items():
#             score = cosine_similarity(text_vector, subcategory_vector)
#             scored.append((subcategory, score))
#             if not scored:
#                 return [("Misc", 0.0)]
#         scored.sort(key=lambda x: x[1], reverse=True)
#         return scored[: self.sub_shortlist_size]
#
#     def _keyword_subcategory_from_shortlist(self, text: str, main_category: str, shortlist: list[tuple[str, float]]) -> tuple[str, int]:
#         subcategories = CATEGORY_KEYWORDS.get(main_category, {})
#         best_subcategory = "Misc"
#         best_score = 0
#
#         for subcategory, _emb_score in shortlist:
#             keywords = subcategories.get(subcategory, [])
#             hits = self._count_keyword_hits(text, keywords)
#             if hits > best_score:
#                 best_score = hits
#                 best_subcategory = subcategory
#
#             if best_score < self.subcategory_keyword_threshold:
#                 return "Misc", best_score
#         return best_subcategory, best_score
#
#     def categorize(self, text: str) -> tuple[str, float, str]:
#         self._ensure_vectors()
#         text = self._normalize_text(text)
#         if not text:
#             return "Misc/Empty", 0.0, "EMPTY"
#         main_shortlist = self._embedding_shortlist(text)
#         best_main_embedding_category, best_main_embedding_score = main_shortlist[0]
#         shortlist_main, shortlist_main_hits = self._keyword_main_category_from_shortlist(text, main_shortlist)
#         if shortlist_main_hits == 0 and best_main_embedding_score >= self.embedding_threshold:
#             main_category = best_main_embedding_category
#             main_method = "EMBED_SHORTLIST"
#         elif shortlist_main_hits > 0:
#             main_category = shortlist_main
#             main_method = "EMBED+KEYWORDS_SHORTLIST"
#         else:
#             main_category = "Misc"
#             main_method = "LOW_CONFIDENCE"
#         if main_category == "Misc":
#             return "Misc/LowConfidence", best_main_embedding_score, main_method
#
#         sub_shortlist = self._subcategory_embedding_shortlist(text, main_category)
#         if not sub_shortlist:
#             return f"{main_category}/Misc", best_main_embedding_score, f"{main_method}|NO_SUB_SHORTLIST"
#         best_sub_embedding_category, best_sub_embedding_score = sub_shortlist[0]
#         shortlist_sub, shortlist_sub_hits = self._keyword_subcategory_from_shortlist(text, main_category, sub_shortlist)
#         if shortlist_sub_hits >= self.subcategory_keyword_threshold:
#             sub_category = shortlist_sub
#             sub_method = "EMBED+KEYWORDS_SUB"
#         elif best_sub_embedding_score >= self.sub_embedding_threshold:
#             sub_category = best_sub_embedding_category
#             sub_method = "EMBED_SUB"
#         else:
#             sub_category = "Misc"
#             sub_method = "LOW_CONFIDENCE_SUB"
#
#         final_category = f"{main_category}/{sub_category}"
#         final_method = f"{main_method}|{sub_method}"
#
#         return final_category, best_main_embedding_score, final_method