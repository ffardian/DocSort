import streamlit as st
from docling.document_converter import DocumentConverter
from docling.document_converter import DocumentStream
from io import BytesIO
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from pathlib import Path
from Dropbox import DropBoxTool
load_dotenv(override=True)

#choose whether cloud or to save locally 
#cloud_provider = st.selectbox("Choose where to store the documents",["Local","Dropbox"],index=0)
cloud_provider = st.selectbox("Choose where to store the documents",["Dropbox"],index=0)
#File uploader to categorize file
uploaded_files = st.file_uploader("Classify documents and automatically assign to a folder (MULTIPLE DOCUMENTS ALLOWED)", accept_multiple_files=True, key="pdf_file_uploader",on_change=None, type=["jpg", "jpeg", "png","pdf","PDF","pptx"])

ACCESS_TOKEN_DROPBOX = os.getenv("DROPBOX_ACCESS_TOKEN")
LOCAL_FOLDER_PATH = os.getenv("LOCAL_FOLDER_PATH")

#Folder listing depending on whether to list subfolders on local machine or cloud provider, result is always the same, you get a list of sub folder
def listSubFolder(cloud_provider):
    match cloud_provider:
        case "Local":
            base_path = Path(LOCAL_FOLDER_PATH)
            # List all subdirectories
            folders = [f.name for f in base_path.iterdir() if f.is_dir()]
            return base_path,folders
        case "Dropbox":
            base_path = "/DocSort"
            db_cloud = DropBoxTool(ACCESS_TOKEN_DROPBOX) #o ACCESS_TOKEN_DROPBOX
            if not db_cloud.folder_exists("","DocSort"):
                db_cloud.create_folder(base_path)
            return base_path, db_cloud.list_dropbox_subfolders(path=base_path)


def invoke_categorization_process(uploaded_files,cloud_provider):
    if uploaded_files is not None:
        #Categorize all of the uploaded files 
        for uploaded_file in uploaded_files:
            # Construct a DocumentStream from the uploaded file
            document_stream = DocumentStream(
                name=uploaded_file.name,
                stream=BytesIO(uploaded_file.read())
            )
            converter = DocumentConverter()
            result = converter.convert(document_stream)
            content = result.document.export_to_text()
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            #Creates folder list for the prompt, that LLM knows, which folders already exist
            base_path, folders = listSubFolder(cloud_provider=cloud_provider)
            folder_list_text = "\n".join(f"- {f}" for f in folders)

            #LLM invocation for folder name based on content, name and already folder existing folders. ToDo: This prompt should be dynmaically adjustable
            response = client.responses.create(
            model="gpt-4.1",
            instructions=f"You are an document categorizer. You categorize documents by their content. If there are already a fitting category (folder) for a document, just classify the document using an existing folder. Otherwise, create a new folder name." \
            f"For example you recognize an invoice, check whether there is already a fitting folder name in the list. If yes, return the folder name where the documents fits in by the name. Otherwise, create a new folder name, which fits to that document. So you should always categorize the document by its type and content. If it helps you, you can also incorporate the file name." \
            f"I want you to simply answer with the proposed folder name from you, either a existing folder name or a new proposed folder name. Always think carefully, but just return the folder name.",
            input=f"The name of the Document is {uploaded_file.name} and the content is:\n\n {content}.\n\nThe following folders already exist and may represent categories:\n{folder_list_text}\n\nPlease reply with the most fitting folder name for this document. The convetion is always to use underscores for spaces in names and always to use small letters for the name.")
            folder_name_generated = response.output[0].content[0].text

            #Invoke create new folder function to create a new folder or to assign the document to a already existing folder 
            create_new_folder(folder_name_generated=folder_name_generated,uploaded_file=uploaded_file,cloud_provider=cloud_provider)
    
def create_new_folder(folder_name_generated,uploaded_file,cloud_provider):
    base_path, folders = listSubFolder(cloud_provider=cloud_provider)
    save_path = os.path.join(base_path, folder_name_generated, uploaded_file.name)

    match cloud_provider:
        case "Local":
            #If there is no folder at all
            if not folders:
                if not os.path.exists(base_path / folder_name_generated):
                    os.makedirs(base_path / folder_name_generated)
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                        st.toast("File saved successfully at path: " + save_path + " locally", icon=':material/save:')
            #There is a folder, but is there a folder which fits the proposed folder name
            else:
                # Check if folder that already exists
                if folder_name_generated in folders:
                        #Directly save pdf in folder path
                        with open(save_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                            st.toast("File saved successfully at path: " + save_path + " locally", icon=':material/save:')
                #If there are folders but there is no folder with the folder_name            
                else:
                    #Create a new folder and safe the file in the new folder_name path
                    if not os.path.exists(base_path / folder_name_generated):
                        os.makedirs(base_path / folder_name_generated)
                        with open(save_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                            st.toast("File saved successfully at path: " + save_path + " locally", icon=':material/save:')
        case "Dropbox":
            if not folders:
                 db_cloud = DropBoxTool(ACCESS_TOKEN_DROPBOX)
                 db_cloud.upload_to_generated_folder(
                     parent_path=base_path,
                     folder_name=folder_name_generated,
                     file_name=uploaded_file.name,
                     file_content=bytes(uploaded_file.getbuffer())
                     )
            else:
                 db_cloud = DropBoxTool(ACCESS_TOKEN_DROPBOX)
                 db_cloud.upload_to_generated_folder(
                     parent_path=base_path,
                     folder_name=folder_name_generated,
                     file_name=uploaded_file.name,
                     file_content=bytes(uploaded_file.getbuffer())
                     )

if uploaded_files:
    invoke_categorization_process(uploaded_files=uploaded_files,cloud_provider=cloud_provider)


