import dropbox
from dropbox.files import FolderMetadata
from pathlib import Path
from dotenv import load_dotenv
import os
import streamlit as st

class DropBoxTool:
    def __init__(self, token):
        self.dbx = dropbox.Dropbox(token)

    def upload_file(self, local_path, dropbox_path):
        with open(local_path, "rb") as f:
            self.dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
        st.info(f"Uploaded {local_path} to {dropbox_path}")

    def create_folder(self, path):
        try:
            self.dbx.files_create_folder_v2(path)
            print(f"Folder created: {path}")
        except dropbox.exceptions.ApiError as e:
            if "folder already exists" in str(e).lower():
                st.error("Folder already exists.")
            else:
                raise

    def list_folder(self, path=""):
        entries = self.dbx.files_list_folder(path).entries
        return [entry.name for entry in entries]
    
    def list_dropbox_subfolders(self, path: str):
        #List only the subfolders in the given Dropbox path.
        try:
            result = self.dbx.files_list_folder(path)
            folders = [entry.name for entry in result.entries if isinstance(entry, FolderMetadata)]
            return folders
        except dropbox.exceptions.ApiError as e:
            st.error(f"Error accessing {path}: {e}")
            return []
        
    def folder_exists(self, parent_path, folder_name):
        subfolders = self.list_dropbox_subfolders(parent_path)
        return folder_name in subfolders
    
    def upload_to_generated_folder(self, parent_path, folder_name, file_name, file_content):
        folder_path = f"{parent_path}/{folder_name}"
        file_path = f"{folder_path}/{file_name}"

        # Check if folder exists, create if not
        if not self.folder_exists(parent_path, folder_name):
            self.create_folder(folder_path)

        # Upload file to folder
        self.dbx.files_upload(file_content, file_path, mode=dropbox.files.WriteMode.overwrite)
        st.toast(f"File saved successfully at path: {file_path} on Dropbox", icon=":material/ios_share:")
