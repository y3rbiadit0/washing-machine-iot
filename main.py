import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:create_app", host="0.0.0.0", port=8001, reload=True)
