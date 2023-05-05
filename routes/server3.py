from fastapi import APIRouter, WebSocket, WebSocketDisconnect, UploadFile
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from pathlib import Path
import pinecone
import os

router = APIRouter(prefix="/api/server3", tags=["server3"])
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"),
              environment=os.getenv("PINECONE_ENV"))

UPLOAD_FOLDER = "./docs"
LOCAL_STORE = "./faiss"
INDEX_NAME = "whitepaper-docs"


def check_pinecone_index():
    list = pinecone.list_indexes()
    if not INDEX_NAME in list:
        pinecone.create_index(INDEX_NAME)


def check_faiss_index():
    if not os.path.exists(f"{LOCAL_STORE}/index.faiss"):
        faiss_index = FAISS.from_texts(
            ["This is whitepaper data."], OpenAIEmbeddings())
        faiss_index.save_local(LOCAL_STORE)


@router.post("/upload")
async def doc_upload(file: UploadFile):
    path = Path(UPLOAD_FOLDER) / file.filename
    path.write_bytes(await file.read())
    fileext = file.filename.rsplit(".", 1)[1].lower()
    if fileext == 'pdf':
        loader = PyPDFLoader(str(path))
    elif fileext == 'txt':
        loader = TextLoader(str(path))
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100)
    docs = loader.load_and_split(text_splitter)
    embeddings = OpenAIEmbeddings()
    # check_pinecone_index()
    # Pinecone.add_documents(docs, embeddings, index_name=INDEX_NAME)
    check_faiss_index()
    faiss_index = FAISS.load_local(LOCAL_STORE, OpenAIEmbeddings())
    faiss_index.add_documents(docs)
    return {"state": "success"}


template = """You are a chatbot having a conversation with a human.
You are talkative and provide lots of specific details related to crypto knowledge from whitepapers. If the you don't know the answer to a question, you must truthfully say you don't know.
Given the following extracted parts of a long document and a question, create a final answer.

{context}

{chat_history}
Human: {human_input}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input", "context"],
    template=template
)


@router.websocket("/chat")
async def doc_chat(websocket: WebSocket):
    await websocket.accept()
    memory = ConversationBufferMemory(
        memory_key="chat_history", input_key="human_input")
    # docsearch = Pinecone.from_existing_index(
    #     index_name=INDEX_NAME, embedding=OpenAIEmbeddings())
    docsearch = FAISS.load_local(LOCAL_STORE, OpenAIEmbeddings())
    chain = load_qa_chain(llm=ChatOpenAI(temperature=0),
                          chain_type="stuff", prompt=prompt, memory=memory)
    while True:
        try:
            msg = await websocket.receive_text()
            docs = docsearch.similarity_search(msg)
            reply = chain.run(input_documents=docs, human_input=msg)
            await websocket.send_text(reply)
        except WebSocketDisconnect:
            break
