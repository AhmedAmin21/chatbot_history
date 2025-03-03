import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

# Model Calling
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Prompt For the model
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "you are a helpfull assistant you are good at history you will get asked about history questions try to answer user questios in detail and accuratly, finally i want you to answer in arabic"),
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
# Get the absolute path of the "static" directory
static_dir = os.path.join(os.path.dirname(__file__), "static")

# Ensure the static directory exists
if not os.path.exists(static_dir):
    os.makedirs(static_dir)  # Create the folder if it doesn’t exist
# Mount a folder to serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the HTML page at the root URL
@app.get("/")
def read_root():
    return FileResponse("static/index.html")


@app.post('/response')
async def get_response(request: Request):
    data = await request.json()  # Get JSON data from the request
    question = data.get("question")  # Extract 'question' from JSON
    response = chain.invoke({'text': question})
    return {"answer": response}