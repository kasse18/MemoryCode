from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import db

app = FastAPI()

class Data_People(BaseModel):
    id: int
    name: str
    biography: str
    epitaph: str


class Data(BaseModel):
    id: int
    queue: str
    biography: str
    epitaph: str

class GetID(BaseModel):
    id: int


@app.post("/create")
async def create_data(item: Dict[int, str]):
    status = await db.load_data(item["id"], item["questions"])
    return {"status": status}

@app.post("/add")
async def add_data(item: Data):
    status = await db.load_data([item.id, item.name, item.biography, item.epitaph])
    return {"status": status}

@app.post("/add_people")
async def add_data_people(item: Data):
    status = await db.load_data([item.id, item.name, item.biography, item.epitaph])
    return {"status": status}

@app.post("/get")
async def return_data(item: GetID):
    status = await db.return_data(item.id)
    return {"data": status}


@app.post("/get_people")
async def return_data_people(item: GetID):
    status = await db.return_data(item.id)
    return {"data": status}

@app.post("/put")
async def return_data(item: Data):
    status = await db.return_data(item.id)
    return {"status": status}

@app.post("/put_people")
async def return_data_people(item: Data):
    status = await db.return_data(item.id)
    return {"status": status}
