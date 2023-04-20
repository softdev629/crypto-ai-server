from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from tools import LatestInfoTool

load_dotenv()

app = FastAPI()
origins = []
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.websocket("/api/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    llm = ChatOpenAI(temperature=0, model_name="gpt-4")
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    tools = [LatestInfoTool()]
    agent_chain = initialize_agent(
        tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
    while (True):
        try:
            msg = await websocket.receive_text()
            reply = agent_chain.run(input=msg)
            await websocket.send_text(reply)
        except WebSocketDisconnect:
            break


@app.get('/')
async def get():
    return "Hello World!"

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=9000, reload=True)
