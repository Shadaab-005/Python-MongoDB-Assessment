from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "assessment_db"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
employees_collection = db["employees"]

# Creating unique index on employee_id
async def init_db():
    await employees_collection.create_index("employee_id", unique=True)
