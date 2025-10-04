from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

class RAGPipeline:
    def __init__(self, file_path="data/my_details.txt"):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found.")

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = splitter.create_documents([text])

        # Force CPU to avoid meta tensor error
        self.embedder = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )

        self.db = FAISS.from_texts([d.page_content for d in docs], embedding=self.embedder)

    def retrieve(self, query, k=3):
        docs = self.db.similarity_search(query, k=k)
        return "\n".join([d.page_content for d in docs])
