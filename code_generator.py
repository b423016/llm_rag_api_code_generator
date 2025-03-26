def generate_code(function_name: str, additional_params: dict = None):
    """
    geneartes a python script as mentioned in the example with markdown and copy funciton 
    """
    code_template = f"""```python
from automation_functions import {function_name}

def main():
    try:
        result = {function_name}() 
        print("Function executed successfully. Result:", result)
    except Exception as e:
        print(f"Error executing function: {{e}}")

if __name__ == "__main__":
    main()
```"""
    return code_template
