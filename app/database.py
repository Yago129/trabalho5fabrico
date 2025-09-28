from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client: AsyncIOMotorClient | None = None
db = None

async def connect_to_mongo():
    global client, db
    print("Conectando ao MongoDB Atlas...")
    try:
        client = AsyncIOMotorClient(
            settings.MONGO_URL,
            serverSelectionTimeoutMS=5000
        )
        db = client[settings.MONGO_DB]
        await client.admin.command('ping')
        print("Conexão com MongoDB Atlas estabelecida com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB Atlas: {e}")

async def close_mongo_connection():
    global client
    if client:
        print("Fechando conexão com MongoDB Atlas...")
        client.close()
        print("Conexão com MongoDB Atlas fechada.")

def get_message_collection():
    if db is None:
        raise RuntimeError("Conexão com o banco de dados não está ativa.")
    return db["messages"]