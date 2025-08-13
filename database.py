from motor import motor_asyncio
from motor.core import AgnosticClient

from logger import LOGS
from config import MONGO_URL

class Database:
    def __init__(self, uri: str) -> None:
        self.client: AgnosticClient = motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client["chatbot"]
        self.backup_gemini = self.db["gemini"]
        
    async def connect(self):
        try:
            await self.client.admin.command("ping")
            LOGS.info(f"Database onnected")
        except Exception as e:
            LOGS.info(f"DatabaseErr: {e} ")
            quit(1)

    async def _close(self):
        await self.client.close()

db = Database(MONGO_URL)
