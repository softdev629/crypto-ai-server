from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType

from tools import LatestInfoTool

router = APIRouter(prefix="/api/server1", tags=["server1"])


@router.websocket("/chat")
async def google_chat(websocket: WebSocket):
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
