from dotenv import load_dotenv
from fastapi import FastAPI
import os
import json
from typing import List
from supabase import create_client, Client
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

url: str = os.getenv('SUPABASE_URL')
key: str = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Recipe(BaseModel):
    title: str
    description: str
    ingredients: List[str]
    instruction: str


@app.post("/api/recipes")
async def add_recipe(item: Recipe):
    data, count = supabase.table('recipes') \
        .insert({
            "title": item.title,
            "description": item.description,
            "ingredients": item.ingredients,
            "instruction": item.instruction
        }) \
        .execute()

    return {"success": True, "data": data}


@app.get("/api/recipes")
async def add_recipe(recipe_id: int):
    print(recipe_id)

    if recipe_id:
        response = supabase.table('recipes').select('*').eq('id', recipe_id).execute()
    else:
        response = supabase.table('recipes').select('title', 'description', 'id').execute()

    return {"success": True, "response": response}
