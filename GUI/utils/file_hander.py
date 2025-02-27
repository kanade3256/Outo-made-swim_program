import os
import shutil

class FileHandler:
    def __init__(self, target_folder="data/folder"):
        self.target_folder = target_folder
        self._initialize_folder()

    def _initialize_folder(self):
        """ フォルダの初期化（.gitkeepを除いてクリア） """
        if os.path.exists(self.target_folder):
            for filename in os.listdir(self.target_folder):
                if filename == ".gitkeep":
                    continue
                file_path = os.path.join(self.target_folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
        else:
            os.makedirs(self.target_folder, exist_ok=True)

    def copy_files(self, file_paths):
        """ ファイルをコピーする """
        copied_files = []
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(self.target_folder, file_name)
            shutil.copy2(file_path, dest_path)
            copied_files.append(dest_path)
        return copied_files
