from datetime import datetime
from fastapi import UploadFile
from typing import List
import shutil


class HandleFile:
    def __init__(self):
        pass

    def save_files(self, agent_folder: str, files: List[UploadFile]):
        for file in files:
            file_path = agent_folder / file.filename
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

    def get_files(self, agent_folder: str):
        file_details = []

        if agent_folder.exists() and agent_folder.is_dir():
            for file in agent_folder.iterdir():
                if (
                    file.is_file() and file.suffix.lower() == ".md"
                ):  # only markdown files
                    stat = file.stat()

                    last_modified_ts = int(stat.st_mtime * 1000)  # JS timestamp (ms)

                    file_details.append(
                        {
                            "name": file.name,
                            "size": stat.st_size,
                            "lastModified": last_modified_ts,
                            "lastModifiedDate": datetime.fromtimestamp(
                                stat.st_mtime
                            ).isoformat(),
                        }
                    )

        return file_details

    def delete_files(self, agent_folder: str, agent_name: str, email: str):
        if agent_folder.exists() and agent_folder.is_dir():
            for file in agent_folder.iterdir():
                if file.is_file():
                    file.unlink()
