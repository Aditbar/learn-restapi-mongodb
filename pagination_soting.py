from fastapi import FastAPI, Query
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["tutorial"]
collection_name = "items"

@app.get("/items")
def get_all_items(skip: int = Query(0), limit: int = Query(10, ge=1, le=100)):
  items = db[collection_name].find().skip(skip).limit(limit)
  items_list = [item for item in items]
  item_list_processed = []
  for item in items_list:
    item["_id"] = str(item["_id"])
    item_list_processed.append(item)
  return item_list_processed

@app.get("/items_sort/")
def get_all_items_sort(sort_by: str = Query(None, description="Field to sort by")):
  sort_order = 1
  if sort_by:
    items = db[collection_name].find().sort(sort_by, sort_order)
  else:
    items = db[collection_name].find()
  items_list = [item for item in items]
  items_list_processed = []
  for item in items_list:
    item["_id"] = str(item["_id"])
    items_list_processed.append(item)
  return items_list_processed