import os
from dotenv import load_dotenv
from fastapi import FastAPI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

# Model Calling
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Prompt For the model
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant specializing in history. You will be asked history-related questions, and you should answer them in detail and accurately. Finally, respond in Arabic."),
        ("user", "{text}")
    ]
)

# Parser
parser = StrOutputParser()

# Chain
chain = prompt|model|parser

#response = chain.invoke({'text':'how the egyption built the pyramids'})
#print(response)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post('/response')
async def get_response(question:str):
    
    response = chain.invoke({'text': question})
    return {"answer": response}
