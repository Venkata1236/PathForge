"""
PathForge RAG: FAISS Retriever
Wraps FAISS with metadata filtering for level-appropriate course retrieval.
"""

from loguru import logger
from langchain_community.vectorstores import FAISS
from app.rag.embedder import CourseEmbedder
from typing import List, Optional


# Level mapping — beginners don't get Advanced courses
LEVEL_FILTER_MAP = {
    "beginner":     ["introductory", "beginner"],
    "intermediate": ["introductory", "beginner", "intermediate"],
    "advanced":     ["introductory", "beginner", "intermediate", "advanced", "expert"]
}


class CourseRetriever:
    def __init__(self, index_path: str = "faiss_index"):
        embedder = CourseEmbedder(index_path=index_path)
        self.vectorstore = embedder.load_index()
        logger.info("CourseRetriever ready")

    def search(
        self,
        query: str,
        k: int = 5,
        experience_level: Optional[str] = "intermediate"
    ) -> List[dict]:
        """
        Search FAISS and filter by learner experience level.
        Fetches k*3 candidates first, then filters by level.
        Falls back to unfiltered if filtering removes everything.
        """
        logger.debug(f"Searching: '{query}' | level={experience_level} | k={k}")

        # Fetch extra candidates to allow filtering
        candidates = self.vectorstore.similarity_search(query, k=k * 3)

        allowed_levels = LEVEL_FILTER_MAP.get(
            experience_level.lower() if experience_level else "intermediate",
            LEVEL_FILTER_MAP["intermediate"]
        )

        # Filter by level (case-insensitive)
        filtered = [
            doc for doc in candidates
            if any(
                allowed.lower() in doc.metadata.get("level", "").lower()
                for allowed in allowed_levels
            )
        ]

        # Fallback: if filtering removes all results
        if not filtered:
            logger.warning(f"Level filter removed all results for '{query}'. Using unfiltered.")
            filtered = candidates

        # Return top-k as dicts
        results = []
        for doc in filtered[:k]:
            results.append({
                "course_name": doc.metadata.get("course_name", "Unknown"),
                "institution": doc.metadata.get("institution", "Unknown"),
                "level": doc.metadata.get("level", "Unknown"),
                "effort": doc.metadata.get("effort", "Unknown"),
                "description": doc.metadata.get("description", ""),
                "about": doc.metadata.get("about", ""),
                "link": doc.metadata.get("link", "")
            })

        logger.debug(f"Returned {len(results)} courses for '{query}'")
        return results


if __name__ == "__main__":
    retriever = CourseRetriever()

    tests = [
        ("learn python for data science", "beginner"),
        ("machine learning algorithms", "intermediate"),
        ("deep learning transformers NLP", "advanced"),
        ("SQL databases for analysts", "beginner"),
        ("kubernetes docker devops", "intermediate"),
    ]

    for query, level in tests:
        results = retriever.search(query, k=2, experience_level=level)
        print(f"\n🔍 '{query}' [{level}]")
        for r in results:
            print(f"  ✅ {r['course_name']} ({r['level']}) — {r['institution']}")