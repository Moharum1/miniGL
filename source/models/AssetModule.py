from .BaseDataModel import BaseDataModel
from .Enums.DataBaseEunm import DataBaseEnum
from .DB.asset import Asset

class AssetModule(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSETS.value]

    @classmethod
    async def create_module(cls, db_client):
        module = cls(db_client)
        await module.init_collection()
        return module

    async def init_collection(self):
        all_collection = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSETS.value not in all_collection:
            await self.db_client.create_collection(DataBaseEnum.COLLECTION_ASSETS.value)
            # Create Indexes
            for index in Asset.get_index():
                await self.collection.create_index(index["key"], name=index["name"], unique=index["unique"])

    async def create_asset(self, asset_data: Asset) -> Asset:
        result = await self.collection.insert_one(asset_data.model_dump(by_alias=True, exclude_unset=True))
        asset_data.id = result.inserted_id
        return asset_data
    
    async def get_all_project_assets(self, project_id: str) -> list[Asset]:   
        return await self.collection.find({"project_id": project_id}).to_list(length=None)