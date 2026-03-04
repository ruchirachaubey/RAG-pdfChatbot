from dotenv import load_dotenv
load_dotenv()

from graph.workflow import app
from langchain_core.messages import HumanMessage

# Fake extracted PDF text
PDF_TEXT = """
LangGraph is a library for building stateful LLM applications.
It allows graphs, parallel execution, and persistence.
RAG systems retrieve relevant documents before answering.
"""

state = {
    "pdf_text": PDF_TEXT,
    "messages": [
        HumanMessage(content="Explain this PDF briefly")
    ]
}

result = app.invoke(state)

print("\n===== SUMMARY =====")
print(result["summary"])

print("\n===== RAG ANSWER =====")
print(result["rag_answer"])