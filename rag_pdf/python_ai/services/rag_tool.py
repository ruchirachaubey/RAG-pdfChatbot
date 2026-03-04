from langchain.tools import tool
from services.pdf_ingest import get_vectorstore

@tool
def retrieve_context(query: str, thread_id: str) -> str:
    """
    Retrieves the top 4 most relevant documents from the vectorstore for a given query and thread_id.
    """
    store = get_vectorstore(thread_id)
    if not store:
        return "No document indexed."

    docs = store.similarity_search(query, k=4)
    return "\n\n".join(d.page_content for d in docs)