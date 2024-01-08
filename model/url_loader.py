from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub
from langchain.llms import OpenAI
from langchain_community.document_loaders import WebBaseLoader
import os



os.environ["OPENAI_API_KEY"] = "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"



def get_web_text(url):
    loader = WebBaseLoader(url)
    web_page = loader.load()       
    content = web_page[0].page_content
    print("Web page content loaded successfully.")
    print(type(content))
    print(content)
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


def main():

    url = input("Enter the website url : ")
    
     # get url content
    content = get_web_text(url)

    # get the text chunks
    text_chunks = get_text_chunks(content)

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