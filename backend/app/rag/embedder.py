"""
PathForge RAG: FAISS Embedder
Builds and saves FAISS index from course Documents.
"""

import os
from pathlib import Path
from loguru import logger
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from app.rag.loader import CourseLoader
from dotenv import load_dotenv

load_dotenv()


class CourseEmbedder:
    def __init__(self, index_path: str = "faiss_index"):
        self.index_path = Path(index_path)
        self.index_path.mkdir(exist_ok=True)
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    def build_index(self) -> FAISS:
        """Load courses → embed → build FAISS → save to disk."""
        logger.info("Building FAISS index from course catalog...")

        loader = CourseLoader()
        documents = loader.load_and_clean()

        logger.info(f"Embedding {len(documents)} documents with OpenAI ada-002...")
        vectorstore = FAISS.from_documents(documents, self.embeddings)

        vectorstore.save_local(str(self.index_path))
        logger.success(f"FAISS index saved to: {self.index_path}")
        logger.info(f"Total courses indexed: {len(documents)}")

        return vectorstore

    def load_index(self) -> FAISS:
        """Load existing FAISS index from disk."""
        index_file = self.index_path / "index.faiss"
        if not index_file.exists():
            raise FileNotFoundError(
                f"No FAISS index at {self.index_path}. Run build_index() first."
            )
        logger.info(f"Loading FAISS index from {self.index_path}")
        return FAISS.load_local(
            str(self.index_path),
            self.embeddings,
            allow_dangerous_deserialization=True
        )


if __name__ == "__main__":
    embedder = CourseEmbedder()

    # Build index
    index = embedder.build_index()

    # Test 5 sample queries to verify retrieval quality
    test_queries = [
        "machine learning for beginners",
        "advanced deep learning neural networks",
        "python programming fundamentals",
        "data science statistics",
        "cloud computing AWS"
    ]

    print("\n" + "="*50)
    print("FAISS RETRIEVAL TEST")
    print("="*50)
    for query in test_queries:
        docs = index.similarity_search(query, k=3)
        print(f"\n🔍 Query: '{query}'")
        for i, doc in enumerate(docs, 1):
            print(f"  {i}. {doc.metadata['course_name']}")
            print(f"     Level: {doc.metadata['level']} | {doc.metadata['institution']}")