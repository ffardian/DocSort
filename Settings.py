import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv(override=True)
LOCAL_FOLDER_PATH = os.getenv("LOCAL_FOLDER_PATH")

def update_env_variable(key, value, env_path=".env"):
    lines = []
    found = False

    # Read the file line by line
    with open(env_path, "r") as f:
        for line in f:
            if line.strip().startswith(f"{key}="):
                lines.append(f"{key}={value}\n")
                found = True
            else:
                lines.append(line)

    # If the key was not found, add it
    if not found:
        lines.append(f"{key}={value}\n")

    # Write everything back to the file
    with open(env_path, "w") as f:
        f.writelines(lines)

openai_api_key = st.text_input(label="Enter your OpenAI API Key here")
if st.button("Update OpenAI api key"):
    #update_env_variable("OPENAI_API_KEY", openai_api_key)
    st.session_state["openaiapikey"] = openai_api_key
    st.info("Successfully updated OpenAI api key")
    st.rerun()

dropbox_api_key = st.text_input(label="Enter your Dropbox api key here")
if st.button("Update Dropbox api key"):
    #update_env_variable("DROPBOX_ACCESS_TOKEN", dropbox_api_key)
    st.session_state["dropboxapikey"] = dropbox_api_key
    st.info("Successfully updated Dropbox api key")
    st.rerun()

local_folder_path = st.text_input(label="Enter your default path for folder structure",placeholder=f"Current path: {LOCAL_FOLDER_PATH}",key="localpath")
if st.button("Update local folder path"):
    #update_env_variable("LOCAL_FOLDER_PATH", local_folder_path)
    st.session_state["localfolderpath"] = local_folder_path
    st.info("Successfully updated local folder path")
    st.rerun()



