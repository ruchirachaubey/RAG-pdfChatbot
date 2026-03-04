from fastapi import FastAPI, UploadFile
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from graph.workflow import build_graph
from services.pdf_ingest import ingest_pdf
from memory.store import memory, get_config

load_dotenv()

app = FastAPI()
graph = build_graph().with_config({"checkpointer": memory})

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile, thread_id: str):
    pdf_bytes = await file.read()
    return ingest_pdf(pdf_bytes, thread_id, file.filename)

@app.post("/chat")
def chat(thread_id: str, message: str):
    result = graph.invoke(
        {"messages": [HumanMessage(content=message)]},
        config=get_config(thread_id),
    )
    return {
        "answer": result["messages"][-1].content,
        "summary": result.get("summary"),
    }