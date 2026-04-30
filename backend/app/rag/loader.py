"""
PathForge RAG: Course Loader
Loads, cleans, and preprocesses EdX courses dataset for FAISS embedding.
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
        self.required_columns = [
            "Course Name", "Subject", "Level", "Course Effort", 
            "Institution", "Description"
        ]
    
    def load_and_clean(self) -> List[Document]:
        """Load CSV, clean data, create embedding text, return Documents."""
        logger.info(f"Loading courses from {self.data_path}")
        
        # Load CSV
        df = pd.read_csv(self.data_path)
        logger.info(f"Loaded {len(df)} raw courses")
        
        # Verify required columns exist
        missing_cols = [col for col in self.required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing columns: {missing_cols}")
        
        # Select only required columns
        df = df[self.required_columns].copy()
        
        # Drop rows with missing Description (critical for embeddings)
        initial_count = len(df)
        df = df.dropna(subset=["Description"])
        logger.info(f"Dropped {initial_count - len(df)} rows without Description")
        
        # Create combined text field for embedding
        df["embedding_text"] = (
            df["Course Name"] + ". " +
            "Subject: " + df["Subject"] + ". " +
            "Level: " + df["Level"] + ". " +
            "Institution: " + df["Institution"] + ". " +
            df["Description"]
        )
        
        # Create Documents with metadata
        documents = []
        for _, row in df.iterrows():
            doc = Document(
                page_content=row["embedding_text"],
                metadata={
                    "course_name": str(row["Course Name"]),
                    "subject": str(row["Subject"]),
                    "level": str(row["Level"]),
                    "effort": str(row["Course Effort"]),
                    "institution": str(row["Institution"]),
                    "description": str(row["Description"])
                }
            )
            documents.append(doc)
        
        logger.info(f"Created {len(documents)} Documents ready for embedding")
        return documents

if __name__ == "__main__":
    loader = CourseLoader()
    docs = loader.load_and_clean()
    print(f"Sample: {docs[0].page_content[:200]}...")
    print(f"Metadata: {docs[0].metadata}")
    
    