from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub
from langchain.llms import OpenAI
import os

from fastapi import FastAPI,File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path

import logging


os.environ["OPENAI_API_KEY"] = "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"
# pdf_file = r"./model/CIS-OBE-handout.pdf"

def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    print("PDF is loaded succcessfully.")        
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    print("Chunking successful.")
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    print("Index created successfully.")
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = OpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    print ("Chain with memory created.")
    return conversation_chain




app = FastAPI()
chain = None  # Global variable to store the conversation chain


@app.post("/process_pdf")
async def process_pdf(pdf_path: str):
    global chain  # Access the global variable


    # Validate if the provided path exists
    pdf_path = Path(pdf_path)
    # if not pdf_path.is_file():
    #     return JSONResponse(content={"error": "Invalid PDF file path"}, status_code=400)

    # Call your processing function here using the pdf_path
    # For example:
    # get pdf text
    raw_text = get_pdf_text(pdf_path)

    # get the text chunks
    text_chunks = get_text_chunks(raw_text)

    # create vector store
    vectorstore = get_vectorstore(text_chunks)

    # create conversation chain
    chain = get_conversation_chain(vectorstore)

    # Return the result or any other response
    return {"message": "PDF processing started. Waiting for your query"}



@app.post("/process_query")
async def process_query(query_data: dict):
    # print (query_data)

    global chain  # Access the global variable


    if chain is None:
        raise HTTPException(status_code=400, detail="Conversation chain not initialized")


    query = query_data.get("query", "")

    # Process the query using the existing chain
    output = chain.run(query)
    # print (output)

    # Return the output or any other response
    return {"output": output}



# #Check the working
# while True:
#     query = input("Enter your query: ")

#     output = chain.run(query)
#     print(output)









# def main():
#      # get pdf text
#     raw_text = get_pdf_text(pdf_file)

#     # get the text chunks
#     text_chunks = get_text_chunks(raw_text)

#     # create vector store
#     vectorstore = get_vectorstore(text_chunks)

#     # create conversation chain
#     chain = get_conversation_chain(vectorstore)


#     #Check the working
#     while True:
#         query = input("Enter your query: ")

#         output = chain.run(query)
#         print(output)


# if __name__ == '__main__':
#     main()