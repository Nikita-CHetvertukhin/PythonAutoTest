import os

def split_files_by_extension(folder_path, target_ext=".dzwf"):
    processes = []
    others = []

    for f in os.listdir(folder_path):
        full_path = os.path.join(folder_path, f)
        if os.path.isfile(full_path):
            if f.lower().endswith(target_ext):
                processes.append(f)
            else:
                others.append(f)
    
    return processes, others

def get_missing_files(upload_list, current_list):
    return [f for f in upload_list if f not in current_list]