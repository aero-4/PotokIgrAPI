
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        host="localhost",
        port=8001,
        app="app:app",
        reload=True,
    )
