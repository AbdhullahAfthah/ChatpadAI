from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub
from langchain.llms import OpenAI
from langchain_community.document_loaders import WebBaseLoader
import os

from fastapi import FastAPI,File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path



os.environ["OPENAI_API_KEY"] = "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"



def get_web_text(url):
    loader = WebBaseLoader(url)
    web_page = loader.load()       
    content = web_page[0].page_content
    print("Web page content loaded successfully.")
    # print(type(content))
    # print(content)
    return content


def get_text_chunks(content):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(content)
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


# Allow all origins, credentials, methods, and headers for testing purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... your routes and other code ...


@app.post("/process_url")
async def process_pdf(data: dict):
    global chain  # Access the global variable
    print(data)
    print(type(data))
    url = data.get("url","")

    print(url)
    print(type(url))


    # get pdf text
    raw_text = get_web_text(url)

    # get the text chunks
    text_chunks = get_text_chunks(raw_text)

    # create vector store
    vectorstore = get_vectorstore(text_chunks)

    # create conversation chain
    chain = get_conversation_chain(vectorstore)

    # Return the result or any other response
    return {"message": "URL processing started. Waiting for your query"}



@app.post("/url_query")
async def url_query(request: dict):
    # print(type(request))
    # print (request)

    

    # print(type(query))
    # print (query)

    global chain  # Access the global variable


    if chain is None:
        raise HTTPException(status_code=400, detail="Conversation chain not initialized")

    
    query = request.get("query", "")

     
    # Process the query using the existing chain
    output = chain.run(query)
    # print (output)

    # Return the output or any other response
    return {"output": output}




# def main():

#     url = input("Enter the website url : ")
    
#      # get url content
#     content = get_web_text(url)

#     # get the text chunks
#     text_chunks = get_text_chunks(content)

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