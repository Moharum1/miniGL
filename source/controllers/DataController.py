from controllers.BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal

class DataController(BaseController):
    def __init__(self):
        self.size_scale = 1024 * 1024  # 1 MB in bytes
        super().__init__()
        

    def validate_data(self, data : UploadFile) -> tuple[bool, str]:
        if data.content_type not in self.settings.allowed_file_types:
            return False, ResponseSignal.FILE_TYPE_INVALID.value
        
        if data.size > self.settings.max_file_size * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALID.value
    
    

    