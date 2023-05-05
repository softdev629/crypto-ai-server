from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pinecone
import os

from routes import server1, server2, server3

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

app.include_router(server1.router)
app.include_router(server2.router)
app.include_router(server3.router)

if __name__ == "__main__":
    if not os.path.exists("./docs"):
        os.makedirs("./docs")
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
