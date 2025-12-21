import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

def get_pdf_text(pdf_docs):
    text =""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    # Initialize the Gemini Embedding model
    # 'text-embedding-004' is the stable, high-performance choice for 2025
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    # Create the FAISS index using these embeddings
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    
    return vectorstore

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    
    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", 
            accept_multiple_files=True
        )
        
        if st.button("Process"):
            with st.spinner("Processing"):
                # Get pdf text
                raw_text = get_pdf_text(pdf_docs)
                

                # Get the text chunks
                text_chunks = get_text_chunks(raw_text)
                st.write(text_chunks)

                # Create vector store
                vectorstore = get_vectorstore(text_chunks)
                st.success("Done!")

if __name__ == '__main__':
    main()