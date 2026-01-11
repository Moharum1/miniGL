from .BaseDataModel import BaseDataModel
from .Enums.DataBaseEunm import DataBaseEnum
from .DB.dataChunk import DataChunk
from pymongo import InsertOne

class ChunkModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK.value]

    async def create_chuck(self, chunk_data: DataChunk) -> str:
        result = await self.collection.insert_one(chunk_data.model_dump(by_alias=True, exclude_unset=True))
        chunk_data.id = result.inserted_id
        return result.inserted_id
    
    async def get_chunk(self, chunk_id: str) -> DataChunk:
        record = await self.collection.find_one({"_id": chunk_id})
        if record:
            return DataChunk(**record)
        return None
    
    async def insert_mini_chunks(self, chunks: list[DataChunk], batch_size = 100) -> list[str]:
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            operations = [InsertOne(chunk.model_dump(by_alias=True, exclude_unset=True)) for chunk in batch]
            await self.collection.bulk_write(operations)
        return len(chunks)
    
    async def delete_chunks_by_project_id(self, project_id: str) -> int:
        result = await self.collection.delete_many({"project_id": project_id})
        return result.deleted_count