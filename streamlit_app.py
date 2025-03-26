import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("ALGO_ROOT_Assignment")

tabs = st.tabs([
    "Execute Function",
    "List Available Commands",
    "Copy Code To File",
    "Add Function",
    "Get History"
])
with tabs[0]:
    st.header("Execute Function")
    prompt = st.text_input("Enter your prompt:", key="execute_prompt")
    session_id = st.text_input("Session ID (optional):", key="execute_session")
    if st.button("Execute", key="execute_btn"):
        data = {"prompt": prompt}
        if session_id:
            data["session_id"] = session_id
        response = requests.post(f"{BASE_URL}/execute", json=data)
        if response.status_code == 200:
            result = response.json()
            st.markdown("### Generated Code")
            st.code(result["code"], language="python")
            st.success(f"Function executed: {result['function']}")
        else:
            st.error(response.json().get("detail", "Error occurred"))

with tabs[1]:
    st.header("List Available Commands")
    if st.button("Get Commands", key="get_commands_btn"):
        response = requests.get(f"{BASE_URL}/commands")
        if response.status_code == 200:
            commands = response.json().get("available_commands", [])
            st.markdown("### Available Commands")
            for cmd in commands:
                st.write(f"- {cmd}")
        else:
            st.error(response.json().get("detail", "Error occurred"))

with tabs[2]:
    st.header("Copy Code To File")
    prompt_copy = st.text_input("Enter your prompt:", key="copy_prompt")
    if st.button("Copy Code", key="copy_btn"):
        data = {"prompt": prompt_copy}
        response = requests.post(f"{BASE_URL}/copy", json=data)
        if response.status_code == 200:
            result = response.json()
            st.success(result["message"])
            st.write("File Path:", result["file_path"])
        else:
            st.error(response.json().get("detail", "Error occurred"))

with tabs[3]:
    st.header("Add Custom Function")
    new_func_name = st.text_input("Function Name:", key="add_func_name")
    new_func_desc = st.text_area("Function Description:", key="add_func_desc")
    if st.button("Add Custom Function", key="add_func_btn"):
        data = {"function_name": new_func_name, "description": new_func_desc}
        response = requests.post(f"{BASE_URL}/add_function", json=data)
        if response.status_code == 200:
            st.success("Custom function added!")
            st.write(response.json())
        else:
            st.error(response.json().get("detail", "Error occurred"))
with tabs[4]:
    st.header("Get History")
    history_session_id = st.text_input("Enter Session ID:", key="history_session")
    if st.button("Get History", key="get_history_btn"):
        response = requests.get(f"{BASE_URL}/history/{history_session_id}")
        if response.status_code == 200:
            history = response.json().get("history", [])
            st.markdown("### Session History")
            for entry in history:
                st.write(f"**Prompt:** {entry['prompt']}")
                st.markdown(entry['response'])
                st.markdown("---")
        else:
            st.error(response.json().get("detail", "Error occurred"))
