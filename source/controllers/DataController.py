from controllers.BaseController import BaseController
from fastapi import UploadFile

class DataController(BaseController):
    def __init__(self):
        self.size_scale = 1024 * 1024  # 1 MB in bytes
        super().__init__()
        

    def validate_data(self, data : UploadFile) -> tuple[bool, str]:
        if data.content_type not in self.settings.allowed_file_types:
            return False, "Unsupported file type."
        
        if data.size > self.settings.max_file_size * self.size_scale:
            return False, "File size exceeds the maximum limit."
        
        return True, "File is valid."
    
    

    