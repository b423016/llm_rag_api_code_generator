LLM + RAG-Based Function Execution API
Features
Dynamic Function Retrieval:
Uses vector search with FAISS and an open-source Sentence Transformer model (all-MiniLM-L6-v2) to convert function descriptions into embeddings for accurate semantic matching.

Exact Match Fallback:
Checks for an exact match of function names (case-insensitive) before performing vector search, ensuring that custom functions are correctly retrieved.

Custom Function Support:
Provides an endpoint (/add_function) to add custom function metadata (name and description). The vector index is updated dynamically.

Session Management:
Maintains session-based history for prompts and responses, which can be retrieved via the /history/{session_id} endpoint.

Enhanced Logging & Monitoring:
Implements logging using Python’s built-in logging module for improved debugging and monitoring.

Streamlit Frontend:
Offers a complete user interface that includes all endpoints:

Execute Function (POST /execute)

List Available Commands (GET /commands)

Copy Code To File (POST /copy)

Add Custom Function (POST /add_function)

Get History (GET /history/{session_id})

Project Structure

LLM_RAG_API/
├── README.md                 # Project overview and instructions
├── requirements.txt          # Python dependencies
├── main.py                   # FastAPI application entry point (with endpoints, session management, and logging)
├── automation_functions.py   # Predefined automation functions (e.g., open_chrome, open_calculator)
├── vector_store.py           # Builds FAISS index for function metadata and supports custom functions
├── rag_retrieval.py          # Retrieves the best-matching function (exact match fallback + semantic search)
├── code_generator.py         # Generates formatted Python code snippets with Markdown syntax highlighting
├── utils.py                  # Session management utilities (in-memory caching, cleanup)
└── streamlit_app.py          # Streamlit UI for interacting with the API endpoi

uvicorn main:app --reload

1. POST /execute

{
  "prompt": "open chrome",
  "session_id": "1"  // optional
}

Response example
{
  "function": "open_chrome",
  "code": "```python\nfrom automation_functions import open_chrome\n\n...```"
}


streamlit run streamlit_app.py
