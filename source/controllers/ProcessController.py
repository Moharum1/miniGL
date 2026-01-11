from controllers import BaseController,ProjectController
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.Enums.ProcessingEnums import ProcessEnums
import os

class ProcessController(BaseController):
    def __init__(self, project_id: int):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_pass(project_id)

    def get_file_extension(self, filename: str):
        return filename.split('.')[-1]
    
    def get_file_loader(self, filename: str):
        extension = self.get_file_extension(filename)
        file_path = os.path.join(self.project_path, filename)

        if extension == ProcessEnums.TXT.value:
            return TextLoader(file_path, encoding='utf8')
        elif extension == ProcessEnums.PDF.value:
            return PyMuPDFLoader(file_path)
        else:
            return None
        
    def get_file_content(self, filename: str):
        loader = self.get_file_loader(filename)
        if loader:
            documents = loader.load()
            return documents
        return None
    
    def process_file_content(self, filename: str, chunk_size: int = 100, chunk_overlap: int = 20):
        documents = self.get_file_content(filename)
        if documents:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
            chunks = text_splitter.split_documents(documents)
            return chunks
        return None