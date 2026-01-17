from .BaseDataModel import BaseDataModel
from .Enums.DataBaseEunm import DataBaseEnum
from .DB.project import Project
    
class ProjectModule(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECTS.value]

    @classmethod
    async def create_module(cls, db_client):
        module = cls(db_client)
        await module.init_collection()
        return module

    async def init_collection(self):
        all_collection = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECTS.value not in all_collection:
            await self.db_client.create_collection(DataBaseEnum.COLLECTION_PROJECTS.value)
            # Create Indexes
            for index in Project.get_index():
                await self.collection.create_index(index["key"], name=index["name"], unique=index["unique"])

    async def create_project(self, project_data: Project) -> str:
        result = await self.collection.insert_one(project_data.model_dump(by_alias=True, exclude_unset=True))
        return result.inserted_id
    
    async def get_project_by_id(self, project_id: str) -> Project:
        record = await self.collection.find_one({"project_id": project_id})
        if record:
            return Project(**record)
        # Create a new project if not found
        new_project = Project(project_id=project_id)
        inserted_id = await self.create_project(new_project)
        new_project.id = inserted_id
        return new_project
    
    async def get_all_projects(self, index : int = 1, limit: int = 10) -> list[Project]:
        projects = []

        total_docs = await self.collection.count_documents({})
        total_pages = total_docs // limit
        if total_docs % limit > 0:
            total_pages += 1
            
        cursor = self.collection.find({}).skip((index-1) * limit).limit(limit)
        async for document in cursor:
            projects.append(Project(**document))
        return projects, total_pages
