from fastapi import FastAPI

app = FastAPI()

@app.get("/search")
def search_items(query: str = '', limit: int = 10):
    """Use query params like /search?q=python&limit=3"""
    return {"query": query, "limit": limit}
