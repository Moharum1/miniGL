from controllers.BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
from controllers import ProjectController
import regex as re
import os

class DataController(BaseController):
    def __init__(self):
        self.size_scale = 1024 * 1024  # 1 MB in bytes
        super().__init__()
        

    def validate_data(self, data : UploadFile) -> tuple[bool, str]:
        if data.content_type not in self.settings.FILE_ALLOWED_EXTENSIONS:
            return False, ResponseSignal.FILE_TYPE_INVALID.value
        
        if data.size > self.settings.FILE_MAX_SIZE_MB * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALID.value
    
    def generate_unique_filename(self, original_filename: str, project_id: str) -> str:
        random_str = self.generate_random_string()
        project_path = ProjectController().get_project_pass(project_id)
        cleaned_name = self.clean_filename(original_filename)

        unique_filename = f"{random_str}_{cleaned_name}"
        file_path = os.path.join(project_path, unique_filename)
        while os.path.exists(file_path):
            random_str = self.generate_random_string()
            unique_filename = f"{random_str}_{cleaned_name}"
            file_path = os.path.join(project_path, unique_filename)

    def clean_filename(self, filename: str) -> str:
        cleaned_name = re.sub(r'[^\w.]', '', filename)
        cleaned_name = cleaned_name.replace(' ', '_')
        return cleaned_name    