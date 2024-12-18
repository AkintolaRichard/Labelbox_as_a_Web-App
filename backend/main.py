from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId

load_dotenv()

DB_URL = os.environ.get("DB_URL")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB
client = MongoClient(DB_URL)

db = client.labelbox_db
images_collection = db.images
annotations_collection = db.annotations

# Pydantic models for request validation
class Image(BaseModel):
    name: str
    url: str

class Annotation(BaseModel):
    image_id: str
    label: str

# API to add images for annotation
@app.post("/images/")
async def add_image(image: Image):
    new_image = images_collection.insert_one(image.dict())
    return {"id": str(new_image.inserted_id), "message": "Image added successfully."}

# API to get all images for annotation
@app.get("/images/")
async def get_images():
    images = list(images_collection.find())
    for img in images:
        img["_id"] = str(img["_id"])
    return images

# API to save annotations
@app.post("/annotations/")
async def save_annotation(annotation: Annotation):
    if not ObjectId.is_valid(annotation.image_id):
        raise HTTPException(status_code=400, detail="Invalid image ID")
    new_annotation = annotations_collection.insert_one(annotation.dict())
    return {"id": str(new_annotation.inserted_id), "message": "Annotation saved successfully."}

# API to retrieve annotations
@app.get("/annotations/")
async def get_annotations():
    annotations = list(annotations_collection.find())
    for annotation in annotations:
        annotation["_id"] = str(annotation["_id"])
    return annotations
