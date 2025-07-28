import os.path
from datetime import datetime
import shutil
import zipfile

class BackupManager:
    def __init__(self, src_path, dest_root_path, use_zip=False):
        self.src_path = src_path
        self.dest_root_path = dest_root_path
        self.use_zip = use_zip

    def perform_backup(self):
        try:
            backup_name = self._generate_backup_name()
            dest_path = os.path.join(self.dest_root_path, backup_name)
            self._copy_folder(dest_path)
            if self.use_zip:
                self._zip_folder(dest_path)
                dest_path = f"{dest_path}.zip"        
            return {"success": True, "backup_path": dest_path}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _generate_backup_name(self):
        path = self.src_path
        basename = os.path.basename(path)
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d_%H-%M")
        backup_name = f"{basename}_{formatted_time}"
        return backup_name

    def _copy_folder(self, dest_path):
        if os.path.isfile(self.src_path):
            base = os.path.splitext(os.path.basename(self.src_path))[0]
            ext = os.path.splitext(self.src_path)[1]
            unique_dest = dest_path
            counter = 1
            while os.path.exists(unique_dest):
                unique_dest = os.path.join(
                os.path.dirname(dest_path),
                f"{base}_{counter}{ext}"
                )
                counter += 1
            shutil.copy2(self.src_path, unique_dest)
        elif os.path.isdir(self.src_path):
            base = os.path.basename(self.src_path)
            unique_dest = dest_path
            counter = 1
            while os.path.exists(unique_dest):
                unique_dest = f"{dest_path}_{counter}"
                counter += 1
            shutil.copytree(self.src_path, unique_dest)
        else:
            print("Not a file, not a folder!")

    def _zip_folder(self, folder_path):
        zip_path = f"{folder_path}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, folder_path)
                    zipf.write(full_path, arcname=relative_path)

        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
        else:
            os.remove(folder_path)
