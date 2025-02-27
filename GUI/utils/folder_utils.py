# utils/folder_utils.py
import os
import shutil

def prepare_folder(target_folder: str):
    """
    フォルダを初期化（.gitkeep は削除対象外）。
    存在しない場合はフォルダを作成。
    """
    if os.path.exists(target_folder):
        for filename in os.listdir(target_folder):
            if filename == ".gitkeep":
                continue
            file_path = os.path.join(target_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        os.makedirs(target_folder, exist_ok=True)

def copy_files(file_paths: list[str], target_folder: str) -> list[str]:
    """
    指定されたファイルを指定フォルダにコピー。
    コピーされたファイルのパスをリストで返す。
    """
    copied_files = []
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(target_folder, file_name)
        shutil.copy2(file_path, dest_path)
        copied_files.append(dest_path)
    return copied_files
