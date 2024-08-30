from database.schemas import DetailClientSchema
from database.manager import ClientManager
from database.models import Client


class ClientLogicManager(ClientManager):
    def __init__(self) -> None:
        super().__init__()

    async def get_user(self, tg_id: int):
        client: Client = await self.get(params={"tg_id": tg_id})
        return DetailClientSchema(tg_id=client.tg_id, user_name=client.user_name)


def get_client_logic_manager() -> ClientLogicManager:
    return ClientLogicManager()