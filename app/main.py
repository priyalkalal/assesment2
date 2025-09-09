from fastapi import FastAPI, HTTPException

app = FastAPI()

items = [] 

@app.get("/")
def root():
    return {"hello":"world"}
    
@app.post("/items")
def create_item(item: str):
    items.append(item)
    return item 
    
@app.get("/items")
def list_items():
    return items

@app.get("/items/{item_id}")
def get_items(item_id: int) -> str:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found") 
    
