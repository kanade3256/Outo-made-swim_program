import os
import shutil

class FileManager:
    """ ファイル管理クラス: データフォルダのリセット、コピー処理を担当 """
    
    def __init__(self, target_folder):
        self.target_folder = target_folder
        os.makedirs(self.target_folder, exist_ok=True)

    def reset_folder(self):
        """ フォルダの中身をリセット（.gitkeep は保持） """
        if os.path.exists(self.target_folder):
            for filename in os.listdir(self.target_folder):
                if filename == ".gitkeep":
                    continue
                file_path = os.path.join(self.target_folder, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

    def copy_files(self, files):
        """ ファイルをフォルダにコピー """
        copied_files = []
        for file_path in files:
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(self.target_folder, file_name)
            shutil.copy2(file_path, dest_path)
            copied_files.append(dest_path)
        return copied_files
