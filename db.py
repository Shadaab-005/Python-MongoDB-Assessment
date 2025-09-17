from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "assessment_db"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
employees_collection = db["employees"]
users_collection = db["users"]   

async def init_db():
    await employees_collection.create_index("employee_id", unique=True)
    await users_collection.create_index("username", unique=True)  
