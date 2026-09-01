from fastapi import FastAPI

app = FastAPI(title="RAG as a Service")


@app.get("/health")
def health_check():
    return {"status": "healthy"}