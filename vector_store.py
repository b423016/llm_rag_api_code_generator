import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# List of function metadata dictionaries
function_metadata = [
    {
        "function_name": "open_chrome",
        "description": "Opens the default web browser to google.com."
    },
    {
        "function_name": "open_calculator",
        "description": "Opens the calculator application."
    },
    {
        "function_name": "open_notepad",
        "description": "Opens a text editor like notepad on Windows or gedit on Linux."
    },
    {
        "function_name": "get_cpu_usage",
        "description": "Retrieves the current CPU usage percentage."
    },
    {
        "function_name": "get_ram_usage",
        "description": "Retrieves the current RAM usage percentage."
    },
    {
        "function_name": "run_shell_command",
        "description": "Executes a shell command and returns its output."
    },
    {
        "function_name": "open_file_explorer",
        "description": "Opens the file explorer."
    },
    {
        "function_name": "list_directory",
        "description": "Lists the contents of a directory."
    }
]

model = SentenceTransformer("all-MiniLM-L6-v2")

descriptions = [item["description"] for item in function_metadata]
embeddings = model.encode(descriptions, convert_to_numpy=True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension) #l2 norm distance
index.add(embeddings)

def search_function(query: str, k: int = 1):
#k nearest neighbour search
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, k)
    best_index = indices[0][0]
    return function_metadata[best_index]

def add_custom_function(function_name: str, description: str):
   # register new function and rebuild the index
    new_entry = {"function_name": function_name, "description": description}
    function_metadata.append(new_entry)
    descriptions = [item["description"] for item in function_metadata]
    new_embeddings = model.encode(descriptions, convert_to_numpy=True)
    index.reset()
    index.add(new_embeddings)
    return new_entry
