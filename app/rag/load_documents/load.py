import os


# ========================================
# SECTION 1: DOCUMENT LOADING
# ========================================


class LoadDocuments:
    def __init__(self):
        pass

    def load_documents(self, folder_path: str):
        index = -1

        print(os.listdir(folder_path))
        documents = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".md"):
                index += 1
                with open(
                    os.path.join(folder_path, filename), "r", encoding="utf-8"
                ) as f:
                    content = f.read()
                    documents.append(
                        {
                            "id": f"doc_{index}",
                            "content": content,
                            "title": filename.split(".")[0].capitalize(),
                        }
                    )
        return documents
