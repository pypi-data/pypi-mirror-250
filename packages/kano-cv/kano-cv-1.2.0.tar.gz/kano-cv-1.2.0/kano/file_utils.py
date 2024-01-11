import os
import shutil


def remove_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents removed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)

def list_files_in_folder(folder_path, keep_folder_path=True):
    files_list = []
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            if keep_folder_path:
                files_list.append(file_path)
            else:
                files_list.append(file_name)

    return files_list

def list_folders_in_folder(folder_path, keep_folder_path=True):
    folders_list = []
    
    for folder_name in os.listdir(folder_path):
        folder_path_entry = os.path.join(folder_path, folder_name)
        if os.path.isdir(folder_path_entry):
            if keep_folder_path:
                folders_list.append(folder_path_entry)
            else:
                folders_list.append(folder_name)

    return folders_list