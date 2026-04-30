"""
PathForge RAG: Course Loader
Loads, cleans, and preprocesses EdX courses dataset for FAISS embedding.
Updated for actual dataset columns: Name, University, Difficulty Level, etc.
"""

import pandas as pd
import logging
from typing import List
from pathlib import Path
from langchain.docstore.document import Document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CourseLoader:
    def __init__(self, data_path: str = "data/courses.csv"):
        self.data_path = Path(data_path)
        # Map your actual columns to our internal names
        self.column_mapping = {
            "Name": "course_name",
            "University": "institution", 
            "Difficulty Level": "level",
            "Course Description": "description",
            "About": "about"  # Secondary description field
        }
    
    def load_and_clean(self) -> List[Document]:
        """Load CSV, clean data, create embedding text, return Documents."""
        logger.info(f"Loading courses from {self.data_path}")
        
        # Load CSV
        df = pd.read_csv(self.data_path)
        logger.info(f"Loaded {len(df)} raw courses")
        logger.info(f"Available columns: {list(df.columns)}")
        
        # Verify critical columns exist
        missing_cols = ["Name", "University", "Difficulty Level", "Course Description"]
        for col in missing_cols:
            if col not in df.columns:
                raise ValueError(f"Missing critical column: {col}")
        
        # Create combined text field for embedding (prioritize Course Description)
        df["embedding_text"] = (
            "Course: " + df["Name"].astype(str) + ". " +
            "Institution: " + df["University"].astype(str) + ". " +
            "Level: " + df["Difficulty Level"].astype(str) + ". " +
            df["Course Description"].fillna(df["About"].fillna("No description")).astype(str)
        )
        
        # Filter out courses without meaningful description (less than 50 chars)
        initial_count = len(df)
        df = df[df["embedding_text"].str.len() > 50]
        logger.info(f"Dropped {initial_count - len(df)} rows without meaningful description")
        
        # Create Documents with metadata
        documents = []
        for _, row in df.iterrows():
            doc = Document(
                page_content=row["embedding_text"],
                metadata={
                    "course_name": str(row["Name"]),
                    "institution": str(row["University"]),
                    "level": str(row["Difficulty Level"]),
                    "description": str(row["Course Description"]),
                    "about": str(row["About"]) if "About" in row else "",
                    "link": str(row["Link"]) if "Link" in row else ""
                }
            )
            documents.append(doc)
        
        logger.info(f"Created {len(documents)} Documents ready for embedding")
        return documents

if __name__ == "__main__":
    loader = CourseLoader()
    docs = loader.load_and_clean()
    print(f"✅ Success: {len(docs)} documents")
    print(f"Sample metadata: {docs[0].metadata}")
    print(f"Sample content preview: {docs[0].page_content[:300]}...")