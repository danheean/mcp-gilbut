from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
import logging

from mcp.server.fastmcp import FastMCP
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("PDF-RAG")

PDF_PATH = os.getenv("PDF_PATH")
print(f"PDF_PATH: {PDF_PATH}")

loader = PyPDFLoader(PDF_PATH)
pages = loader.load()
print(f"Loaded {len(pages)} documents")


splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(pages)
print(f"Split into {len(docs)} documents")

embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

vectorestore = Chroma.from_documents(docs, embeddings)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorestore.as_retriever(),
)

@mcp.tool()
def ask_pdf(query: str) -> str:
    """Ask the PDF for the query"""
    logging.info(f"Received query: {query}")

    response = qa_chain.run(query)
    return response

if __name__ == "__main__":
    mcp.run(transport="stdio")