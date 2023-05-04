from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

router = APIRouter(prefix="/api/server2", tags=["server2"])

template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. The AI will also offer explanations of projects, tokenomics, whitepapers, concepts, and strategies. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{history}
Human: {input}
AI Assistant:"""
PROMPT = PromptTemplate(
    input_variables=["history", "input"], template=template)


@router.websocket("/chat")
async def sample_chat(websocket: WebSocket):
    await websocket.accept()
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    chain = ConversationChain(
        llm=llm, prompt=PROMPT, memory=ConversationBufferMemory(ai_prefix="AI Assistant"))
    while True:
        try:
            msg = await websocket.receive_text()
            reply = chain.run(input=msg)
            await websocket.send_text(reply)
        except WebSocketDisconnect:
            break
