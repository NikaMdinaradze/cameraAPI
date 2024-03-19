import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from db import collection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/cameras/")
async def search_items(
    search: str = None,
    brand: str = None,
    category: str = None,
    skip: int = 0,
    limit: int = 10
):
    query = {}

    if search:
        regex = re.compile(search, re.IGNORECASE)
        query["$or"] = [
            {"brand": {"$regex": regex}},
            {"model": {"$regex": regex}},
            {"description": {"$regex": regex}}
        ]

    if brand:
        query['brand'] = brand
    if category:
        query['category'] = category

    projection = {"_id": 1, "model": 1, "brand": 1, "price": 1, "category": 1, "images": 1}
    cursor = collection.find(query, projection).skip(skip).limit(limit)

    cameras = []
    async for document in cursor:
        document['_id'] = str(document['_id'])
        cameras.append(document)

    return {"results": cameras}

@app.get("/cameras/{camera_id}")
async def get_item(camera_id: str):
    try:
        object_id = ObjectId(camera_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    camera = await collection.find_one({"_id": object_id})
    if camera is None:
        raise HTTPException(status_code=404, detail="Camera not found")
    camera['_id'] = str(camera['_id'])
    return camera
