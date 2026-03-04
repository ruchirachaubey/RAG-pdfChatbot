from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
)


def summarize(text: str) -> str:
    prompt = f"Summarize this document:\n{text}"
    return llm.invoke(prompt).content