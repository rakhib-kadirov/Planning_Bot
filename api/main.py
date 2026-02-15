from http.client import HTTPException
from fastapi import FastAPI, Depends
from sqlalchemy import select
from db import SessionLocal
from models import Lead, Client

app = FastAPI(title="PlaningChat Leads API")

@app.get("/leads/{client_id}")
async def get_leads(client_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Lead).where(Lead.client_id == client_id)
        )
        return result.scalars().all()
    
async def verify_client(client_id: int, session=Depends(SessionLocal)):
    async with session as s:
        result = await s.execute(
            select(Client).where(Client.id == client_id)
        )
        client = result.scalar_one_or_none()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client