from vector_store import search_function, function_metadata

def retrieve_function(query: str):
    """
    Retrieves the best-matching function name.
    First, it checks for an exact match among the function names.
    If none is found, it uses vector search to find the most semantically similar function.
    
    Args:
        query (str): The user prompt.
        
    Returns:
        str: The function name corresponding to the match.
    """
    query_lower = query.lower().strip()
    for item in function_metadata:
        if item["function_name"].lower().strip() == query_lower:
            return item["function_name"]
    
    result = search_function(query)
    return result["function_name"]
