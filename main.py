import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_retrieval import retrieve_function
from code_generator import generate_code
from utils import add_to_session, get_session
from vector_store import add_custom_function, function_metadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class ExecutionRequest(BaseModel):
    prompt: str
    session_id: str = None

class CustomFunctionRequest(BaseModel):
    function_name: str
    description: str

@app.post("/execute")
def execute_function(request: ExecutionRequest):
    """
    processes the user request search for the exact match in hte vector then if not ofunfd goes with semantic search
    """
    query = request.prompt
    logger.info(f"Received Request: {query}")

    function_name = retrieve_function(query)
    logger.info(f"Retrieved Function: {function_name}")

    if not function_name:
        logger.error("No function found for the given prompt.")
        raise HTTPException(status_code=404, detail="No matching function found")

    code_snippet = generate_code(function_name)
    
    if request.session_id:
        add_to_session(request.session_id, request.prompt, code_snippet)

    return {"function": function_name, "code": code_snippet}

@app.get("/commands")
def list_available_commands():
    """
    a list of all available function commands.
    """
    commands = [item["function_name"] for item in function_metadata]
    return {"available_commands": commands}

@app.post("/copy")
def copy_code_to_file(request: ExecutionRequest):
    """
    directly saves the code in a .py file and returns the path
    """
    query = request.prompt
    function_name = retrieve_function(query)

    if not function_name:
        raise HTTPException(status_code=404, detail="No matching function found")

    code_snippet = generate_code(function_name)
    cleaned_code = code_snippet.replace("```python", "").replace("```", "").strip()

    file_path = f"{function_name}.py"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(cleaned_code)

    return {"message": f"Code saved to {file_path}", "file_path": os.path.abspath(file_path)}

@app.post("/add_function")
def add_function(request: CustomFunctionRequest):
    """
    Adds a custom function to the registry.
    not fully developed yet
    """
    new_func = add_custom_function(request.function_name, request.description)
    logger.info(f"Custom function added: {new_func}")
    return {"message": "Custom function added", "function": new_func}

@app.get("/history/{session_id}")
def get_history(session_id: str):
    """
    the history of the session
    """
    history = get_session(session_id)
    return {"session_id": session_id, "history": history}
