from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub
from langchain.llms import OpenAI
import os


os.environ["OPENAI_API_KEY"] = "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"
pdf_file = r"./model/CIS-OBE-handout.pdf"

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


def main():
     # get pdf text
    raw_text = get_pdf_text(pdf_file)

    # get the text chunks
    text_chunks = get_text_chunks(raw_text)

    # create vector store
    vectorstore = get_vectorstore(text_chunks)

    # create conversation chain
    chain = get_conversation_chain(vectorstore)


    #Check the working
    while True:
        query = input("Enter your query: ")

        output = chain.run(query)
        print(output)


if __name__ == '__main__':
    main()