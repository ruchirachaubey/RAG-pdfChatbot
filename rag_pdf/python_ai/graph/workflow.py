from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from models.state import GraphState
from services.summarizer import summarize
from services.rag_tool import retrieve_context

# Initialize your LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
)


# Summarizer node
def summarizer_node(state: GraphState):
    last = state.messages[-1].content
    return {"summary": summarize(last)}

# RAG node (v1.2.10 compatible)
def rag_node(state: GraphState):
    # 1️⃣ Retrieve context using your tool function
    context = retrieve_context(state.messages[-1].content)

    # 2️⃣ Pass it to LLM manually
    prompt = f"Use the following context to answer the question:\n{context}\nQuestion: {state.messages[-1].content}"
    response = llm.generate([prompt])[0]  # v1.2.10 returns a list of outputs

    # 3️⃣ Return as HumanMessage
    return {"messages": [HumanMessage(content=response)]}

# Build the graph
def build_graph():
    g = StateGraph(GraphState)

    g.add_node("summarizer", summarizer_node)
    g.add_node("rag", rag_node)

    g.set_entry_point("summarizer")
    g.add_edge("summarizer", "rag")
    g.set_finish_point("rag")

    return g.compile()

# Compile the graph
app = build_graph()