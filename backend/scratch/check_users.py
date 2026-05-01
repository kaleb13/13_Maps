
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models import User

async def list_users():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User))
        users = result.scalars().all()
        for user in users:
            print(f"ID: {user.id}, Email: {user.email}, Full Name: {user.full_name}, Role: {user.role}")

if __name__ == "__main__":
    asyncio.run(list_users())
