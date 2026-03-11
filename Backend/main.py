from fastapi import FastAPI, UploadFile, File
from .search import search_arxiv
from .rag import ask_ai, vectorize_paper

app = FastAPI()

@app.get("/search")
def get_papers(query: str):
    return search_arxiv(query)

@app.post("/chat")
async def chat_with_papers(query: str, workspace_id: str):
    answer = await ask_ai(query, workspace_id)
    return {"response": answer}

@app.post("/import")
async def import_pdf(paper_id: str, file: UploadFile = File(...)):
    # In a real app, you would extract text from the PDF here
    content = await file.read()
    text = content.decode("utf-8") # Simplified for demo
    await vectorize_paper(paper_id, text)
    return {"status": "success"}