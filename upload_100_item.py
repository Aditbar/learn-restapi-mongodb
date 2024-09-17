from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["tutorial"]
collection_name = "items"

def upload_items():
  items_to_insert = []
  for i in range(1, 101):
    item = {
      "name": f"item {i}",
      "description": f"description of item {i}",
      "price": i*10}
    
    items_to_insert.append(item)
    
  if items_to_insert:
    db[collection_name].insert_many(items_to_insert)
    print("Uploaded 100 items to MongoDB")
    
if __name__ == "__main__":
  upload_items()