from controllers.BaseController import BaseController
import os

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.file_dir = os.path.join(self.base_dir, "assets/files")

    def get_project_pass(self, project_id: str) -> str:
        project_dir = os.path.join(self.file_dir, project_id)
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        return project_dir