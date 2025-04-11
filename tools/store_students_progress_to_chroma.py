import chromadb
from chromadb.config import Settings
from crewai.tools import tool
import time

chroma_client = chromadb.PersistentClient(path="./admission_db")

# Create or get the collection
admission_collection = chroma_client.get_or_create_collection(name="admission_progress")


@tool
def store_students_progress_to_chroma(student_ids: list[str],names: list[str],summaries: list[str]) -> str:
    """
    Store multiple students' admission progress in ChromaDB.

    Args:
        student_ids (list[str]): List of unique student IDs.
        names (list[str]): List of student full names.
        summaries (list[str]): List of admission status summaries.

    Returns:
        str: Confirmation message after storing.
    """
    if not (len(student_ids) == len(names) == len(summaries)):
        return "❌ Error: student_ids, names, and summaries must have the same length."

    metadatas = [{"name": name} for name in names]

    admission_collection.upsert(
        documents=summaries,
        ids=student_ids,
        metadatas=metadatas
    )
    time.sleep(5)
    return f"✅ Stored {len(student_ids)} students in ChromaDB."