#!/usr/bin/env python3

from fastapi import FastAPI
import uvicorn

# Create a simple test app
app = FastAPI(title="Books Test Server", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Books & Library Test Server", "status": "working"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/test")
def test():
    return {"test": "success", "message": "Books platform is working"}

if __name__ == "__main__":
    print("🚀 Starting Books Test Server on port 8004...")
    uvicorn.run(app, host="0.0.0.0", port=8004)