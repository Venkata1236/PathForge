"""
PathForge RAG: Course Loader
"""

import pandas as pd
import logging
from typing import List
from pathlib import Path
from langchain.docstore.document import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default effort by difficulty since CSV has no effort column
EFFORT_BY_LEVEL = {
    "introductory": "2-3 hours per week",
    "beginner": "2-3 hours per week",
    "intermediate": "4-6 hours per week",
    "advanced": "6-8 hours per week",
    "expert": "8-10 hours per week"
}


class CourseLoader:
    def __init__(self, data_path: str = "data/EdX.csv"):
        self.data_path = Path(data_path)

    def load_and_clean(self) -> List[Document]:
        logger.info(f"Loading courses from {self.data_path}")

        df = pd.read_csv(self.data_path)
        logger.info(f"Loaded {len(df)} raw courses")
        logger.info(f"Available columns: {list(df.columns)}")

        # Fill effort from level since CSV has no effort column
        df["effort"] = df["Difficulty Level"].str.lower().map(EFFORT_BY_LEVEL).fillna("3-5 hours per week")

        # Create embedding text
        df["embedding_text"] = (
            "Course: " + df["Name"].astype(str) + ". " +
            "Institution: " + df["University"].astype(str) + ". " +
            "Level: " + df["Difficulty Level"].astype(str) + ". " +
            df["Course Description"].fillna(df["About"].fillna("No description")).astype(str)
        )

        # Drop rows with very short embedding text
        initial_count = len(df)
        df = df[df["embedding_text"].str.len() > 50]
        logger.info(f"Dropped {initial_count - len(df)} rows without meaningful description")

        documents = []
        for _, row in df.iterrows():
            doc = Document(
                page_content=row["embedding_text"],
                metadata={
                    "course_name": str(row["Name"]),
                    "institution": str(row["University"]),
                    "level": str(row["Difficulty Level"]),
                    "effort": str(row["effort"]),
                    "description": str(row["Course Description"]) if pd.notna(row.get("Course Description")) else "",
                    "about": str(row["About"]) if pd.notna(row.get("About")) else "",
                    "link": str(row["Link"]) if pd.notna(row.get("Link")) else ""
                }
            )
            documents.append(doc)

        logger.info(f"Created {len(documents)} Documents ready for embedding")
        return documents


if __name__ == "__main__":
    loader = CourseLoader()
    docs = loader.load_and_clean()
    print(f"✅ {len(docs)} documents")
    print(f"Sample effort: {docs[0].metadata['effort']}")
    print(f"Sample metadata: {docs[0].metadata}")